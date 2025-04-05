import discord
import asyncio
import sys
import logging
from discord.ext import commands
from scraper import login_and_fetch_tasks
from task_store import load_seen_tasks, save_seen_tasks, get_new_tasks
from dotenv import load_dotenv
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('task_bot')

load_dotenv()

TOKEN = os.getenv("bot_token")
CHANNEL_ID = int(os.getenv("channel_id"))

logger.info(f"Starting bot with token: {TOKEN[:10]}...{'*' * 10}")
logger.info(f"Channel ID: {CHANNEL_ID}")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def sort_tasks_by_id(tasks):
    """Sort tasks by ID, converting to integer if possible"""
    return sorted(tasks, key=lambda task: int(task['id']) if task['id'].isdigit() else task['id'])

@bot.event
async def on_ready():
    logger.info(f"✅ Bot logged in as {bot.user}")
    bot.loop.create_task(task_check_loop())

@bot.command()
async def tasks(ctx):
    logger.info(f"Tasks command triggered by {ctx.author}")
    tasks = login_and_fetch_tasks()
    sorted_tasks = sort_tasks_by_id(tasks)
    message = "**Latest Tasks:**\n"
    for task in sorted_tasks:
        message += f"• {task['title']} (ID: {task['id']})\n"
    await ctx.send(message)

async def task_check_loop():
    await bot.wait_until_ready()

    while True:
        logger.info("🔍 Checking for new tasks...")
        try:
            current_tasks = login_and_fetch_tasks()
            logger.info(f"🪪 Found {len(current_tasks)} tasks")
            seen_tasks = load_seen_tasks()
            new_tasks = get_new_tasks(current_tasks, seen_tasks)

            if not seen_tasks and current_tasks:
                logger.info("💾 First run – initializing seen_tasks.json")
                save_seen_tasks(current_tasks)

            if new_tasks:
                logger.info(f"📢 New tasks found: {len(new_tasks)}")
                channel = bot.get_channel(CHANNEL_ID)
                if not channel:
                    logger.error(f"Could not find channel with ID: {CHANNEL_ID}")
                    continue
                    
                sorted_new_tasks = sort_tasks_by_id(new_tasks)
                for task in sorted_new_tasks:
                    await channel.send(f"🆕 New Task: **{task['title']}** (ID: `{task['id']}`)")
                save_seen_tasks(current_tasks)
            else:
                logger.info("✅ No new tasks found.")
        except Exception as e:
            logger.exception(f"❌ Error during task check: {e}")

        await asyncio.sleep(600)  # wait 10 minutes

if __name__ == "__main__":
    logger.info("Bot is starting...")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        logger.error("Failed to login to Discord. Please check your bot token.")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error starting bot: {e}")
        sys.exit(1)

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
    status_msg = await ctx.send("🔍 Fetching tasks...")
    
    try:
        tasks = login_and_fetch_tasks()
        sorted_tasks = sort_tasks_by_id(tasks)
        
        message = "**Latest Tasks:**\n"
        for task in sorted_tasks:
            message += f"• {task['title']} (ID: {task['id']})\n"
        
        await status_msg.edit(content=message)
        logger.info(f"Displayed {len(tasks)} tasks for {ctx.author}")
    except Exception as e:
        await status_msg.edit(content=f"❌ Error fetching tasks: {str(e)}")
        logger.exception(f"Error during task fetch: {e}")


@bot.command()
async def updates(ctx):
    logger.info(f"Updates command triggered by {ctx.author}")
    
    # Initial message
    status_msg = await ctx.send("🔍 Checking for new tasks...")
    
    try:
        current_tasks = login_and_fetch_tasks()
        seen_tasks = load_seen_tasks()
        new_tasks = get_new_tasks(current_tasks, seen_tasks)

        if new_tasks:
            sorted_new_tasks = sort_tasks_by_id(new_tasks)
            await status_msg.edit(content=f"📢 Found {len(new_tasks)} new tasks!")
            
            for task in sorted_new_tasks:
                await ctx.send(f"🆕 New Task: **{task['title']}** (ID: `{task['id']}`)")
            
            # Update seen tasks after notifying
            save_seen_tasks(current_tasks)
            logger.info(f"Updated seen_tasks.json with {len(new_tasks)} new tasks")
        else:
            await status_msg.edit(content="✅ No new tasks available.")
            logger.info("No new tasks found during manual check")
            
    except Exception as e:
        await status_msg.edit(content=f"❌ Error checking for updates: {str(e)}")
        logger.exception(f"Error during manual task check: {e}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Unknown command. Use `!tasks` to see all available tasks or `!updates` to check for new tasks.")
        logger.info(f"User {ctx.author} tried to use an unknown command: {ctx.message.content}")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
        logger.info(f"User {ctx.author} missed required argument: {error.param}")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        logger.exception(f"Command error: {error}")


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

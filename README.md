# 🤖 Wargaming Course - New Task Notifier Discord Bot

A Discord bot that scrapes Wargaming's Backend SWE Course platform for new tasks and immediately notifies users in our Discord server.

The idea came to me after constantly having to check for updates manually—I wanted a solution that would help not just me, but also the 50 other course participants stay on top of new assignments effortlessly. Currently, the bot runs locally, and I'm planning to deploy it soon for 24/7 automated monitoring.

## Features

- 🔄 **Automated Monitoring:** Checks for new course tasks every 10 minutes using Selenium web automation.
- 🔔 **Real-Time Notifications:** Posts instant alerts in a designated Discord channel when new tasks are detected.
- 💾 **Task Tracking:** Maintains a record of previously seen tasks to prevent duplicate notifications.
- 🤖 **Command Interface:** Enables users to retrieve current tasks or check for updates on demand using simple commands.

## Current Status

⚠️ **Note:** This bot currently only works locally when running the Python file. I'm planning to deploy it to a cloud service to provide 24/7 availability and share it with our course Discord server of approximately 50 participants to help everyone stay updated on new assignments.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/tsembp/WG-Course-Task-Notifier-Bot.git
   cd WG-Course-Task-Notifier-Bot
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables (see Configuration section)

## Configuration

Create a `.env` file in the project root with the following variables:

```
# Wargaming Board Platform Credentials
wg_username = "username"
wg_password = "password"
login_url = "url/login"
tasks_url = "url/tasks"

# Discord Bot Config Parameters
bot_token = "token"
bot_url = "url"
channel_id = "id"
permissions_int = "perms"
```

### Getting Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" tab and click "Add Bot"
4. Copy the token from the "Token" section

### Getting Channel ID

1. Enable Developer Mode in Discord (Settings > Advanced > Developer Mode)
2. Right-click on the channel you want to use and select "Copy ID"

## Usage

Run the bot:

```
python bot.py
```

The bot will automatically check for new tasks every 10 minutes and post notifications to the configured Discord channel.

## Commands

- `!tasks` - Displays all available tasks from the course platform
- `!updates` - Checks for new tasks


## Dependencies

- discord.py - Discord API wrapper
- selenium - Web automation
- python-dotenv - Environment variable management

## License

[MIT License](LICENSE)
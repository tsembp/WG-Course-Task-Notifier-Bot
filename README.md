# 🤖 Wargaming Task Notifier Discord Bot

A Discord bot that automatically checks for new tasks in Wargaming's Backend SWE Course platform and notifies a specified Discord channel when new tasks become available for students to attempt.

This project idea came to me after I wanted to somehow get notified for when the tutors of the course added a new task on the platform so I can go ahead and complete it.

## Features

- 🔄 Automatically checks for new course tasks every 10 minutes
- 🔔 Posts notifications to your Discord channel when new tasks are found
- 💾 Keeps track of previously seen tasks to avoid duplicate notifications
- 🤖 Command-based interaction to view all current tasks

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
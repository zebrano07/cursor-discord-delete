# Discord Message Cleaner Bot

A Discord bot that can delete messages in bulk from Discord channels. The bot supports deleting a specific number of messages or all messages in a channel, with the ability to stop the deletion process.

## Features

- Delete a specific number of messages from a channel
- Delete all messages from a channel
- Stop deletion process mid-way
- PostgreSQL database for storing server configurations
- Docker containerization for easy deployment

## Prerequisites

- Docker and Docker Compose installed
- A Discord Bot Token (see Setup Instructions)
- Basic understanding of Discord bot permissions

## Setup Instructions

### 1. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Reset Token" to get your bot token
5. Enable these "Privileged Gateway Intents":
   - Message Content Intent
   - Server Members Intent
6. Go to OAuth2 -> URL Generator
7. Select these scopes:
   - bot
   - applications.commands
8. Select these bot permissions:
   - Manage Messages
   - Read Message History
   - Send Messages
9. Use the generated URL to invite the bot to your server

### 2. Environment Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/discord-message-cleaner.git
cd discord-message-cleaner
```

2. Create a `.env` file in the root directory:
```plaintext
# PostgreSQL Configuration
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Discord Configuration
DISCORD_BOT_TOKEN=your_bot_token_here

# Note: Never share or commit your .env file containing real credentials
```

For local development, you can use these default values:
- POSTGRES_USER: postgres
- POSTGRES_PASSWORD: postgres
- POSTGRES_DB: discord_cleaner

### 3. Running the Bot

1. Build and start the containers:
```bash
docker compose build
docker compose up -d
```

2. To view logs:
```bash
docker compose logs -f
```

## Usage

The bot responds to the following commands:

- `!setup` - Configure the current channel for message deletion
- `!clear [number]` - Delete messages
  - With number: Deletes that specific number of messages
  - Without number: Deletes all messages in the channel
- `!stop` - Stops an ongoing deletion process

### Examples:
```
!clear 10    # Deletes 10 most recent messages
!clear       # Starts deleting all messages
!stop        # Stops the deletion process
```

## Important Notes

- The bot requires "Manage Messages" permission in the channels where it will delete messages
- Message deletion has a built-in delay to respect Discord's rate limits
- The bot will provide feedback about the deletion process and number of messages deleted
- Use `!stop` if you accidentally start deleting all messages

## Troubleshooting

1. If the bot doesn't respond:
   - Check if the bot is online in your Discord server
   - Verify the bot token in your `.env` file
   - Check the Docker logs for any errors

2. If messages aren't being deleted:
   - Verify the bot has "Manage Messages" permission in the channel
   - Check if the bot's role is positioned high enough in the server settings

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

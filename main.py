import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot_commands import setup_commands

# Load environment variables
load_dotenv()

# Access the bot token
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Create a bot instance with the necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Set up the commands
setup_commands(bot)

# Run the bot
bot.run(BOT_TOKEN)

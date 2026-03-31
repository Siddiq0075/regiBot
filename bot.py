import discord
from discord.ext import commands
import asyncio
from config import DISCORD_TOKEN
from database.db_client import client
from cogs.setup import setup_all

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("🔁 Slash commands synced successfully!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

async def load_cogs():
    await setup_all(bot)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n🛑 Bot stopped by user. Closing DB connection...")
    client.close()
    print("✅ DB connection closed. Goodbye!")

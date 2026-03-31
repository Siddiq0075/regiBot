import asyncio

async def setup_all(bot):
    """Loads all bot cogs automatically."""
    await bot.load_extension("cogs.public_commands")
    await bot.load_extension("cogs.admin_commands")
    await bot.load_extension("cogs.export_command")
    print("✅ All cogs loaded successfully!")

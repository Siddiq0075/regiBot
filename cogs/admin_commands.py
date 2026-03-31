import discord
from discord import app_commands
from discord.ext import commands
from database.db_client import reset_counter, users as find_user

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🧾 /list — List all registered participants (Admin only)
    @app_commands.command(name="list", description="List all registered participants (Admin only)")
    @app_commands.default_permissions(administrator=True)
    async def list_registrations(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        participants = list(find_user.find({}, {"_id": 0, "name": 1, "reg_number": 1, "college": 1}))
        if not participants:
            embed = discord.Embed(
                title="📭 No Registrations Yet",
                description="Looks like no one has registered so far.",
                color=discord.Color.greyple()
            )
            embed.set_footer(text="Check back later after more participants join!")
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        # Format participant list
        lines = [f"• **{p['name']}** ({p['college']}) — `#{p['reg_number']}`" for p in participants]
        chunks, current = [], ""
        for line in lines:
            if len(current) + len(line) > 3800:
                chunks.append(current)
                current = ""
            current += line + "\n"
        if current:
            chunks.append(current)

        # Send paginated embeds
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"🏆 Registered Participants (Page {i + 1}/{len(chunks)})",
                description=chunk,
                color=discord.Color.gold()
            )
            if i == len(chunks) - 1:
                embed.set_footer(text=f"Total Registered: {len(participants)} participants 🎉")
            else:
                embed.set_footer(text="Use /list again to refresh the data.")
            await interaction.followup.send(embed=embed, ephemeral=True)

    # 🧹 /clear — Clear all registration data (Admin only)
    @app_commands.command(name="clear", description="Clear all registration data (Admin only)")
    @app_commands.default_permissions(administrator=True)
    async def clear_registrations(self, interaction: discord.Interaction):
        # Ask for confirmation first
        embed = discord.Embed(
            title="⚠️ Confirm Data Wipe",
            description="This will **delete all registrations permanently**.\n\nAre you sure you want to continue?",
            color=discord.Color.red()
        )
        embed.set_footer(text="Action cannot be undone!")

        # Confirmation buttons
        view = discord.ui.View()
        confirm_button = discord.ui.Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
        cancel_button = discord.ui.Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)

        async def confirm_callback(interaction2: discord.Interaction):
            find_user.delete_many({})
            reset_counter()
            confirm_embed = discord.Embed(
                title="🧹 Data Cleared Successfully",
                description="All registration records have been wiped from the database.",
                color=discord.Color.green()
            )
            confirm_embed.set_footer(text="You can start fresh registrations now.")
            await interaction2.response.edit_message(embed=confirm_embed, view=None)

        async def cancel_callback(interaction2: discord.Interaction):
            cancel_embed = discord.Embed(
                title="❎ Cancelled",
                description="No data was deleted. Everything is safe.",
                color=discord.Color.blurple()
            )
            await interaction2.response.edit_message(embed=cancel_embed, view=None)

        confirm_button.callback = confirm_callback
        cancel_button.callback = cancel_callback
        view.add_item(confirm_button)
        view.add_item(cancel_button)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    #🔍 /lookup (Admin Only)
    @app_commands.command(name="lookup", description="Lookup a participant by registration number (Admin only)")
    @app_commands.describe(
        reg_number="Registration ID (e.g. SWAP001)",
        user="Mention the user to search"
    )
    @app_commands.default_permissions(administrator=True)
    async def lookup_registration(self, interaction: discord.Interaction, reg_number: str = None, user: discord.User = None):
        await interaction.response.defer(ephemeral=True)
        
        # Ensure at least one input is provided
        if not reg_number and not user:
            await interaction.followup.send(
                "⚠️ please provide either a registration ID or mention a user.",
                ephemeral=True
            )
            return
        
        query = {}
        if reg_number:
            query["reg_number"] = reg_number.upper()
        if user:
            query["discord_id"] = user.id
            
        result = find_user.find_one(query)
        
        if not result:
            await interaction.followup.send("❌ No participant found with the provided details.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🔎 Registration Lookup Result",
            color=discord.Color.light_grey()
        )
        embed.add_field(name="👤 Name", value=result["name"], inline=False)
        embed.add_field(name="🤝 Partner", value=result["partner_name"], inline=False)
        embed.add_field(name="🏫 College", value=result["college"], inline=False)
        embed.add_field(name="📱 Mobile", value=result["mobile"], inline=False)
        embed.add_field(name="🆔 Registration ID", value=result["reg_number"], inline=False)
        embed.add_field(name="🔐 Password", value=result["password"], inline=False)
        embed.set_footer(text="Admin lookup • SWAP 2K25 Event")
        
        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))

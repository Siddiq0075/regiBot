import discord
from discord import app_commands
from discord.ext import commands
from database.db_client import save_registration, get_next_reg_number, users as find_user
from config import LOG_CHANNEL_ID

# Static password
STATIC_PASSWORD = "SWAPJMC"

class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 📝 /register
    @app_commands.command(name="register", description="Register for the event")
    @app_commands.describe(
        name="Your full name",
        partner_name="Your partner's name",
        college="Your college name",
        department="Your department",
        mobile="Your mobile number",
    )
    async def register(self, interaction: discord.Interaction, name: str, partner_name: str, college: str, department: str, mobile: str):
        await interaction.response.defer(ephemeral=True)

        existing = find_user.find_one({"discord_id": interaction.user.id})
        if existing:
            await interaction.followup.send(
                "⚠️ You’re already registered! Use `/view` to see your details.",
                ephemeral=True
            )
            return

        reg_number = get_next_reg_number()
        data = {
            "discord_id": interaction.user.id,
            "name": name,
            "partner_name": partner_name,
            "college": college,
            "department": department,
            "mobile": mobile,
            "reg_number": reg_number,
            "password": STATIC_PASSWORD
        }
        save_registration(data)

        # 🎟️ Fancy DM Embed
        dm_embed = discord.Embed(
            title="🎟️ SWAP 2K25 Registration Ticket",
            description=(
                f"Hey **{name}** 👋\n\n"
                "You're officially registered for the **SWAP 2K25** event!\n"
                "Here’s your digital participant ticket — keep it safe 🔒"
            ),
            color=discord.Color.blurple()
        )
        dm_embed.add_field(name="🆔 Registration ID", value=f"`{reg_number}`", inline=False)
        dm_embed.add_field(name="🔑 Password", value=f"`{STATIC_PASSWORD}`", inline=False)
        dm_embed.add_field(name="👥 Partner", value=partner_name, inline=False)
        dm_embed.add_field(name="🏫 College", value=college, inline=False)
        dm_embed.add_field(name="📱 Mobile", value=mobile, inline=False)
        dm_embed.add_field(name="🏛️ Department", value=department, inline=False)
        dm_embed.set_footer(
            text="✨ SWAP 2K25 | Organized by Jamal Mohamed College"
        )

        # Try sending DM
        try:
            await interaction.user.send(embed=dm_embed)
            await interaction.followup.send(
                f"✅ Registration complete, **{name}**! Your ticket was sent to your DMs. 🎫",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "⚠️ I couldn’t DM you your ticket — please enable **Direct Messages** and use `/resend` to get it again.",
                ephemeral=True
            )
        
        # Log registration
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            log_embed = discord.Embed(
                title="🆕 New Registration Received!",
                description="A new participant has registered for **SWAP 2K25** 🎉",
                color=discord.Color.teal()
            )
            log_embed.add_field(name="SWAP ID", value=f"`{reg_number}`", inline=False)
            log_embed.add_field(name="Name", value=name, inline=False)
            log_embed.add_field(name="Partner", value=partner_name if partner_name else "—", inline=False)
            log_embed.add_field(name="College", value=college, inline=False)
            log_embed.add_field(name="Department", value=department, inline=False)
            log_embed.set_footer(text="📅 SWAP 2K25 | Organized by Jamal Mohamed College")

            await log_channel.send(embed=log_embed)

    # 🔁 /resend (anyone)
    @app_commands.command(name="resend", description="Resend your registration ticket to DM")
    async def resend_dm(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user_data = find_user.find_one({"discord_id": interaction.user.id})

        if not user_data:
            await interaction.followup.send("❌ You’re not registered yet! Use `/register` first.", ephemeral=True)
            return

        # Fancy DM for resend
        dm_embed = discord.Embed(
            title="📩 Your SWAP 2K25 Ticket",
            description="Here’s your registration ticket again — keep it safe and don’t share it. 🔒",
            color=discord.Color.blue()
        )
        dm_embed.add_field(name="🆔 Registration ID", value=f"`{user_data['reg_number']}`", inline=False)
        dm_embed.add_field(name="🔑 Password", value=f"`{user_data['password']}`", inline=False)
        dm_embed.add_field(name="🏫 College", value=user_data["college"], inline=False)
        dm_embed.add_field(name="📱 Mobile", value=user_data["mobile"], inline=False)
        dm_embed.add_field(name="🏛️ Department", value=user_data["department"], inline=False)
        dm_embed.set_footer(
            text="SWAP 2K25 | Jamal Mohamed College — Present this during entry 🎫"
        )

        try:
            await interaction.user.send(embed=dm_embed)
            await interaction.followup.send("✅ Ticket sent to your DM! Check your inbox 📬", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send(
                "⚠️ I still can’t DM you — please enable **Direct Messages** and try again.",
                ephemeral=True
            )

    # 👀 /view
    @app_commands.command(name="view", description="View your registration details")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user_data = find_user.find_one({"discord_id": interaction.user.id})
        if not user_data:
            await interaction.followup.send("❌ You haven’t registered yet! Use `/register` first.", ephemeral=True)
            return

        embed = discord.Embed(
            title="📋 Your Registration Details",
            color=discord.Color.green()
        )
        embed.add_field(name="Name", value=user_data["name"], inline=False)
        embed.add_field(name="Partner", value=user_data["partner_name"], inline=False)
        embed.add_field(name="College", value=user_data["college"], inline=False)
        embed.add_field(name="Mobile", value=user_data["mobile"], inline=False)
        embed.add_field(name="Department", value=user_data["department"], inline=False)
        embed.add_field(name="Registration Number", value=user_data["reg_number"], inline=False)
        embed.add_field(name="Password", value=user_data["password"], inline=False)
        embed.set_footer(text="Keep this information safe for the event!")
        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Registration(bot))

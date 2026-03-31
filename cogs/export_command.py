import discord
from discord import app_commands
from discord.ext import commands
from database.db_client import users as find_user
from openpyxl import Workbook
from datetime import datetime
import io

class ExportCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 📤 /export command (Admin only)
    @app_commands.command(name="export", description="Export all registration data as an Excel file (Admin only)")
    @app_commands.default_permissions(administrator=True)
    async def export_data(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Check admin permissions (extra safeguard)
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send("❌ This command is for admins only.", ephemeral=True)
            return

        # Fetch data
        registrations = list(find_user.find({}, {"_id": 0}))
        if not registrations:
            await interaction.followup.send("ℹ️ No registration data found to export.", ephemeral=True)
            return

        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Registrations"

        # Headers
        headers = ["Registration Number", "Name", "Partner Name", "College", "Department","Mobile"]
        ws.append(headers)

        # Rows
        for reg in registrations:
            ws.append([
                reg.get("reg_number", ""),
                reg.get("name", ""),
                reg.get("partner_name", ""),
                reg.get("college", ""),
                reg.get("department", ""),
                reg.get("mobile", "")
            ])

        # Save Excel file to memory
        file_stream = io.BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        # Create file name with timestamp
        filename = f"registrations_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"

        # Send as ephemeral message
        await interaction.followup.send(
            content=f"✅ Successfully exported **{len(registrations)}** registrations!",
            file=discord.File(file_stream, filename),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(ExportCommand(bot))
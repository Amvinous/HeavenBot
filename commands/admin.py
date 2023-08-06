import discord
from discord import app_commands


class Admin(app_commands.Group):
    @app_commands.command()
    # + Clears commands synced to guild
    async def clear(self, interaction: discord.Interaction):
        if interaction.user.id == 1039558370765574175:
            await interaction.response.send_message('Cleared commands')
            client.tree.clear_commands(guild=interaction.guild)
            await client.tree.sync(guild=interaction.guild)
        else:
            await interaction.response.send_message(content="You're not Ambi", ephemeral=True)

    @app_commands.command()
    # + Command to check if bot globally synced
    async def boop(self, interaction: discord.Interaction):
        await interaction.response.send_message("Boop")


group = Admin(name="admin")

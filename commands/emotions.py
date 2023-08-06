import discord
from discord import app_commands

from queries import emotions


class Emote(app_commands.Group):
    @app_commands.command(description="slap someone")
    async def slap(self, interaction: discord.Interaction, member: discord.Member = None):
        author = interaction.user
        if member is None:
            member = author
        # + Change this for another color
        embed = discord.Embed(colour=0x3B83BD)
        # + Change this for another emotion
        emotion = emotions("slap")

        embed.set_image(url=emotion)
        # + Change value for different message
        embed.add_field(name="\n",
                        value=f'{author.name} slapped {member}')

        await interaction.response.send_message(embed=embed, content=f"{member.mention}")

    @app_commands.command(description="cuddle someone")
    async def cuddle(self, interaction: discord.Interaction, member: discord.Member = None):
        author = interaction.user
        if member is None:
            member = author
        # + Change this for another color
        embed = discord.Embed(colour=0xFAD201)
        # + Change this for another emotion
        emotion = emotions("cuddle")

        embed.set_image(url=emotion)
        # + Change value for different message
        embed.add_field(name="\n",
                        value=f'{author.name} cuddled {member}')

        await interaction.response.send_message(embed=embed, content=f"{member.mention}")

    @app_commands.command(description="hug someone")
    async def hug(self, interaction: discord.Interaction, member: discord.Member = None):
        author = interaction.user
        if member is None:
            member = author
        # + Change this for another color
        embed = discord.Embed(colour=0x1D1E33)
        # + Change this for another emotion
        emotion = emotions("hug")

        embed.set_image(url=emotion)
        # + Change value for different message
        embed.add_field(name="\n",
                        value=f'{author.name} sends wisherprice to {member}')

        await interaction.response.send_message(embed=embed, content=f"{member.mention}")

    @app_commands.command(description="kiss someone")
    async def kiss(self, interaction: discord.Interaction, member: discord.Member = None):
        author = interaction.user
        if member is None:
            member = author
        # + Change this for another color
        embed = discord.Embed(colour=0x20603D)
        # + Change this for another emotion
        emotion = emotions("kiss")

        embed.set_image(url=emotion)
        # + Change value for different message
        embed.add_field(name="\n",
                        value=f'{author.name} gives a kiss to {member}')

        await interaction.response.send_message(embed=embed, content=f"{member.mention}")

    @app_commands.command(description="bully someone")
    async def bully(self, interaction: discord.Interaction, member: discord.Member = None):
        author = interaction.user
        if member is None:
            member = author
        # + Change this for another color
        embed = discord.Embed(colour=0xAF2B1E)
        # + Change this for another emotion
        emotion = emotions("bully")

        embed.set_image(url=emotion)
        # + Change value for different message
        embed.add_field(name="\n",
                        value=f'{author.name} bonked {member}')

        await interaction.response.send_message(embed=embed, content=f"{member.mention}")


group = Emote(name="emote")

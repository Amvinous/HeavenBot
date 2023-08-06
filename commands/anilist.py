import discord
from discord import app_commands

from queries import *


class Anilist(app_commands.Group):
    @app_commands.command(
        name="next",
        description="Gets next episode of an anime")
    async def next_ep(self, interaction: discord.Interaction, anime: str):
        data = get_episode(anime)
        if data["total episodes"] is None:
            data["total episodes"] = "?"

        embed = discord.Embed(
            colour=discord.Colour.blurple())

        embed.set_thumbnail(
            url=data["pic"])

        embed.set_author(
            name=data["title"],
            url=data["anime_url"])

        embed.add_field(
            name=f' Episode: {data["next episode"]}/{data["total episodes"]}\n',
            value=f'<t:{data["unix"]}:F>')
        if data["title"] == "ONE PIECE":
            embed.add_field(name="", inline=True, value="<:gear5:1137738300707328092>")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        description="Gets Schedule of Trending anime")
    async def trending(self, interaction: discord.Interaction):
        data = get_trending()
        embed = discord.Embed(
            colour=discord.Colour.green())
        for anime in data:
            embed.add_field(
                name=f' {anime["title"]} : {anime["next episode"]}\n',
                value=f'<t:{anime["unix"]}>')

        await interaction.response.send_message(embed=embed)


group = Anilist(name="anilist")

import os
import random

import discord
from discord import app_commands
from dotenv import load_dotenv

from Next_Ep import get_episode

load_dotenv()

MY_GUILD = discord.Object(id=1110874535156269157)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


def flip():
    coin = random.choice(["Heads", "Tails"])
    return coin


client = MyClient(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'logged in as {client.user}')
    print('-------------------')


@client.tree.command()
async def coin(interaction: discord.Interaction):
    """Flips a coin"""
    coin = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(coin)


@client.tree.command()
async def clear_commands(interaction: discord.Interaction):
    if interaction.user.id == 1039558370765574175:
        await interaction.response.send_message('Settings run')
        client.tree.clear_commands(guild=interaction.guild)
        await client.tree.sync(guild=interaction.guild)
    else:
        await interaction.response.send_message('Not Owner')


@client.tree.command()
async def dice(interaction: discord.Interaction):
    """Rolls a dice"""
    dice = random.randint(1, 6)
    await interaction.response.send_message(dice)


@client.tree.command()
async def next_ep(interaction: discord.Interaction, anime: str):
    """Gets next episode of an anime"""
    data = get_episode(anime)
    if data["total episodes"] is None:
        data["total episodes"] = "?"

    embed = discord.Embed(colour=discord.Colour.blurple(), type="rich")
    embed.set_thumbnail(url=data["pic"])
    embed.set_author(name=data["title"], url=data["anime_url"])

    embed.add_field(name=f' Episode: {data["next episode"]}/{data["total episodes"]}\n',
                    value=f'<t:{data["unix"]}:F>')
    await interaction.response.send_message(embed=embed)


def run_bot():
    client.run(os.getenv("TOKEN"))

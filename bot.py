import os
import random

import discord
from discord import app_commands
from dotenv import load_dotenv

from next_ep import get_episode
from trending import get_trending

load_dotenv()
# + test
MY_GUILD = discord.Object(id=1110874535156269157)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'logged in as {client.user}')
    print('-------------------')


@client.tree.command()
async def settings(interaction: discord.Interaction):
    await interaction.response.send_message('Settings run')
    client.tree.clear_commands(guild=interaction.guild)
    await client.tree.sync(guild=interaction.guild)


@client.tree.command(description="Flips a coin")
async def coin(interaction: discord.Interaction):
    coin = random.choice(["<:Heads:1134851517845884950>", "<:Tails:1134851515954241659>"])
    await interaction.response.send_message(coin)


@client.tree.command(description="Rolls a dice")
@app_commands.describe(amount="Amount of dice you want to roll", sides="Amount of Sides you want dice to have")
async def dice(interaction: discord.Interaction, amount: app_commands.Range[int, 0, 24] = 1, sides: int = 6):
    embed = discord.Embed(title="Rolling Dice <:yumeko:1135112795810181140>", colour=0xe00b79)
    dice_sum = 0
    for _ in range(amount):
        dice = random.randint(1, sides)
        embed.add_field(name=f'd{sides}: {dice}', value=f'Rolled: {dice}')
        dice_sum += dice
    embed.set_footer(text=f'Sum: {dice_sum}')
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="next", description="Gets next episode of an anime")
async def next_ep(interaction: discord.Interaction, anime: str):
    data = get_episode(anime)
    if data["total episodes"] is None:
        data["total episodes"] = "?"

    embed = discord.Embed(colour=discord.Colour.blurple())
    embed.set_thumbnail(url=data["pic"])
    embed.set_author(name=data["title"], url=data["anime_url"])

    embed.add_field(name=f' Episode: {data["next episode"]}/{data["total episodes"]}\n',
                    value=f'<t:{data["unix"]}:F>')
    await interaction.response.send_message(embed=embed)


@client.tree.command(description="Gets Schedule of Trending anime")
async def trending(interaction: discord.Interaction):
    data = get_trending()
    embed = discord.Embed(colour=discord.Colour.green(), type="rich")
    for anime in data:
        embed.add_field(name=f' {anime["title"]} : {anime["next episode"]}\n',
                        value=f'<t:{anime["unix"]}>')
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="sticker", description="Gets Sticker from message ID")
async def sticker(interaction: discord.Interaction, message_id: str):
    channel = interaction.channel
    message_content = await channel.fetch_message(int(message_id))
    embed = discord.Embed(colour=discord.Colour.red(), type="image")
    if message_content.stickers:
        for pic in message_content.stickers:
            sticker = pic.url
            embed.set_image(url=sticker)
    await interaction.response.send_message(embed=embed)


def run_bot():
    client.run(os.getenv("TOKEN"))

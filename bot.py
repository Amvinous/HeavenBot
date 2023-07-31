import os
import random

# ? Discord
import discord
from discord import app_commands
from dotenv import load_dotenv

# ? My modules
from queries import *

# + Test Guild/My Server
MY_GUILD = discord.Object(id=465894931139919883)  # 1110874535156269157)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        await self.tree.sync()


intents = discord.Intents.default()
# + Overwrites `self.tree` and `self.setup_hook()`
client = MyClient(intents=intents)


@client.event
# + Prints on Boot
async def on_ready():
    print(f'logged in as {client.user}')
    print('-------------------')


@client.tree.command()
# + Clears commands synced to guild
async def clear(interaction: discord.Interaction):
    if interaction.user.id == 1039558370765574175:
        await interaction.response.send_message('Cleared commands')
        client.tree.clear_commands(guild=interaction.guild)
        await client.tree.sync(guild=interaction.guild)
    else:
        await interaction.response.send_message(content="You're not Ambi", ephemeral=True)


@client.tree.command()
# + Command to check if bot globally synced
async def boop(interaction: discord.Interaction):
    await interaction.response.send_message("Boop")


@client.tree.command(
    description="Flips a coin")
async def coin(interaction: discord.Interaction):
    coin = random.choice(
        ["<:Heads:1134851517845884950>",
         "<:Tails:1134851515954241659>"])

    await interaction.response.send_message(coin)


@client.tree.command(
    description="Rolls a dice")
@app_commands.describe(
    amount="Amount of dice you want to roll",
    sides="Amount of Sides you want dice to have")
async def dice(interaction: discord.Interaction,
               amount: app_commands.Range[int, 0, 24] = 1,
               sides: app_commands.Range[int, 0] = 6):
    embed = discord.Embed(
        title="Rolling Dice <:yumeko:1135112795810181140>",
        colour=0xe00b79)
    dice_sum = 0

    for _ in range(amount):
        dice = random.randint(1, sides)
        embed.add_field(
            name=f'd{sides}: {dice}',
            value=f'Rolled: {dice}')
        dice_sum += dice

    embed.set_footer(
        text=f'Sum: {dice_sum}')

    await interaction.response.send_message(embed=embed)


@client.tree.command(
    name="next",
    description="Gets next episode of an anime")
async def next_ep(interaction: discord.Interaction, anime: str):
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

    await interaction.response.send_message(embed=embed)


@client.tree.command(
    description="Gets Schedule of Trending anime")
async def trending(interaction: discord.Interaction):
    data = get_trending()
    embed = discord.Embed(
        colour=discord.Colour.green())
    for anime in data:
        embed.add_field(
            name=f' {anime["title"]} : {anime["next episode"]}\n',
            value=f'<t:{anime["unix"]}>')

    await interaction.response.send_message(embed=embed)


@client.tree.command(
    name="sticker",
    description="Gets Sticker from message ID")
@app_commands.rename(message_id="id")
async def sticker(interaction: discord.Interaction, message_id: str):
    message_content = await interaction.channel.fetch_message(int(message_id))

    embed = discord.Embed(
        colour=discord.Colour.red(),
        type="image")

    if message_content.stickers:
        for pic in message_content.stickers:
            sticker = pic.url

            embed.set_image(
                url=sticker)

    await interaction.response.send_message(embed=embed)


@client.tree.command()
async def slap(interaction: discord.Interaction, member: discord.Member = None):
    # + Change this for another emotion
    emotion = emotions("slap")
    # + Change this for another color
    embed = discord.Embed(colour=0xFFFFFF)
    author = interaction.user

    if member is None:
        member = author

    embed.set_image(url=emotion)
    # + Change value for different message
    embed.add_field(name="\n",
                    value=f'{author.name} slapped {member}')

    await interaction.response.send_message(embed=embed, content=f"{member.mention}")


@client.tree.command()
async def hug(interaction: discord.Interaction, member: discord.Member = None):
    # + Change this for another emotion
    emotion = emotions("hug")
    # + Change this for another color
    embed = discord.Embed(colour=0xFFFFFF)
    author = interaction.user

    if member is None:
        member = author

    embed.set_image(url=emotion)
    # + Change value for different message
    embed.add_field(name="\n",
                    value=f'{author.name} hugged {member}')

    await interaction.response.send_message(embed=embed, content=f"{member.mention}")


@client.tree.command()
async def kiss(interaction: discord.Interaction, member: discord.Member = None):
    # + Change this for another emotion
    emotion = emotions("kiss")
    # + Change this for another color
    embed = discord.Embed(colour=0xFFFFFF)
    author = interaction.user

    if member is None:
        member = author

    embed.set_image(url=emotion)
    # + Change value for different message
    embed.add_field(name="\n",
                    value=f'{author.name} kissed {member}')

    await interaction.response.send_message(embed=embed, content=f"{member.mention}")


@client.tree.command(nsfw=True)
async def quickie(interaction: discord.Interaction, member: discord.Member = None):
    # + Change this for another emotion
    emotion = emotions("blowjob", "nsfw")
    # + Change this for another color
    embed = discord.Embed(colour=0xFFFFFF)
    author = interaction.user

    if member is None:
        member = author

    embed.set_image(url=emotion)
    # + Change value for different message
    embed.add_field(name="\n",
                    value=f'{author.name} gave {member} a quickie')

    await interaction.response.send_message(embed=embed, content=f"{member.mention}")


load_dotenv()


def run_bot():
    client.run(os.getenv("TOKEN"))

# * Discord
import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from commands.anilist import Anilist
# * My modules
from commands.emotions import Emote
from commands.throw import Throw


# + Overwrites `self.tree` and `self.setup_hook()`
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # self.tree.copy_global_to(guild=MY_GUILD)
        for group in groups:
            self.tree.add_command(group)
        await self.tree.sync(guild=MY_GUILD)
        await self.tree.sync()


MY_GUILD = discord.Object(id=1110874535156269157)

intents = discord.Intents.default()

client = MyClient(intents=intents)

# + Additional commands from other files

groups = (
    Emote(name="emote"),
    Throw(name="throw"),
    Anilist(name="anilist")
)


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


load_dotenv()


def run_bot():
    client.run(os.getenv("TOKEN"))

import importlib
import os
import pathlib

import discord
from discord import app_commands
from dotenv import load_dotenv


# * My modules

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


# + Define variables
MY_GUILD = discord.Object(id=1110874535156269157)
intents = discord.Intents.default()
client = MyClient(intents=intents)
cmd_path = pathlib.Path("commands")
groups = []
# + populate groups list with subcommands
for module_file in cmd_path.iterdir():
    module_file = module_file.name
    if module_file.endswith(".py"):
        module_name = module_file[:-3]
        module = importlib.import_module(f"{cmd_path.name}.{module_name}")
        groups += (module.group,)


@client.event
# + Prints on Boot
async def on_ready():
    print(f'logged in as {client.user}')
    print('-----------------------------')


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


# + load token from .env
load_dotenv()


def run_bot():
    client.run(os.getenv("TOKEN"))

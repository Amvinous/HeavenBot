import discord
from discord import app_commands


class Throw(app_commands.Group):
    @app_commands.command(
        description="Flips a coin")
    async def coin(self, interaction: discord.Interaction):
        coin = random.choice(
            ["<:Heads:1134851517845884950>",
             "<:Tails:1134851515954241659>"])

        await interaction.response.send_message(coin)

    @app_commands.command(
        description="Rolls a dice")
    @app_commands.describe(
        amount="Amount of dice you want to roll",
        sides="Amount of Sides you want dice to have")
    async def dice(self, interaction: discord.Interaction,
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


group = Throw(name="throw")

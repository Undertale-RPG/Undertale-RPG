import disnake
import requests
from disnake.ext import commands

from main import UndertaleBot
from utility.constants import BLUE
from utility.utils import ConsoleColors


class Errors(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandOnCooldown):
            embed = disnake.Embed(
                title="This command is on cooldown!",
                description=f"Try again in **{error.retry_after:.2f}** seconds",
                color=BLUE,
            )
            return await inter.send(embed=embed, ephemeral=True)

        url = self.bot.error_webhook

        if url is None:
            raise error

        embed = {
            "description": f"{error}",
            "title": "An error has occurred",
            "color": BLUE,
            "timestamp": "",
        }

        data = {"embeds": [embed]}
        result = requests.post(url, json=data)
        if 200 <= result.status_code < 300:
            print(f"Webhook sent {result.status_code}")
        else:
            print(
                f"{ConsoleColors.WARNING}Not sent with {result.status_code}, response:\n{result.json()}"
            )


def setup(bot: UndertaleBot):
    bot.add_cog(Errors(bot))

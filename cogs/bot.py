from disnake import Interaction
from disnake.ext import commands

class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="ping, pong")
    async def ping(self, inter):
        """Latency check for stability"""
        await inter.send(f"pong! **{round(self.bot.latency * 1000)}ms**")


def setup(bot):
    bot.add_cog(Bot(bot))
from email import utils
import disnake
from disnake.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.slash_command()
    async def test(self, inter):
        await inter.send("test")

def setup(bot):
    bot.add_cog(Test(bot))

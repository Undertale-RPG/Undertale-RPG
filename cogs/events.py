from disnake.ext import commands

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("im ready!!!!!!")


def setup(bot):
    bot.add_cog(Event(bot))
from disnake.ext import commands, tasks
from utility.dataIO import fileIO

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("im ready!!!!!!")

    @tasks.loop(seconds=5)
    async def data_task(self):
        #self.bot.items = fileIO("data/items/items.json", "load")
        #self.bot.monsters = fileIO("data/stats/monsters.json", "load")
        #self.bot.locations = fileIO("data/traveling.json", "load")
        self.bot.crates = fileIO("data/crates.json", "load")
        #self.bot.shopping = fileIO("data/shops.json", "load")
        self.bot.boosters = await self.bot.db["boosters"].find_one({"_id": 0})
        self.bot.levels = fileIO("data/levels.json", "load")


def setup(bot):
    bot.add_cog(Event(bot))
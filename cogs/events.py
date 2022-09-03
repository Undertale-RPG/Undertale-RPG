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
        #self.bot.monsters = fileIO("data/monsters.json", "load")
        self.bot.locations = fileIO("data/locations.json", "load")
        #self.bot.crates = fileIO("data/crates.json", "load")
        #self.bot.shopping = fileIO("data/shops.json", "load")
        self.bot.boosters = await self.bot.db["boosters"].find_one({"_id": 0})
        self.bot.levels = fileIO("data/levels.json", "load")
        self.bot.bosses = fileIO("data/bosses.json", "load")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(
                    "Hello!, Thanks for adding me! You can use the command **/tutorial** To "
                    "know how the bot works!")
                break

def setup(bot):
    bot.add_cog(Event(bot))
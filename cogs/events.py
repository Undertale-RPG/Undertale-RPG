import disnake
from disnake.ext import commands, tasks

from main import UndertaleBot
from utility.dataIO import fileIO
from utility.utils import ConsoleColors


class Event(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot
        self.data_task.start()

    @commands.Cog.listener()
    async def on_ready(self):
        # await self.bot.players.update_many({}, { "$rename": { "standard crate": "standard-crate", "determination crate": "determination-crate", "soul crate": "soul-crate", "void crate": "void-crate", "event crate": "event-crate" } })
        player_count = await self.bot.players.count_documents({})
        print(
            f"{ConsoleColors.GREEN}logged in as {self.bot.user}\nguilds: {len(self.bot.guilds)}\nplayers: {player_count}{ConsoleColors.ENDC}"
        )


    @tasks.loop(seconds=5)
    async def data_task(self):
        self.bot.items = fileIO("data/items/items.json", "load")
        self.bot.monsters = fileIO("data/stats/monsters.json", "load")
        self.bot.locations = fileIO("data/traveling.json", "load")
        self.bot.crates = fileIO("data/crates.json", "load")
        self.bot.shopping = fileIO("data/shops.json", "load")
        self.bot.boosters = await self.bot.db["boosters"].find_one({"_id": 0})
        self.bot.levels = fileIO("data/levels.json", "load")

def setup(bot: UndertaleBot):
    bot.add_cog(Event(bot))

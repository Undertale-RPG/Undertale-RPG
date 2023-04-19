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
        print(
            f"{ConsoleColors.GREEN}logged in as {self.bot.user}\nguilds: {len(self.bot.guilds)}{ConsoleColors.ENDC}"
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

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        print(f'{ConsoleColors.CYAN}➕Joined "{guild.name}"')
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(
                    "Hello!, Thanks for adding me! You can use the **/help** and **/tutorial** To learn how the bot works!"
                )
                break


def setup(bot: UndertaleBot):
    bot.add_cog(Event(bot))

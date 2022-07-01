import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from utility.utils import ConsoleColors

load_dotenv()

DEFAULT_DISABLED_MESSAGE = (
    "The bot is currently disabled for an update or an refresh is happening, please. "
    "wait until its back up, you can join our support server to get notified once its backup."
)


async def is_enabled(ctx):
    if ctx.author.id not in ctx.bot.owner_ids:
        if ctx.bot.ENABLED:
            return True

        await ctx.send(DEFAULT_DISABLED_MESSAGE)
        return False
    return True

class UndertaleBot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guilds_db = None
        self.players = None
        self.cluster = None
        self.db = None
        self.players = None
        self.boosters = []
        self.db = None
        self.cluster = None
        self.shopping = None
        self.BotToken = os.getenv("TOKEN")
        self.TopGGToken = os.getenv("TOPGG_TOKEN")
        self.MongoUrl = os.getenv("MONGO_URL")
        self.log_channel = os.getenv("LOG_CHANNEL")
        self.invite_url = "https://discord.gg/FQYVpuNz4Q"
        self.vote_url = "https://top.gg/bot/815153881217892372"
        self.patreon_link = "https://www.patreon.com/undertale_rpg"
        self.currency = "<:doge_coin:864929485295321110>"
        self.add_check(is_enabled)
        self.activity = disnake.Game("Undertale | u?help ")
        self.ENABLED = False
        self.help_command = None
        self.events = None
        self.fights = {}
        self.shops = {}
        self.duels = {}

    async def on_shard_connect(self, shard):
        print(
            f"----------Shard {shard} is on.-------------\n"
            f"Total Guilds: {len(self.guilds)}\n"
            f"Total Shards: {len(self.shards)}\n"
            f"------------------------------------------"
        )

    def load_all_cogs(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                self.load_extension(f"cogs.{filename[:-3]}")
                print(f"🔁 {ConsoleColors.GREEN}{ConsoleColors.BOLD}cogs.{filename[:-3]} is loaded and ready.{ConsoleColors.ENDC}")
        self.ENABLED = True
        return

    def db_load(self):
        self.cluster = AsyncIOMotorClient(self.MongoUrl)
        self.db = self.cluster["database"]
        self.players = self.db["players"]
        self.guilds_db = self.db["guilds"]
        self.boosters = self.db["boosters"]
        print("Database connection established")
        print("db_load task finished")
        return


bot = UndertaleBot(
    command_prefix=os.getenv("PREFIX"),
    owner_ids=[536538183555481601, 513351917481623572],
    intents=disnake.Intents.all()
)

bot.db_load()
bot.load_all_cogs()
bot.load_extension("jishaku")

bot.run(bot.BotToken)

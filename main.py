import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

description = """The undertale RPG Beta bot."""

intents = disnake.Intents.none()
intents.members = False
intents.message_content = False

class UndertaleBot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BotToken = os.getenv("TOKEN")
        self.invite_url = "https://discord.gg/FQYVpuNz4Q"
        self.vote_url = "https://top.gg/bot/815153881217892372"
        self.patreon_link = "https://www.patreon.com/undertaleRPG"
        self.currency = ":coin:"
        self.activity = disnake.Game("Undertale | /help ")
        self.help_command = None
        self.MongoUrl = os.getenv("MONGO_URL")
        self.cluster = AsyncIOMotorClient(self.MongoUrl)
        self.guilds_db = None
        self.players = None
        self.db = None
        self.boosters = None
        self.shopping = None
        self.fights = {}

    async def on_shard_connect(self, shard):
        print(
            f"----------Shard {shard} is on.-------------\n"
            f"Total Guilds: {len(self.guilds)}\n"
            f"Total Shards: {len(self.shards)}\n"
            f"-------------------------------------------"
        )

    def load_all_cogs(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                self.load_extension(f"cogs.{filename[:-3]}")
                print(f"🔁 cogs.{filename[:-3]} is loaded and ready.")
        return

    def db_load(self):
        self.cluster = AsyncIOMotorClient(self.MongoUrl)
        self.db = self.cluster["database"]
        self.players = self.db["players"]
        self.guilds_db = self.db["guilds"]
        self.boosters = self.db["boosters"]
        print("the database has loaded")
        return


bot = UndertaleBot(
    description=description,
    intents=intents,
    owner_ids=[536538183555481601, 513351917481623572]
)

bot.db_load()
bot.load_all_cogs()
bot.run(bot.BotToken)
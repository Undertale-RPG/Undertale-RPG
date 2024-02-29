import os
from typing import Dict

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from utility.utils import ConsoleColors

# Constants for URLs
INVITE_URL = "https://discord.gg/FQYVpuNz4Q"
VOTE_URL = "https://top.gg/bot/748868577150369852/vote"
WEBSITE = "https://undertalerpg.monster/"
PATREON_LINK = "https://www.patreon.com/undertaleRPG"

load_dotenv()

description = """The undertale RPG bot."""

intents = disnake.Intents.none()
intents.members = False
intents.message_content = False


class UndertaleBot(commands.AutoShardedInteractionBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BotToken = os.getenv("TOKEN")
        self.invite_url = INVITE_URL
        self.vote_url = VOTE_URL
        self.website = WEBSITE
        self.patreon_link = PATREON_LINK
        self.currency = ":coin:"
        self.activity = disnake.Game("Undertale | /help ")
        self.help_command = None
        self.MongoUrl = os.getenv("MONGO_URL")
        self.error_webhook = os.getenv("ERROR_WEBHOOK")
        self.cluster = AsyncIOMotorClient(self.MongoUrl)
        self.players = None
        self.consumables = None
        self.armor = None
        self.weapons = None
        self.db = None
        self.boosters = None
        self.data = None

    async def on_shard_connect(self, shard):
        print(
            f"{ConsoleColors.CYAN}---------- {ConsoleColors.GREEN}Shard {shard} is on {ConsoleColors.CYAN}-------------\n"
            f"{ConsoleColors.GREEN}Total Guilds: {len(self.guilds)}\n"
            f"{ConsoleColors.GREEN}Total Shards: {len(self.shards)}\n"
            f"{ConsoleColors.CYAN}--------------------------------------{ConsoleColors.ENDC}"
        )

    def load_all_cogs(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                self.load_extension(f"cogs.{filename[:-3]}")
                print(
                    f"{ConsoleColors.GREEN}🔁 cogs.{filename[:-3]} is loaded and ready."
                )
        return

    def db_load(self):
        self.cluster = AsyncIOMotorClient(self.MongoUrl)
        self.db = self.cluster["database"]
        self.consumables = self.db["consumables"]
        self.armor = self.db["armor"]
        self.weapons = self.db["weapons"]
        self.players = self.db["players"]
        self.guilds_db = self.db["guilds"]
        self.boosters = self.db["boosters"]
        self.data = self.db["data"]
        print(f"{ConsoleColors.GREEN}✅ the database has loaded test test")
        return


bot = UndertaleBot(intents=intents, owner_ids=[536538183555481601])

bot.db_load()
bot.load_all_cogs()
bot.run(bot.BotToken)

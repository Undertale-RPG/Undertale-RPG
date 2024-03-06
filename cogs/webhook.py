import time

import topgg
from topgg.types import BotVoteData
from disnake.ext import commands

from main import UndertaleBot


class TopGG(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot
        self.topggpy = topgg.WebhookManager(bot).dbl_webhook()
        self.topggpy.run(55566)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data: BotVoteData):
        print("this is the real thing it works!")

        voter = await self.bot.fetch_user(data["user"])

        if await self.bot.players.find_one({"_id": voter.id}) is None:
            return

        await self.bot.players.update_one(
            {"_id": voter.id},
            {"$inc": {"gold": 300, "standard crate": 1}, "$set": {"last_voted": round(time.time())}}
        )

        print(f"Received a vote from {str(voter.id)}, They got their rewards successfully")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print("this is a test it works!")

        voter = await self.bot.fetch_user(data["user"])

        if await self.bot.players.find_one({"_id": voter.id}) is None:
            return

        await self.bot.players.update_one(
            {"_id": voter.id},
            {"$inc": {"gold": 300, "standard crate": 1}, "$set": {"last_voted": round(time.time())}}
        )

        print(f"Received a vote from {str(voter.id)}, They got their rewards successfully")


def setup(bot: UndertaleBot):
    bot.add_cog(TopGG(bot))

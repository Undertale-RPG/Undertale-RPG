import time

import topgg
from topgg.types import BotVoteData
from disnake.ext import commands

from main import UndertaleBot


class TopGG(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot
        self.topggpy = topgg.WebhookManager(bot).dbl_webhook(auth_key=bot.top_gg_auth)
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

        print(f"Received a vote from {str(voter)}, They got their rewards successfully")

        cha = self.bot.get_channel(1010596574155522078)
        await cha.send(content=f"{str(voter)} voted.")

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

        print(f"Received a vote from {str(voter)}, They got their rewards successfully")

        cha = self.bot.get_channel(1010596574155522078)
        await cha.send(content=f"{str(voter)} voted.")


def setup(bot: UndertaleBot):
    bot.add_cog(TopGG(bot))

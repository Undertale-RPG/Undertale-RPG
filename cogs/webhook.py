import time

import topgg
from disnake.ext import commands
from utility.utils import ConsoleColors


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.topggpy = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "dady2005")
        bot.topggpy.run(55111)
        self.cmds = []

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print("this is the real thing it works!")
        #vote_data = data
        #voter = await self.bot.fetch_user(vote_data["user"])
        #info = await self.bot.players.find_one({"_id": voter.id})
        #if info is None:
        #    print(f"{ConsoleColors.WARNING} This user is not registered.{ConsoleColors.ENDC}")
        #    return
        #info["gold"] = info["gold"] + 300
        #info["standard crate"] += 1
        #info["last_voted"] = time.time()
#        #await self.bot.players.update_one({"_id": voter.id}, {"$set": info})
        #print(f"{ConsoleColors.GREEN}Received a vote from {str(voter)}, They got their rewards successfully{ConsoleColors.ENDC}")

        #cha = self.bot.get_channel(1010596574155522078)
        #await cha.send(content=f"someone voted")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print("this is a test it works!")
        #vote_data = data
        #voter = await self.bot.fetch_user(vote_data["user"])
        #info = await self.bot.players.find_one({"_id": voter.id})
        #info["gold"] = info["gold"] + 500
        #info["standard crate"] += 1
        ##await self.bot.players.update_one({"_id": voter.id}, {"$set": info})
        #print(f"{ConsoleColors.GREEN}Received a vote from {str(voter)}, They got their rewards successfully{ConsoleColors.ENDC}")
#
        #cha = self.bot.get_channel(1010596574155522078)
        #await cha.send(content=f"someone voted!!")

def setup(bot):
    bot.add_cog(TopGG(bot))
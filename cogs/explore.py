from disnake import Interaction
from disnake.ext import commands
import random

class Explore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="explore to find monsters, xp, gold and items")
    async def explore(self, inter):
        """Explore and fine all kinds of monsters and treasure!"""

        choices = ["fight", "gold", "crate", "puzzle"]
        item = random.choices(choices, weights=(70, 20, 10, 30), k=1)

        data = await inter.bot.players.find_one({"_id": inter.author.id})

        if item[0] == "fight":
            await inter.send("the monsters do not feel like fighting rn")
            return
        
        if item[0] == "gold":
            found_gold = random.randint(150, 250)
            new_gold = data["gold"] + found_gold
            data["gold"] += found_gold
            await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
            await inter.send(f"You found `{found_gold}`**G**! you now have `{new_gold}`**G**")
            return
        
        if item[0] == "crate":
            data["determination crate"] += 1
            await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
            await inter.send("You found `1` Determination crate! you can open it with `/crates`")
            return

        if item[0] == "puzzle":
            await inter.send("coming soon!")
            return



def setup(bot):
    bot.add_cog(Explore(bot))
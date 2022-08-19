from disnake import Interaction
from disnake.ext import commands
import random

class Explore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="explore to find monsters, xp, gold and items")
    async def explore(self, inter):
        """Explore and fine all kinds of monsters and treasure!"""

        choices = ["fight", "gold", "food", "puzzle"]
        item = random.choices(choices, weights=(55, 20, 10, 30), k=1)

        if item[0] == "fight":
            await inter.send("the monsters do not feel like fighting rn")
            return
        
        if item[0] == "gold":
            await inter.send("You found gold!")
            return
        
        if item[0] == "food":
            await inter.send("here have some food")
            return

        if item[0] == "puzzle":
            await inter.send("coming soon!")
            return



def setup(bot):
    bot.add_cog(Explore(bot))
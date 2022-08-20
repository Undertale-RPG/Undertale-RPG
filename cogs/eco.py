import re
from disnake.ext import commands
import disnake

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def stats(self, inter):
        """Check your stats and powers"""
        player = inter.author
        if player.bot:
            await inter.send("Nice try!")
            return
        data = await inter.bot.players.find_one({"_id": inter.author.id})

        health = data["health"]
        love = data["level"]
        exp = data["exp"]
        kills = data["kills"]
        deaths = data["deaths"]
        weapon = data["weapon"]
        armor = data["armor"]
        gold = data["gold"]
        tokens = data["tokens"]
        resets = data["resets"]
        multi_g = data["multi_g"] 
        multi_xp = data["multi_xp"]

        em = disnake.Embed(
            title = f"{player}'s stats",
            color = 0x0077ff,
            description = "Your Status and progress in the game"
        )
        em.set_thumbnail(url=player.display_avatar)
        em.add_field(name="▫️┃Health", value=f"{health}")
        em.add_field(name="▫️┃LOVE", value=f"{love}")
        em.add_field(name="▫️┃EXP", value=f"{exp}")
        em.add_field(name="▫️┃Kills", value=f"{kills}")
        em.add_field(name="▫️┃Deaths", value=f"{deaths}")
        em.add_field(name="▫️┃Weapon", value=f"{weapon}")
        em.add_field(name="▫️┃Armor", value=f"{armor}")
        em.add_field(name="▫️┃Gold", value=f"{gold}")
        em.add_field(name="▫️┃Tokens", value=f"{tokens}")
        em.add_field(name="▫️┃resets", value=f"{resets}")
        em.add_field(name="▫️┃Gold Multiplier", value=f"{multi_g}")
        em.add_field(name="▫️┃EXP Multiplier", value=f"{multi_xp}")

        await inter.send(inter.author.mention, embed=em)


def setup(bot):
    bot.add_cog(Economy(bot))
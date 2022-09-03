import re
from xml.etree.ElementTree import tostring
from disnake.ext import commands
import disnake
from utility.utils import create_player_info
import time

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
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

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def booster(self, inter):
        """Claim Your daily booster Reward!"""
        author = inter.author
        data = await self.bot.players.find_one({"_id": author.id})
        boosters = await self.bot.db["boosters"].find_one({"_id": 0})
        await create_player_info(inter, inter.author)

        if author.id not in boosters["boosters"]:
            await inter.send(
                "You are not a booster!, only people who boost our support server are able to get the rewards!")
            return
       
        new_gold = 2500 * data["multi_g"]
        curr_time = time.time()
        delta = int(curr_time) - int(int(data["booster_block"]))

        if delta >= 86400:
            data["gold"] += new_gold
            data["booster_block"]= curr_time
            await self.bot.players.update_one({"_id": author.id}, {"$set": data})
            await inter.send(f"**You recieved your booster gold! {int(new_gold)} G**")
        else:
            seconds = 86400 - delta
            em = disnake.Embed(
                description=(
                    f"**You can't claim your booster reward yet!\n\nYou can claim your booster reward"
                    f" <t:{int(time.time()) + int(seconds)}:R>**"),
                color=0x0077ff,
            )

        await inter.send(embed=em)

def setup(bot):
    bot.add_cog(Economy(bot))
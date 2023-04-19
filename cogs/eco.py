import random
import time

import disnake
from disnake.ext import commands

from main import UndertaleBot
from utility.constants import BLUE
from utility.utils import create_player_info


class Economy(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot

    @commands.slash_command(
        description="Get your supporter reward for being in our support server."
    )
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def supporter(self, inter: disnake.ApplicationCommandInteraction):
        """Get your supporter reward for being in our support server."""
        await create_player_info(inter, inter.author)
        if inter.guild.id != 817437132397871135:
            return await inter.send(
                "this command is exclusive for our support server, you can join via \n\n https://discord.gg/FQYVpuNz4Q",
                ephemeral=True,
            )

        info = await self.bot.players.find_one({"_id": inter.author.id})
        gold_amount = random.randint(200, 500) * info["multi_g"]
        try:
            current_time = time.time()
            delta = int(current_time) - int(info["supporter_block"])

            if delta >= 86400 and delta > 0:
                info["gold"] += gold_amount
                info["supporter_block"] = current_time
                await self.bot.players.update_one(
                    {"_id": inter.author.id}, {"$set": info}
                )
                embed = disnake.Embed(
                    description=f"**You received your supporter gold! {int(gold_amount)} G**",
                    color=BLUE,
                )
            else:
                seconds = 86400 - delta
                embed = disnake.Embed(
                    description=(
                        f"**You can't claim your supporter reward yet!\n\n You can use this command again"
                        f" <t:{int(time.time()) + int(seconds)}:R>**"
                    ),
                    color=BLUE,
                )
            await inter.send(embed=embed)
        except KeyError:
            info["supporter_block"] = 0
            await self.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

    @commands.slash_command(description="Check your balance or other people's ones.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def gold(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.User = None,
    ):
        """Check your gold and progress"""
        player = member or inter.author

        if player.bot:
            return await inter.send("Nice try!", ephemeral=True)

        await create_player_info(inter, player)

        data = await self.bot.players.find_one({"_id": player.id})
        gold = data["gold"]

        embed = disnake.Embed(
            title="Balance",
            color=BLUE,
            description=f"{player.name}'s balance\n**{round(gold)}G**",
        )
        await inter.send(embed=embed)

    @commands.slash_command(description="Check your Statistics or other people's ones.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def stats(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.User = None,
    ):
        """Check your stats and progress"""
        player = member or inter.author
        if player.bot:
            await inter.send("Nice try!")
            return

        await create_player_info(inter, player)

        data = await self.bot.players.find_one({"_id": player.id})

        health = data["health"]
        love = data["level"]
        exp = data["exp"]
        exp_lvl_up = love * 100 / 0.4
        kills = data["kills"]
        deaths = data["deaths"]
        spares = data["spares"]
        gold = data["gold"]
        weapon = data["weapon"]
        armor = data["armor"]
        resets = data["resets"]
        multi_g = data["multi_g"]
        multi_xp = data["multi_xp"]
        max_health = love * 2 / 0.5 + 20
        atk = data["attack"]
        deff = data["defence"]

        embed = disnake.Embed(
            title=f"{player}'s stats",
            color=BLUE,
            description="Status and progress in the game.",
        )
        embed.set_thumbnail(url=player.display_avatar)
        embed.add_field(name="▫️┃Health", value=f"{round(health)}/{round(max_health)}")
        embed.add_field(name="▫️┃LOVE", value=f"{round(love)}")
        embed.add_field(name="▫️┃EXP", value=f"{round(exp)}/{round(exp_lvl_up)}")
        embed.add_field(name="▫️┃Kills", value=f"{round(kills)}")
        embed.add_field(name="▫️┃Deaths", value=f"{round(deaths)}")
        embed.add_field(name="▫️┃Spares", value=f"{round(spares)}")
        embed.add_field(name="▫️┃Gold", value=f"{round(gold)}")
        embed.add_field(name="▫️┃Weapon", value=f"{weapon}")
        embed.add_field(name="▫️┃Armor", value=f"{armor}")
        embed.add_field(name="▫️┃Resets", value=f"{round(resets)}")
        embed.add_field(name="▫️┃Gold Multiplier", value=f"{round(multi_g)}")
        embed.add_field(name="▫️┃EXP Multiplier", value=f"{round(multi_xp)}")
        embed.add_field(name="▫️┃Attack", value=f"{round(atk)}")
        embed.add_field(name="▫️┃Defence", value=f"{round(deff)}")

        await inter.send(inter.author.mention, embed=embed)

    @commands.slash_command(description="Claim your booster rewards.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def booster(self, inter: disnake.ApplicationCommandInteraction):
        """Claim Your daily booster Reward!"""
        await create_player_info(inter, inter.author)
        author = inter.author
        data = await self.bot.players.find_one({"_id": author.id})
        boosters = await self.bot.db["boosters"].find_one({"_id": 0})
        await create_player_info(inter, inter.author)

        if author.id not in boosters["boosters"]:
            return await inter.send(
                "You are not a booster!, only people who boost our support server are able to get the rewards!"
            )

        new_gold = 700 * data["multi_g"]
        current_time = time.time()
        delta = int(current_time) - int(data["booster_block"])

        if delta >= 86400:
            data["gold"] += new_gold
            data["booster_block"] = current_time
            await self.bot.players.update_one({"_id": author.id}, {"$set": data})
            embed = disnake.Embed(
                description=f"**You received your booster gold! {int(new_gold)} G**",
                color=BLUE,
            )
            return await inter.send(embed=embed, ephemeral=True)

        seconds = 86400 - delta
        embed = disnake.Embed(
            description=(
                f"**You can't claim your booster reward yet!\n\nYou can claim your booster reward"
                f" <t:{int(time.time()) + int(seconds)}:R>**"
            ),
            color=BLUE,
        )

        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(description="Claim your daily gold reward.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def daily(self, inter: disnake.ApplicationCommandInteraction):
        """Claim Your daily Reward!"""
        await create_player_info(inter, inter.author)
        data = await self.bot.players.find_one({"_id": inter.author.id})

        new_gold = 250 * data["multi_g"]
        current_time = time.time()
        delta = int(current_time) - int(int(data["daily_block"]))

        if delta >= 86400:
            data["gold"] += new_gold
            data["daily_block"] = current_time
            await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
            embed = disnake.Embed(
                description=f"**You received your daily gold! {int(new_gold)} G**",
                color=BLUE,
            )
            return await inter.send(embed=embed)

        seconds = 86400 - delta
        embed = disnake.Embed(
            description=(
                f"**You can't claim your daily reward yet!\n\nYou can claim your daily reward"
                f" <t:{int(time.time()) + int(seconds)}:R>**"
            ),
            color=BLUE,
        )
        await inter.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))

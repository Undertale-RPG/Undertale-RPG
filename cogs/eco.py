import random
import time

import disnake
from disnake.ext import commands
from disnake.ui import Button
from disnake.enums import ButtonStyle

from main import UndertaleBot
from utility.constants import BLUE,HEALTH,GOLD,ATTACK,DEFENCE,LEVEL,EXP
from utility.utils import create_player_info


class Economy(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def supporter(self, inter: disnake.ApplicationCommandInteraction):
        """Get your supporter reward for being in our support server."""
        await create_player_info(inter, inter.author)
        if inter.guild.id != 817437132397871135:
            em = disnake.Embed(
                description=f"This command is specifically for our support server, which you can access by joining through the link below. Click the button to join:",
                color=BLUE
            )

            buttons = [
            Button(
                style=ButtonStyle.link,
                label="Support server",
                url="https://discord.gg/FQYVpuNz4Q",
            ),
            ]
            
            return await inter.send(embed=em, ephemeral=True, components=buttons)

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
                    description=f"**You received your supporter gold! {int(gold_amount)} {GOLD}**",
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

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def gold(self, inter: disnake.ApplicationCommandInteraction, member: disnake.User = None):
        """Check your gold balance"""
        player = member or inter.author

        if player.bot:
            return await inter.send("Nice try!", ephemeral=True)

        await create_player_info(inter, player)

        data = await self.bot.players.find_one({"_id": player.id})
        gold = data["gold"]

        embed = disnake.Embed(
            title="Balance",
            color=BLUE,
            description=f"{player.name}'s balance\n**{round(gold)} {GOLD}**",
        )
        await inter.send(embed=embed)

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def stats(self, inter: disnake.ApplicationCommandInteraction, member: disnake.User = None):
        """Check your stats and progress"""
        player = member or inter.author
        if player.bot:
            await inter.send("Nice try!")
            return

        await create_player_info(inter, player)

        data = await self.bot.players.find_one({"_id": player.id})
        badge_data = await self.bot.data.find_one({"_id": "badges"})

        health = data["health"]
        level = data["level"]
        exp = data["exp"]
        exp_lvl_up = level * 100 / 0.4
        kills = data["kills"]
        deaths = data["deaths"]
        spares = data["spares"]
        gold = data["gold"]
        weapon = data["weapon"]
        armor = data["armor"]
        resets = data["resets"]
        multi_g = data["multi_g"]
        multi_xp = data["multi_xp"]
        max_health = level * 2 / 0.5 + 20
        atk = data["attack"]
        deff = data["defence"]

        badges = ""
        for i in data["badges"]:
            badges += f"{badge_data[i]} "
        if len(data["badges"]) == 0:
            badges = "None"

        embed = disnake.Embed(
            title=f"{player.name}'s stats",
            color=BLUE,
            description=f"""
            ▫️ **Badges:** {badges}
            {HEALTH} **Health:** `{round(health)}/{round(max_health)}`
            {LEVEL} **Level:** `{round(level)}`
            ▫️ **Exp:** `{round(exp)}/{round(exp_lvl_up)}`
            ▫️ **Deaths:** `{round(deaths)}`
            ▫️ **Spares:** `{round(spares)}`
            {GOLD} **Gold:** `{round(gold)}`
            ▫️ **Weapon:** `{weapon}`
            ▫️ **Armor:** `{armor}`
            ▫️ **Resets:** `{round(resets)}`
            {ATTACK} **Attack:** `{round(atk)}`
            {DEFENCE} **Defence:** `{round(deff)}`
            ▫️ **Gold Multiplier:** `{multi_g}`
            ▫️ **Exp Multiplier:** `{multi_xp}`
            """,
        )
        embed.set_thumbnail(url=player.display_avatar)

        await inter.send(embed=embed)

    @commands.slash_command()
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
                description=f"**You received your booster gold! {int(new_gold)} {GOLD}**",
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

    @commands.slash_command()
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
                description=f"**You received your daily gold! {int(new_gold)} {GOLD}**",
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

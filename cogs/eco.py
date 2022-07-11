import random
import time

import disnake
from disnake.ext import commands

from utility.utils import get_bar, in_battle, in_shop, create_player_info

from datetime import datetime

starttime = time.time()


class Choice(disnake.ui.View):
    def __init__(self, author: disnake.Member):
        super().__init__()
        self.author = author
        self.choice = None

    @disnake.ui.button(label="Yes", style=disnake.ButtonStyle.green)
    async def yes(self, button, inter):
        if inter.author != self.author:
            return await inter.send("This is not yours kiddo!", ephemeral=True)
        self.choice = True
        await inter.response.defer()

        await inter.edit_original_message(components=[])
        self.stop()

    @disnake.ui.button(label="No", style=disnake.ButtonStyle.red)
    async def no(self, button, inter):
        if inter.author != self.author:
            return await inter.send("This is not yours kiddo!", ephemeral=True)
        self.choice = False

        await inter.response.defer()

        await inter.edit_original_message(components=[])
        self.stop()


class Economy(commands.Cog):
    """Economy module and balance related"""

    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    @in_shop()
    @in_battle()
    async def reset(self, inter):
        await create_player_info(inter, inter.author)
        old_data = await self.bot.players.find_one({"_id": inter.author.id})

        if old_data["level"] < 50:
            await inter.send(
                "you are not yet passed, reach **LVL70**, and you shall come back"
            )
            return

        gold = round(old_data["multi_g"] + 0.4, 1)
        xp = round(old_data["multi_xp"] + 0.2, 1)

        embed = disnake.Embed(
            title="Reseting your world.",
            description=("Are you sure you want to proceed\nYour progress will vanish, but you will gain multipliers"
                         "for gold and xp.\n\n"
                         f"Your gold multiplier will be **{gold}x**"
                         f"\nYour XP multiplier will be **{xp}x**"
                         )
        )
        embed.set_image(
            "https://static.wikia.nocookie.net/xtaleunderverse4071/images/c/c4/UnderverseReset.jpg"
        )
        embed.set_thumbnail(inter.author.display_avatar)

        embed.set_footer(text=datetime.utcnow(), icon_url=inter.bot.user.avatar.url)

        embed.set_author(name=f"executed by {str(inter.author)}", icon_url=inter.author.display_avatar)
        view = Choice(inter.author)
        await inter.send(embed=embed, view=view)
        await view.wait()

        if view.choice:
            await self.bot.players.delete_one({"_id": inter.author.id})
            await create_player_info(inter, inter.author)
            new_data = await self.bot.players.find_one({"_id": inter.author.id})
            new_data["resets"] = old_data["resets"] + 1
            new_data["multi_g"] = old_data["multi_g"] + 0.4
            new_data["multi_xp"] = old_data["multi_xp"] + 0.2
            new_data["tokens"] = old_data["tokens"]
            new_data["kills"] = old_data["kills"]
            new_data["deaths"] = old_data["deaths"]
            await self.bot.players.update_one(
                {"_id": inter.author.id}, {"$set": new_data}
            )
            await inter.send("You deleted your world, a new world appear in the horizon.")
        else:
            await inter.send("You should come back again!")

    @commands.command(aliases=["bt"])
    @in_shop()
    @in_battle()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def booster(self, inter):
        """Claim Your daily Reward!"""
        author = inter.author

        await create_player_info(inter, inter.author)
        if author.id not in inter.bot.boosters["boosters"]:
            await inter.send(
                "You are not a booster!, only people who boost our support server are able to get the rewards!")
            return
        info = await self.bot.players.find_one({"_id": author.id})
        goldget = 2500 * info["multi_g"]
        curr_time = time.time()
        if "booster_block" not in info:
            info["booster_block"] = 0
        delta = int(curr_time) - int(info["booster_block"])

        if delta >= 86400 and delta > 0:
            info["gold"] += goldget
            info["booster_block"] = curr_time
            await self.bot.players.update_one({"_id": author.id}, {"$set": info})
            em = disnake.Embed(
                description=f"**You received your booster gold! {int(goldget)} G**",
                color=disnake.Color.blue(),
            )
            return await inter.send(embed=em)
        else:
            seconds = 86400 - delta
            em = disnake.Embed(
                description=(
                    f"**You can't claim your booster reward yet!\n\nYou can claim your booster reward"
                    f" <t:{int(time.time()) + int(seconds)}:R>**"),
                color=disnake.Color.red(),
            )

        await inter.send(embed=em)

    @commands.command(aliases=["dl"])
    @in_shop()
    @in_battle()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def daily(self, inter):
        """Claim Your daily Reward!"""
        author = inter.author
        await create_player_info(inter, inter.author)

        info = await self.bot.players.find_one({"_id": author.id})
        goldget = 500 * info["multi_g"]
        curr_time = time.time()
        delta = int(curr_time) - int(info["daily_block"])

        if delta >= 86400 and delta > 0:
            info["gold"] += goldget
            info["daily_block"] = curr_time
            await self.bot.players.update_one({"_id": author.id}, {"$set": info})
            em = disnake.Embed(
                description=f"**You received your daily gold! {int(goldget)} G**",
                color=disnake.Color.blue(),
            )
        else:
            seconds = 86400 - delta
            em = disnake.Embed(
                description=(
                    f"**You can't claim your daily reward yet!\n\nYou can claim your daily reward"
                    f"<t:{int(time.time()) + int(seconds)}:R>**"
                ),
                color=disnake.Color.red(),
            )

        await inter.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def gold(self, inter):
        """Check your gold balance"""
        await create_player_info(inter, inter.author)
        info = await self.bot.players.find_one({"_id": inter.author.id})
        bal = info["gold"]
        embed = disnake.Embed(
            title="Balance",
            description=f"Your balance:\n**{int(bal)}G**",
            color=disnake.Colour.random(),
        )
        await inter.send(embed=embed)

    # for our guild only for now.
    @commands.user_command(name="Check Stats", guild_ids=[817437132397871135])
    async def check_stats(self, inter, member):
        await inter.response.defer()
        await Economy.stats(self, inter, member)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats(self, inter, member: disnake.User = None):
        """Check your stats and powers"""
        player = member or inter.author
        if player.bot:
            await inter.send("Nice try!")
            return
        await create_player_info(inter, player)
        info = await self.bot.players.find_one({"_id": player.id})

        xp = info["exp"]
        # stats
        level = info["level"]
        lvlexp = self.bot.levels[str(level)]["EXP_TO_LVLUP"]
        
        health = info["health"]
        max_health = self.bot.levels[str(level)]["HP"]

        bar = await get_bar(health, max_health)
        armor = info["armor"]
        weapon = info["weapon"]
        deaths = info["deaths"]
        gold = info["gold"]
        kills = info["kills"]
        resets = info["resets"]
        g_mult = info["multi_g"]
        xp_mult = info["multi_xp"]
        tokens = info["tokens"]

        embed = disnake.Embed(
            title=f"{player.name}‘s Stats!",
            description="Your Status and progress in the game",
            color=disnake.Color.random(),
        )
        embed.add_field(
            name="<:HP:916553886339309588>┃Health",
            value=f"{health}/{max_health} {bar}"
        )
        embed.add_field(
            name="<:LV:916554742975590450>┃LOVE",
            value=f"{level}"
        )
        embed.add_field(
            name="<:XP:916555463145971772>┃XP",
            value=f"{round(xp)}/{lvlexp}"
        )
        embed.add_field(
            name="<:KillsWeapon:916556418025414657> ┃kills",
            value=f"{kills}"
        )
        embed.add_field(
            name="<:broken_heart:865088299520753704>┃deaths",
            value=f"{deaths}"
        )
        embed.add_field(
            name="<:KillsWeapon:916556418025414657> ┃Weapon",
            value=f"{weapon}"
        )
        embed.add_field(
            name="<:armor:916558817595097098>┃Armor",
            value=f"{armor}"
        )
        embed.add_field(
            name="<:gold:924599104674332727>┃Gold",
            value=f"{int(gold)}"
        )
        embed.add_field(name="▫️┃Tokens", value=f"{int(tokens)}")
        embed.add_field(name="▫️┃Resets", value=f"{resets}")
        embed.add_field(name="▫️┃Gold Multiplier", value=f"{round(g_mult, 1)}x")
        embed.add_field(name="▫️┃XP Multiplier", value=f"{round(xp_mult, 1)}x")

        embed.set_thumbnail(url=player.display_avatar)
        await inter.send(embed=embed)

    @commands.command(aliases=["sp"])
    @in_shop()
    @in_battle()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def supporter(self, inter):
        """Join our support server and claim a bunch of gold"""
        await create_player_info(inter, inter.author)
        while True:
            if inter.guild.id != 817437132397871135:
                await inter.send(
                    "this command is exclusive for our server, you can join via \n\n https://discord.gg/FQYVpuNz4Q"
                )
                return
            author = inter.author

            info = await self.bot.players.find_one({"_id": author.id})
            goldget = random.randint(500, 1000) * info["multi_g"]
            try:
                curr_time = time.time()
                delta = int(curr_time) - int(info["supporter_block"])

                if delta >= 86400 and delta > 0:
                    info["gold"] += goldget
                    info["supporter_block"] = curr_time
                    await self.bot.players.update_one(
                        {"_id": author.id}, {"$set": info}
                    )
                    em = disnake.Embed(
                        description=f"**You received your supporter gold! {int(goldget)} G**",
                        color=disnake.Color.blue(),
                    )
                else:
                    seconds = 86400 - delta
                    em = disnake.Embed(
                        description=(
                            f"**You can't claim your supporter reward yet!\n\n You can use this command again"
                            f" <t:{int(time.time()) + int(seconds)}:R>**"
                                     ),
                        color=disnake.Color.red(),
                    )
                await inter.send(embed=em)
                break
            except KeyError:
                info["supporter_block"] = 0
                await self.bot.players.update_one({"_id": author.id}, {"$set": info})
                continue


def setup(bot):
    bot.add_cog(Economy(bot))

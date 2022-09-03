import disnake
from disnake.ext import commands
from utility.utils import in_battle, in_shop, create_player_info
from datetime import datetime
import random
from utility import utils
from utility.dataIO import fileIO

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

class Explore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="explore to find monsters, xp, gold and items")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def explore(self, inter):
        """Explore and fine all kinds of monsters and treasure!"""
        await utils.create_player_info(inter, inter.author)
        choices = ["fight", "gold", "crate", "puzzle"]
        item = random.choices(choices, weights=(80, 10, 10, 10), k=1)

        data = await inter.bot.players.find_one({"_id": inter.author.id})

        if item[0] == "fight":
            location = data["location"]
            monsters = fileIO("./data/monsters.json", "load")

            random_monster = []

            for i in monsters[location]:
                random_monster.append(i)

            print(random_monster)

            if len(random_monster) == 0:
                await inter.send(f"There are no monsters here?, You are for sure inside a u?boss area only!")
                return

        monster = random.choice(random_monster)
        await inter.send(f"{monster} appeard!")

        enemy_hp = monsters[location][monster]["hp"]
        enemy_atk = monsters[location][monster]["attack"]
        enemy_def = monsters[location][monster]["defence"]
        gold_min = monsters[location][monster]["gold_min"]
        gold_max = monsters[location][monster]["gold_max"]
        enemy_exp = monsters[location][monster]["exp"]
        title = monsters[location][monster]["title"]
        
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
    
    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def reset(self, inter):
        data = await self.bot.players.find_one({"_id": inter.author.id})

        if data["level"] < 70:
            await inter.send("You can not reset just yet. You will need to be **LOVE 70**")
            return
        if data["resets"] >= 10:
            await inter.send("You are already at the max amount of resets!")
            return

        gold = round(data["multi_g"] + 0.4, 1)
        xp = round(data["multi_xp"] + 0.2, 1)

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
            new_data["resets"] = data["resets"] + 1
            new_data["multi_g"] = data["multi_g"] + 0.4
            new_data["multi_xp"] = data["multi_xp"] + 0.2
            new_data["tokens"] = data["tokens"]
            new_data["kills"] = data["kills"]
            new_data["deaths"] = data["deaths"]
            new_data["registered_on"] = data["registered_on"]
            await self.bot.players.update_one(
                {"_id": inter.author.id}, {"$set": new_data}
            )
            await inter.send("You deleted your world, a new world appears in the horizon.")
        else:
            await inter.send("You should come back again!")



def setup(bot):
    bot.add_cog(Explore(bot))
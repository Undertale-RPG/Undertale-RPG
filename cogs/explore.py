from discord import Embed
import disnake
from disnake.ext import commands
from utility.utils import in_battle, in_shop, create_player_info, ConsoleColors
from datetime import datetime
import random
from utility import utils
from utility.dataIO import fileIO
import time
import humanize
import asyncio
from disnake.ext import commands

class Travelbtn(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="Ruins", style=disnake.ButtonStyle.secondary)
    async def ruins(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "ruins"
        self.stop()

    @disnake.ui.button(label="Snowdin", style=disnake.ButtonStyle.secondary)
    async def snowdin(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "snowdin"
        self.stop()

    @disnake.ui.button(label="Waterfall", style=disnake.ButtonStyle.secondary)
    async def waterfall(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "waterfall"
        self.stop()

    @disnake.ui.button(label="Hotland", style=disnake.ButtonStyle.secondary)
    async def hotland(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "hotland"
        self.stop()

    @disnake.ui.button(label="Core", style=disnake.ButtonStyle.secondary)
    async def core(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "core"
        self.stop()

    @disnake.ui.button(label="Barrier", style=disnake.ButtonStyle.secondary)
    async def barrier(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "barrier"
        self.stop()

    @disnake.ui.button(label="Last Corridor", style=disnake.ButtonStyle.secondary)
    async def last_corridor(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "last_corridor"
        self.stop()

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

class Explorebtn(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="Fight", style=disnake.ButtonStyle.red)
    async def fight(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "fight"
        self.stop()

    @disnake.ui.button(label="Use", style=disnake.ButtonStyle.gray)
    async def use(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        self.value = "use"
        self.stop()

    @disnake.ui.button(label="Mercy", style=disnake.ButtonStyle.green)
    async def mercy(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        self.value = "mercy"
        self.stop()

async def Battle(self, inter, monster: str, user_hp: int, user_atk: int, user_def: int):
    await inter.edit_original_message("test")

class Explore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="explore to find monsters, xp, gold and items")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def explore(self, inter):
        """Explore and find all kinds of monsters and treasure!"""
        await utils.create_player_info(inter, inter.author)
        choices = ["fight", "gold", "crate", "puzzle"]
        item = random.choices(choices, weights=(90, 10, 10, 10), k=1)

        data = await inter.bot.players.find_one({"_id": inter.author.id})

        if item[0] == "fight":
            location = data["location"]
            monsters = fileIO("./data/monsters.json", "load")

            random_monster = []

            for i in monsters[location]:
                random_monster.append(i)

            if len(random_monster) == 0:
                return await inter.send(f"There are no monsters here?, You are for sure inside a /boss area only!")

            monster = random.choice(random_monster)
            #player stats
            location = data["location"]
            user_hp = data["health"]
            user_atk = data["attack"]
            user_def = data["defence"]

            #monster stats
            enemy_title = monsters[location][monster]["title"]
            enemy_hp = monsters[location][monster]["hp"]
            enemy_atk = monsters[location][monster]["attack"]
            enemy_def = monsters[location][monster]["defence"]

            em = disnake.Embed(
                title=enemy_title,
                description=f"**Location:** {location}",
                color=0x0077ff
            )
            em.set_thumbnail(url=inter.author.avatar)
            em.add_field(name=f"{monster}'s stats", value=f"**HP:** {enemy_hp}\n**Attack:** {enemy_atk}\n**Defence:** {enemy_def}")
            em.add_field(name=f"{inter.author.name}'s stats", value=f"**HP:** {user_hp}\n**Attack:** {user_atk}\n**Defence:** {user_def}")
            view = Explorebtn()
            await inter.send(embed=em, view=view, ephemeral=True)
            info = {"in_fight": True, "fight_monster": monster, "fight_hp": enemy_hp, "fight_atk": enemy_atk, "fight_def": enemy_def}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            print(f"{ConsoleColors.YELLOW}{inter.author} has entered a fight{ConsoleColors.ENDC}")


            await view.wait()
            if view.value == None:
                return await inter.edit_original_message("You took to long to reply!")
            else:
                if view.value == "fight":
                    await Battle(self, inter, monster, user_hp, user_atk, user_def)
                if view.value == "mercy":
                    em = disnake.Embed(
                        title="Mercy",
                        color=0x0077ff,
                        description=f"You tried to spare {monster}"
                    )
                    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
                    await inter.edit_original_message(embed=em, view=None)
                    await asyncio.sleep(5)

                    choice = 2 #random.randint(1, 3)
                    if choice == 2:
                        em = disnake.Embed(
                            title="Mercy",
                            color=0x0077ff,
                            description=f"{monster} didn't accept your mercy!"
                        )
                        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
                        await inter.edit_original_message(embed=em)

                        await Battle(self, inter)
                    else:
                        em = disnake.Embed(
                            title="Mercy",
                            color=0x0077ff,
                            description=f"{monster} accepted your mercy!"
                        )
                        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
                        await inter.edit_original_message(embed=em)
                        spares = data["spares"] =+ 1
                        info = {"in_fight": False, "fight_monster": "", "fight_hp": 0, "fight_atk": 0, "fight_def": 0, "spares": spares}
                        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

                        print(f"{ConsoleColors.LRED}{inter.author} has stopped a fight(spared){ConsoleColors.ENDC}")
                        return

        if item[0] == "gold":
            found_gold = random.randint(150, 250)
            new_gold = data["gold"] + found_gold
            data["gold"] += found_gold
            await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
            await inter.send(content=f"You found `{found_gold}`**G**! you now have `{round(new_gold)}`**G**", ephemeral=True)
            return
        
        if item[0] == "crate":
            data["determination crate"] += 1
            await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
            await inter.send(content="You found `1` Determination crate! you can open it with `/crates`", ephemeral=True)
            return

        if item[0] == "puzzle":
            await inter.send(content="coming soon! do the command again to fight monsters", ephemeral=True)
            return
    
    @commands.slash_command(description="Reset your stats for multipliers of gold and exp.")
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
                         ),
            color=0x0077ff
        )
        embed.set_image("https://static.wikia.nocookie.net/xtaleunderverse4071/images/c/c4/UnderverseReset.jpg")
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

    @commands.slash_command(description="Travel within the world of undertale and fight unique enemies.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def travel(self, inter):
        data = await self.bot.players.find_one({"_id": inter.author.id})

        curr_location = data["location"]
        lvl = data["level"]

        em = disnake.Embed(
            title="Where would you like to go?",
            description=f"**Current location:** {curr_location}\n**Current level:** {lvl}",
            color=0x0077ff
        )
        em.add_field(name="Locations", value="""
        Ruins
        Snowdin
        Waterfall
        Hotland
        Core
        Barrier
        Last Corridor
        """)
        em.add_field(name="Level Requirements", value="""
        lvl **1**
        lvl **5**
        lvl **13**
        lvl **25**
        lvl **50**
        lvl **75**
        lvl **100**
        """)
        view = Travelbtn()
        await inter.send(view=view, embeds=[em], ephemeral=True)

        await view.wait()
        if view.value == None:
            return await inter.edit_original_message("You took to long to reply!")
        else:
            locations = fileIO("data/locations.json", "load")

            if locations[view.value]["level"] > lvl:
                return await inter.edit_original_message(
                    content=f"You are to low of a level to travel here!",
                    embed=None,
                    components=[]
                )

            if curr_location == view.value:
                return await inter.edit_original_message(
                    content=f"You are already at **{curr_location}**",
                    embed=None,
                    components=[]
                )
            
            data["location"] = view.value
            
            info = {"location": data["location"]}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            await inter.edit_original_message(
                content=f"Traveling to **{view.value}**...",
                embed=None,
                components=[]
            )

            await asyncio.sleep(3)
            await inter.edit_original_message(
                content=f"You arrived at **{view.value}**"
            )

    @commands.slash_command(description="View the top 10 players on specific stats.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def leaderboard(self, inter, lb: str = None):
        if lb not in ["gold", "exp", "resets", "kills", "spares", "deaths"] or None:
            em = disnake.Embed(
                title=f"There is no shuch leaderboard as {lb}",
                description="""
                You can choose from the following leaderboards:
                **gold, exp, resets, kills, spared, deaths**
                """,
                color=0x0077ff
            )
            em.set_thumbnail(url="https://media.discordapp.net/attachments/900274624594575361/974933965356019772/trophy.png")
            return await inter.send(embed=em)

        data = self.bot.players.find().limit(10).sort(lb, -1)
        users = []
        async for raw in data:
            users.append(raw)

        users.sort(key=lambda user: user[lb], reverse=True)

        output = [""]
        for i, user in enumerate(users, 1):
            player = await self.bot.fetch_user(user['_id'])
            if i == 1:
                i = ":medal:"
            if i == 2:
                i = ":second_place:"
            if i == 3:
                i = ":third_place:"

            if len(str(player)) >= 24:
                player = str(player)[:-10]

            output.append(
                f"**{i}. {str(player)}:** {humanize.intcomma(int(user[lb]))} {lb}"
            )
            if i == 10:
                break
        output.append("")
        result = "\n".join(output)
        embed = disnake.Embed(
            title=f"{lb} Leaderboard:",
            description=f"{result}",
            color=0x0077ff,
        )
        embed.set_image(
            url="https://media.discordapp.net/attachments/900274624594575361/974936472199249970/lb_image.png"
        )
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/900274624594575361/974933965356019772/trophy.png"
        )
        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Explore(bot))
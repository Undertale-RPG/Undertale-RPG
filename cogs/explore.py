import disnake
from disnake.ext import commands
from utility.utils import create_player_info, ConsoleColors
from datetime import datetime
import random
from utility import utils
from utility.dataIO import fileIO
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

class Loading(disnake.ui.View):
    def __init__(self):
        super().__init__()

    @disnake.ui.button(emoji="<a:loading:1033856122345508874>", style=disnake.ButtonStyle.gray, disabled=True)
    async def loading(self):
        return

class Bossbtn(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label="Fight", style=disnake.ButtonStyle.red)
    async def fight(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        monsters = fileIO("./data/bosses.json", "load")
        monster = data["fight_monster"]
        #player stats
        location = data["location"]
        user_hp = data["health"]
        user_atk = data["attack"]
        user_def = data["defence"]
        #monster stats
        enemy_title = monsters[location][monster]["title"]
        enemy_hp = data["fight_hp"]
        enemy_atk = monsters[location][monster]["attack"]
        enemy_def = monsters[location][monster]["defence"]

        gold_min = monsters[location][monster]["gold_min"]
        gold_max = monsters[location][monster]["gold_max"]

        await BossBattle(self, inter, monster, user_hp, user_atk, user_def, enemy_title, enemy_hp, enemy_atk, enemy_def, gold_min, gold_max)
        return

    @disnake.ui.button(label="Use", style=disnake.ButtonStyle.gray, disabled=True)
    async def use(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        await interaction.response.defer()

    @disnake.ui.button(label="Mercy", style=disnake.ButtonStyle.green)
    async def mercy(self, button: disnake.ui.button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        loading = Loading()

        location = data["location"]
        monsters = fileIO("./data/bosses.json", "load")
        monster = data["fight_monster"]
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

        gold_min = monsters[location][monster]["gold_min"]
        gold_max = monsters[location][monster]["gold_max"]

        em = disnake.Embed(
            title="Mercy",
            color=0x0077ff,
            description=f"You tried to spare {monster}"
        )
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
        await inter.edit_original_message(embed=em, view=loading)
        await asyncio.sleep(5)

        choice = random.randint(1, 3)
        if choice == 2:
            em = disnake.Embed(
                title="Mercy",
                color=0x0077ff,
                description=f"{monster} didn't accept your mercy!"
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
            await inter.edit_original_message(embed=em)
            await asyncio.sleep(5)

            await Battle(self, inter, monster, user_hp, user_atk, user_def, enemy_title, enemy_hp, enemy_atk, enemy_def, gold_min, gold_max)
        else:
            em = disnake.Embed(
                title="Mercy",
                color=0x0077ff,
                description=f"{monster} accepted your mercy!"
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
            await inter.edit_original_message(embed=em, view=None)
            spares = data["spares"] =+ 1
            info = {"in_fight": False, "fight_monster": "", "fight_hp": 0, "fight_atk": 0, "fight_def": 0, "spares": spares}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            print(f"{ConsoleColors.LRED}{inter.author} has stopped a fight(spared){ConsoleColors.ENDC}")
            return

class Explorebtn(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label="Fight", style=disnake.ButtonStyle.red)
    async def fight(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        monsters = fileIO("./data/monsters.json", "load")
        monster = data["fight_monster"]
        #player stats
        location = data["location"]
        user_hp = data["health"]
        user_atk = data["attack"]
        user_def = data["defence"]
        #monster stats
        enemy_title = monsters[location][monster]["title"]
        enemy_hp = data["fight_hp"]
        enemy_atk = monsters[location][monster]["attack"]
        enemy_def = monsters[location][monster]["defence"]

        gold_min = monsters[location][monster]["gold_min"]
        gold_max = monsters[location][monster]["gold_max"]

        await Battle(self, inter, monster, user_hp, user_atk, user_def, enemy_title, enemy_hp, enemy_atk, enemy_def, gold_min, gold_max)
        return

    #@disnake.ui.button(label="Use", style=disnake.ButtonStyle.gray, disabled=True)
    #async def use(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
    #    await interaction.response.defer()

    @disnake.ui.button(label="Mercy", style=disnake.ButtonStyle.green)
    async def mercy(self, button: disnake.ui.button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        loading = Loading()

        location = data["location"]
        monsters = fileIO("./data/monsters.json", "load")
        monster = data["fight_monster"]
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

        gold_min = monsters[location][monster]["gold_min"]
        gold_max = monsters[location][monster]["gold_max"]

        em = disnake.Embed(
            title="Mercy",
            color=0x0077ff,
            description=f"You tried to spare {monster}."
        )
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
        await inter.edit_original_message(embed=em, view=loading)
        await asyncio.sleep(5)

        choice = random.randint(1, 3)
        if choice == 2:
            em = disnake.Embed(
                title="Mercy",
                color=0x0077ff,
                description=f"{monster} didn't accept your mercy!"
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
            await inter.edit_original_message(embed=em)
            await asyncio.sleep(5)

            await Battle(self, inter, monster, user_hp, user_atk, user_def, enemy_title, enemy_hp, enemy_atk, enemy_def, gold_min, gold_max)
        else:
            em = disnake.Embed(
                title="Mercy",
                color=0x0077ff,
                description=f"{monster} accepted your mercy!"
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032089003912089770/3abaf892f9a10b66e7341589a9b6d210.jpg")
            await inter.edit_original_message(embed=em, view=None)
            spares = data["spares"] =+ 1
            info = {"in_fight": False, "fight_monster": "", "fight_hp": 0, "fight_atk": 0, "fight_def": 0, "spares": spares}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            print(f"{ConsoleColors.LRED}{inter.author} has stopped a fight(spared){ConsoleColors.ENDC}")
            return

async def BossBattle(self, inter, monster: str, user_hp: int, user_atk: int, user_def: int, enemy_title: str, enemy_hp: int, enemy_atk: int, enemy_def: int, gold_min: int, gold_max: int):
    view = Bossbtn()
    loading = Loading()
    data = await inter.bot.players.find_one({"_id": inter.author.id})

    new_user_hp = user_hp - enemy_atk
    new_enemy_hp = enemy_hp - user_atk

    em = disnake.Embed(
        title=f"You damaged {monster}",
        color=0x0077ff,
        description=f"""
        **{monster}'s stats**
        **HP:** {new_enemy_hp}
        **Attack:** {enemy_atk}
        **Defence:** {enemy_def}
        """
    )
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032250561610907650/download.png")
    await inter.edit_original_message(embed=em, view=loading)
    await asyncio.sleep(5)

    if new_enemy_hp <= 0:
        location = data["location"]
        monsters = fileIO("./data/bosses.json", "load")
        exp = monsters[location][monster]["exp"]
        gold = random.randint(gold_min, gold_max)
        em = disnake.Embed(
            title=f"{monster} died!",
            color=0x0077ff,
            description=f"You got **{exp}**EXP, **{gold}**G and **1** soul crate!"
        )
        await inter.edit_original_message(embed=em, view=None)
        new_gold = data["gold"] + gold
        new_exp = data["exp"] + exp
        new_soul_crate = data["soul crate"] + 1
        kills = data["kills"] + 1
        info = {f"{location}_boss": True, "soul crate": new_soul_crate, "in_fight": False, "kills": kills, "exp": new_exp, "gold": new_gold, "health": user_hp, "fight_monster": "", "fight_hp": 0, "fight_atk": 0, "fight_def": 0}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})
        print(f"{ConsoleColors.LRED}{inter.author} has stopped a fight(won){ConsoleColors.ENDC}")

        await levelup_check(self, inter)
        return

    em = disnake.Embed(
        title=f"{monster} damaged you",
        color=0x0077ff,
        description=f"""
        **{inter.author.name}'s stats**
        **HP:** {new_user_hp}
        **Attack:** {user_atk}
        **Defence:** {user_atk}
        """
    )
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032250561610907650/download.png")
    await inter.edit_original_message(embed=em)
    await asyncio.sleep(5)

    if new_user_hp <= 0:
        location = data["location"]
        monsters = fileIO("./data/bosses.json", "load")
        em = disnake.Embed(
            title="You died!",
            color=0x0077ff,
            description=f"You lost **{gold_min}**G"
        )
        await inter.edit_original_message(embed=em, view=None)
        new_gold = data["gold"] - gold_min
        if new_gold < 0:
            new_gold = 0
        deaths = data["deaths"] + 1
        info = {"in_fight": False, "deaths": deaths, "gold": new_gold, "health": 20, "fight_monster": "", "fight_hp": 0, "fight_atk": 0, "fight_def": 0}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})
        print(f"{ConsoleColors.LRED}{inter.author} has stopped a fight(died){ConsoleColors.ENDC}")
        return

    em = disnake.Embed(
        title=enemy_title,
        color=0x0077ff
    )
    em.set_thumbnail(url=inter.author.avatar)
    em.add_field(name=f"{monster}'s stats", value=f"**HP:** {new_enemy_hp}\n**Attack:** {enemy_atk}\n**Defence:** {enemy_def}")
    em.add_field(name=f"{inter.author.name}'s stats", value=f"**HP:** {new_user_hp}\n**Attack:** {user_atk}\n**Defence:** {user_def}")
    await inter.edit_original_message(embed=em, view=view)
    info = {"health": new_user_hp, "fight_hp": new_enemy_hp, "fight_atk": enemy_atk, "fight_def": enemy_def}
    await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

async def Battle(self, inter, monster: str, user_hp: int, user_atk: int, user_def: int, enemy_title: str, enemy_hp: int, enemy_atk: int, enemy_def: int, gold_min: int, gold_max: int):
    view = Explorebtn()
    loading = Loading()
    data = await inter.bot.players.find_one({"_id": inter.author.id})

    new_user_hp = user_hp - enemy_atk
    new_enemy_hp = enemy_hp - user_atk

    em = disnake.Embed(
        title=f"You damaged {monster}",
        color=0x0077ff,
        description=f"""
        **{monster}'s stats**
        **HP:** {new_enemy_hp}
        **Attack:** {enemy_atk}
        **Defence:** {enemy_def}
        """
    )
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032250561610907650/download.png")
    await inter.edit_original_message(embed=em, view=loading)
    await asyncio.sleep(5)

    if new_enemy_hp <= 0:
        location = data["location"]
        monsters = fileIO("./data/monsters.json", "load")
        exp = monsters[location][monster]["exp"]
        gold = random.randint(gold_min, gold_max)
        em = disnake.Embed(
            title=f"{monster} died!",
            color=0x0077ff,
            description=f"You got **{exp}**EXP and **{gold}**G"
        )
        await inter.edit_original_message(embed=em, view=None)
        new_gold = data["gold"] + gold
        new_exp = data["exp"] + exp
        kills = data["kills"] + 1
        info = {"in_fight": False, "kills": kills, "exp": new_exp, "gold": new_gold, "health": user_hp, "fight_monster": "", "fight_hp": 0, "fight_atk": 0, "fight_def": 0}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})
        print(f"{ConsoleColors.LRED}{inter.author} has stopped a fight(won){ConsoleColors.ENDC}")

        await levelup_check(self, inter)
        return

    em = disnake.Embed(
        title=f"{monster} damaged you",
        color=0x0077ff,
        description=f"""
        **{inter.author.name}'s stats**
        **HP:** {new_user_hp}
        **Attack:** {user_atk}
        **Defence:** {user_atk}
        """
    )
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1032250561610907650/download.png")
    await inter.edit_original_message(embed=em)
    await asyncio.sleep(5)

    if new_user_hp <= 0:
        location = data["location"]
        monsters = fileIO("./data/monsters.json", "load")
        em = disnake.Embed(
            title="You died!",
            color=0x0077ff,
            description=f"You lost **{gold_min}**G"
        )
        await inter.edit_original_message(embed=em, view=None)
        new_gold = data["gold"] - gold_min
        if new_gold < 0:
            new_gold = 0
        deaths = data["deaths"] + 1
        info = {"in_fight": False, "deaths": deaths, "gold": new_gold, "health": 20, "fight_monster": "", "fight_hp": 0, "fight_atk": 0, "fight_def": 0}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})
        print(f"{ConsoleColors.LRED}{inter.author} has stopped a fight(died){ConsoleColors.ENDC}")
        return

    em = disnake.Embed(
        title=enemy_title,
        color=0x0077ff
    )
    em.set_thumbnail(url=inter.author.avatar)
    em.add_field(name=f"{monster}'s stats", value=f"**HP:** {new_enemy_hp}\n**Attack:** {enemy_atk}\n**Defence:** {enemy_def}")
    em.add_field(name=f"{inter.author.name}'s stats", value=f"**HP:** {new_user_hp}\n**Attack:** {user_atk}\n**Defence:** {user_def}")
    await inter.edit_original_message(embed=em, view=view)
    info = {"health": new_user_hp, "fight_hp": new_enemy_hp, "fight_atk": enemy_atk, "fight_def": enemy_def}
    await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

async def levelup_check(self, inter):
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    author = inter.author
    exp = data["exp"]
    level = data["level"]
    attack = data["attack"]
    defence = data["defence"]
    exp_lvl_up = level * 100 / 0.4

    if exp >= exp_lvl_up:
        new_attack = attack + 2
        new_defence = defence + 2
        new_lvl = level + 1
        new_exp = exp - exp_lvl_up
        new_exp_lvl_up = new_lvl * 100 / 0.4
        em = disnake.Embed(
            title=f"{author.name} Leveled up!",
            color=0x0077ff,
            description=f"""
            Your new level is **{new_lvl}!**
            Your new exp is **{round(new_exp)}/{round(new_exp_lvl_up)}**
            """
        )
        info = {"level": new_lvl, "exp": new_exp, "attack": new_attack, "defence": new_defence}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})
        await inter.send(embed=em)
    return

class Explore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Fight bosses!")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def boss(self, inter):
        await utils.create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        location = data["location"]
        if data[f"{location}_boss"] == True:
            return await inter.send("You already killed the boss of this location.")
        monsters = fileIO("./data/bosses.json", "load")

        random_monster = []

        for i in monsters[location]:
            random_monster.append(i)

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
        view = Bossbtn()
        await inter.send(embed=em, view=view, ephemeral=True)
        info = {"in_fight": True, "fight_monster": monster, "fight_hp": enemy_hp, "fight_atk": enemy_atk, "fight_def": enemy_def}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

        print(f"{ConsoleColors.YELLOW}{inter.author} has entered a fight{ConsoleColors.ENDC}")
        return

    @commands.slash_command(description="Explore to find monsters, xp, gold and items.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def explore(self, inter):
        """Explore and find all kinds of monsters and treasure!"""
        await utils.create_player_info(inter, inter.author)
        choices = ["fight", "gold", "crate", "puzzle"]
        item = random.choices(choices, weights=(90, 10, 10, 10), k=1)

        data = await inter.bot.players.find_one({"_id": inter.author.id})
        await inter.response.defer()

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
        await utils.create_player_info(inter, inter.author)
        data = await self.bot.players.find_one({"_id": inter.author.id})

        if data["level"] < 70:
            await inter.send("You can not reset just yet. You will need to be **LOVE 70**.")
            return
        if data["resets"] >= 10:
            await inter.send("You are already at the max amount of resets!")
            return

        gold = round(data["multi_g"] + 0.4, 1)
        xp = round(data["multi_xp"] + 0.2, 1)

        embed = disnake.Embed(
            title="Reseting your world.",
            description=("Are you sure you want to proceed?\nYour progress will vanish, but you will gain multipliers "
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
            new_data["kills"] = data["kills"]
            new_data["deaths"] = data["deaths"]
            new_data["registered_on"] = data["registered_on"]
            new_data["badges"] = data["badges"]
            new_data["void crate"] = data["void crate"] + 1
            await self.bot.players.update_one(
                {"_id": inter.author.id}, {"$set": new_data}
            )
            await inter.send("You deleted your world, a new world appears in the horizon.")
        else:
            await inter.send("You should come back again!")

    @commands.slash_command(description="Travel within the world of undertale and fight unique enemies.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def travel(self, inter):
        await utils.create_player_info(inter, inter.author)
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
                    content=f"Your level is too low to travel there!",
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
    async def leaderboard(self, inter, lb:str = None):
        await inter.response.defer()
        if lb not in ["gold", "exp", "resets", "kills", "spares", "deaths"] or None:
            em = disnake.Embed(
                title=f"There is no shuch leaderboard as {lb}",
                description="""
                You can choose from the following leaderboards:
                **gold, exp, resets, kills, spares, deaths**
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
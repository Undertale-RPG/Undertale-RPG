from disnake.ui import Button, View
from discord import ButtonStyle
import disnake
from disnake.ext import commands
import asyncio
from utility.dataIO import fileIO
from utility import utils

class Loading(disnake.ui.View):
    def __init__(self):
        super().__init__()

    @disnake.ui.button(emoji="<a:loading:1033856122345508874>", style=disnake.ButtonStyle.gray, disabled=True)
    async def loading(self):
        return

class Cratesbtn(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="Standard crate", style=disnake.ButtonStyle.secondary)
    async def standard(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "standard crate"
        self.stop()
    
    @disnake.ui.button(label="Determination crate", style=disnake.ButtonStyle.secondary)
    async def determination(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "determination crate"
        self.stop()
    
    @disnake.ui.button(label="Soul crate", style=disnake.ButtonStyle.secondary)
    async def soul(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "soul crate"
        self.stop()

    @disnake.ui.button(label="Void crate", style=disnake.ButtonStyle.secondary)
    async def void(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "void crate"
        self.stop()

    @disnake.ui.button(label="Event crate", style=disnake.ButtonStyle.secondary)
    async def event(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "event crate"
        self.stop()

class Shopbtn(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__()

    @disnake.ui.button(label="Consumables", emoji="🍎", style=disnake.ButtonStyle.secondary)
    async def consumables(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await Consumables(self, inter, button)
        return
    
    @disnake.ui.button(label="Armor", emoji="🔰", style=disnake.ButtonStyle.secondary)
    async def armor(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await Armor(self, inter, button)
        return
    
    @disnake.ui.button(label="Weapons", emoji="🪓", style=disnake.ButtonStyle.secondary)
    async def weapons(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await Weapons(self, inter, button)
        return

async def Consumables(self, inter, button: disnake.ui.Button):
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    consumables = fileIO("./data/consumables.json", "load")

    em = disnake.Embed(
        title=f"{location}'s Shop",
        color=0x0077ff
    )
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1046934688914210906/unknown.png")

    items = []
    for item in consumables[location]:
        items.append(item)
        item_name = consumables[location][item]["name"]
        item_heal = consumables[location][item]["heal"]
        item_price = consumables[location][item]["price"]
        em.add_field(name=item_name,value=f"Heal: **{item_heal}**\nPrice: **{item_price}**")

    view = Consbtn(location, items)
    await inter.edit_original_message(embed=em, view=view)

class Consbtn(disnake.ui.View):
    def __init__(self, location, items) -> None:
        super().__init__(timeout=None)
        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await ConsBuy(self, inter)
        consumables = fileIO("./data/consumables.json", "load")
        for item in items:
            item_name = consumables[location][item]["name"]
            button = Button(label=str(item_name), style=disnake.ButtonStyle.gray, custom_id=item)
            button.callback = shared_callback
            self.add_item(button)
    
async def ConsBuy(self, inter):
    item = inter.component.custom_id
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    consumables = fileIO("./data/consumables.json", "load")
    item_name = consumables[location][item]["name"]
    item_cost = consumables[location][item]["price"]
    gold = data["gold"]
    inv = data["inventory"]
    new_inv = []
    new_inv.append(item)
    for i in inv:
        new_inv.append(i)
    new_gold = gold - item_cost

    info = {"gold": new_gold, "inventory": new_inv}
    await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

    em = disnake.Embed(
        description=f"You bought **{item_name}** for **{item_cost}G**\n\nBalance: **{new_gold}G**",
        color=0x0077ff
    )
    await inter.send(embed=em, ephemeral=True)

async def Armor(self, inter, button: disnake.ui.Button):
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    armor = fileIO("./data/items.json", "load")

    em = disnake.Embed(
        title=f"{location}'s Shop",
        color=0x0077ff
    )
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1046934688914210906/unknown.png")

    items = []
    for item in armor[location]["armor"]:
        items.append(item)
        item_name = armor[location]["armor"][item]["name"]
        item_min_def = armor[location]["armor"][item]["min_def"]
        item_max_def = armor[location]["armor"][item]["max_def"]
        item_price = armor[location]["armor"][item]["price"]
        em.add_field(name=item_name,value=f"Min deffence: **{item_min_def}**\nMax deffence: **{item_max_def}**\nPrice: **{item_price}**")

    view = Armorbtn(location, items)
    await inter.edit_original_message(embed=em, view=view)

class Armorbtn(disnake.ui.View):
    def __init__(self, location, items) -> None:
        super().__init__(timeout=None)
        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await ArmorBuy(self, inter)
        itemsfile = fileIO("./data/items.json", "load")
        for item in items:
            item_name = itemsfile[location]["armor"][item]["name"]
            button = Button(label=str(item_name), style=disnake.ButtonStyle.gray, custom_id=item)
            button.callback = shared_callback
            self.add_item(button)
    
async def ArmorBuy(self, inter):
    item = inter.component.custom_id
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    items = fileIO("./data/items.json", "load")
    item_name = items[location]["armor"][item]["name"]
    item_cost = items[location]["armor"][item]["price"]
    gold = data["gold"]
    inv = data["inventory"]
    new_inv = []
    new_inv.append(item)
    for i in inv:
        new_inv.append(i)
    new_gold = gold - item_cost

    info = {"gold": new_gold, "inventory": new_inv}
    await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

    em = disnake.Embed(
        description=f"You bought **{item_name}** for **{item_cost}G**\n\nBalance: **{new_gold}G**",
        color=0x0077ff
    )
    await inter.send(embed=em, ephemeral=True)

async def Weapons(self, inter, button: disnake.ui.Button):
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    weapons = fileIO("./data/items.json", "load")

    em = disnake.Embed(
        title=f"{location}'s Shop",
        color=0x0077ff
    )
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1046934688914210906/unknown.png")

    items = []
    for item in weapons[location]["weapons"]:
        items.append(item)
        item_name = weapons[location]["weapons"][item]["name"]
        item_min_dmg = weapons[location]["weapons"][item]["min_dmg"]
        item_max_dmg = weapons[location]["weapons"][item]["max_dmg"]
        item_price = weapons[location]["weapons"][item]["price"]
        em.add_field(name=item_name,value=f"Min deffence: **{item_min_dmg}**\nMax deffence: **{item_max_dmg}**\nPrice: **{item_price}**")

    view = weaponsbtn(location, items)
    await inter.edit_original_message(embed=em, view=view)

class weaponsbtn(disnake.ui.View):
    def __init__(self, location, items) -> None:
        super().__init__(timeout=None)
        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await weaponsBuy(self, inter)
        itemsfile = fileIO("./data/items.json", "load")
        for item in items:
            item_name = itemsfile[location]["weapons"][item]["name"]
            button = Button(label=str(item_name), style=disnake.ButtonStyle.gray, custom_id=item)
            button.callback = shared_callback
            self.add_item(button)
    
async def weaponsBuy(self, inter):
    item = inter.component.custom_id
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    items = fileIO("./data/items.json", "load")
    item_name = items[location]["weapons"][item]["name"]
    item_cost = items[location]["weapons"][item]["price"]
    gold = data["gold"]
    inv = data["inventory"]
    new_inv = []
    new_inv.append(item)
    for i in inv:
        new_inv.append(i)
    new_gold = gold - item_cost

    info = {"gold": new_gold, "inventory": new_inv}
    await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

    em = disnake.Embed(
        description=f"You bought **{item_name}** for **{item_cost}G**\n\nBalance: **{new_gold}G**",
        color=0x0077ff
    )
    await inter.send(embed=em, ephemeral=True)

class Usebtn(disnake.ui.View):
    def __init__(self, inv) -> None:
        super().__init__(timeout=None)
        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await UseItem(self, inter)
        for i in inv:
            button = Button(label=i, style=disnake.ButtonStyle.gray)
            button.callback = shared_callback
            self.add_item(button)

async def UseItem(self, inter):
    item = inter.component.label
    print(item)
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    consu = await inter.bot.consumables.find_one({"_id": item})
    if consu == None:
        return
    else:
        health = data["health"]
        inv = data["inventory"]
        lvl = data["level"]
        max_health = lvl * 2 / 0.5 + 20

        new_health = health + consu["heal"]
        if new_health >= max_health:
            new_health = max_health
        new_inv = []
        for i in inv:
            new_inv.append(i)
        new_inv.remove(item)
        print(f"{new_health}\n{new_inv}")
        info = {"inventory": new_inv, "health": new_health}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

        em = disnake.Embed(
            description=f"You used **{item}**",
            color=0x0077ff
        )
        await inter.send(embed=em)

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="buy new items here!")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def shop(self, inter):
        await utils.create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        location = data["location"]
        view = Shopbtn()
        em = disnake.Embed(
            title=f"{location}'s Shop!",
            color=0x0077ff,
            description="Choose a category to buy a item from"
        )
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1046934688914210906/unknown.png")
        await inter.send(embed=em, view=view)

    @commands.slash_command(description="Open your crates!")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def crates(self, inter):
        await utils.create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        standard = data["standard crate"]
        determin = data["determination crate"]
        soul = data["soul crate"]
        void = data["void crate"]
        event = data["event crate"]
        embed = disnake.Embed(
            title="Your crates",
            description="You can earn crates by exploring, voting, defeating bosses or in events",
            color=0x0077ff,
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/900274624594575361/1024789274840813568/Untitled379_202209282004321.png")
        embed.add_field(
            name="Your boxes",
            value=f"""
                Standard crates: {standard}
                Determination crates: {determin}
                Soul crates: {soul}
                Void crates: {void}
                Event crates: {event}
            """
        )
        embed.add_field(
            name="How to get",
            value=f"""
                (Voting)
                (/explore)
                (Bosses)
                (Resets)
                (Events)
            """
        )

        view = Cratesbtn()
        await inter.send(view=view, embed=embed, ephemeral=True)

        await view.wait()
        if view.value == None:
            return await inter.edit_original_message("You took to long to reply!")
        else:
            crates = fileIO("data/crates.json", "load")
            image = crates[view.value]["image"]
            if data[view.value] <= 0:
                return await inter.edit_original_message(
                    content=f"You don't have any **{view.value}**",
                    embed=None,
                    components=[]
                )
            
            data[view.value] -= 1
            earned_gold = crates[view.value]["gold"] * data["multi_g"]
            gold = data["gold"] + earned_gold

            info = {"gold": gold, view.value: data[view.value]}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            await inter.edit_original_message(
                content=f"You are opening a **{view.value}**...",
                embed=None,
                components=[]
            )

            em = disnake.Embed(
                title=f"You opened a {view.value}!",
                color=0x0077ff,
                description=f"""
                    You found the following inside the crate.

                    Gold: {round(earned_gold)}
                    Items: None
                """
            )
            em.set_thumbnail(url=image)

            await asyncio.sleep(3)
            await inter.edit_original_message(
                content=None,
                embed=em
            )

    @commands.slash_command(description="check all items in your inventory")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def inventory(self, inter):
        await utils.create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        inv = data["inventory"]
        if len(inv) == None:
            inv = "None"
        else:
            inv = "".join(f" `{item}` • " for item in inv)

        em = disnake.Embed(
            title=f"{inter.user.name}'s inventory",
            color=0x0077ff,
            description=f"{inv}"
        )
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1034392719675633745/unknown.png")

        await inter.send(embed=em)

    @commands.slash_command(description="equip/use items from your inventorys")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def use(self, inter):
        await utils.create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        inv = data["inventory"]

        view = Usebtn(inv)

        em = disnake.Embed(
            title="Use a item",
            color=0x0077ff
        )
        em.set_thumbnail(url="https://media.discordapp.net/attachments/900274624594575361/1034392719675633745/unknown.png?width=671&height=676")

        await inter.send(embed=em, view=view)

def setup(bot):
    bot.add_cog(Shop(bot))
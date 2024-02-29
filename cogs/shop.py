import asyncio
import typing

import disnake
from disnake.ext import commands
from disnake.ui import Button
from main import UndertaleBot
from utility.constants import BLUE

from utility.dataIO import fileIO
from utility.utils import create_player_info, in_battle, InFight


class Loading(disnake.ui.View):
    def __init__(self):
        super().__init__()

    @disnake.ui.button(
        emoji="<a:loading:1033856122345508874>",
        style=disnake.ButtonStyle.gray,
        disabled=True,
    )
    async def loading(self):
        return


class Cratesbtn(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="Standard crate", style=disnake.ButtonStyle.secondary)
    async def standard(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = "standard crate"
        self.stop()

    @disnake.ui.button(label="Determination crate", style=disnake.ButtonStyle.secondary)
    async def determination(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = "determination crate"
        self.stop()

    @disnake.ui.button(label="Soul crate", style=disnake.ButtonStyle.secondary)
    async def soul(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = "soul crate"
        self.stop()

    @disnake.ui.button(label="Void crate", style=disnake.ButtonStyle.secondary)
    async def void(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = "void crate"
        self.stop()

    @disnake.ui.button(label="Event crate", style=disnake.ButtonStyle.secondary)
    async def event(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = "event crate"
        self.stop()


class Shopbtn(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__()

    @disnake.ui.button(
        label="Consumables", emoji="🍎", style=disnake.ButtonStyle.secondary
    )
    async def consumables(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        await inter.response.defer()
        await Consumables(self, inter, button)
        return

    @disnake.ui.button(label="Armor", emoji="🔰", style=disnake.ButtonStyle.secondary)
    async def armor(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await Armor(self, inter, button)
        return

    @disnake.ui.button(label="Weapons", emoji="🪓", style=disnake.ButtonStyle.secondary)
    async def weapons(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        await inter.response.defer()
        await Weapons(self, inter, button)
        return


async def Consumables(
    self, inter: disnake.ApplicationCommandInteraction, button: disnake.ui.Button
):
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    consumables = fileIO("./data/consumables.json", "load")

    embed = disnake.Embed(title=f"{location}'s Shop", color=BLUE)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/900274624594575361/1046934688914210906/unknown.png"
    )

    items = []
    for item in consumables[location]:
        items.append(item)
        item_name = consumables[location][item]["name"]
        item_heal = consumables[location][item]["heal"]
        item_price = consumables[location][item]["price"]
        embed.add_field(
            name=item_name, value=f"Heal: **{item_heal}**\nPrice: **{item_price}**"
        )

    view = Consbtn(location, items)
    await inter.edit_original_message(embed=embed, view=view)


class Consbtn(disnake.ui.View):
    def __init__(self, location: str, items: typing.List[str]) -> None:
        super().__init__(timeout=None)

        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await ConsBuy(self, inter)

        consumables = fileIO("./data/consumables.json", "load")
        for item in items:
            item_name = consumables[location][item]["name"]
            button = Button(
                label=str(item_name), style=disnake.ButtonStyle.gray, custom_id=item
            )
            button.callback = shared_callback
            self.add_item(button)


async def ConsBuy(self, inter: disnake.MessageInteraction):
    item = inter.component.custom_id
    data = await inter.bot.players.find_one({"_id": inter.author.id})

    if data["in_fight"]:
        embed = disnake.Embed(
            title="You have a fight dialogue open",
            description=f"Did the fight message get deleted or can you not find it anymore?\nYou can click the button below to end your fight.\n- gold will be removed\n- health will be taken away\n- death count will go up by 1",
            color=0x0077FF,
        )

        view = InFight()
        await inter.send(embed=embed, view=view, ephemeral=True)
        return

    location = data["location"]
    consumables = fileIO("./data/consumables.json", "load")
    item_name = consumables[location][item]["name"]
    item_cost = consumables[location][item]["price"]
    gold = data["gold"]

    if item_cost > gold:
        return await inter.send("You do not have enough gold for that!")

    inv = data["inventory"]
    if len(inv) >= 25:
        return await inter.send(
            "Your inventory is full! You can have a max of 25 items"
        )
    new_inv = []
    new_inv.append(item)
    for i in inv:
        new_inv.append(i)

    new_gold = gold - item_cost

    info = {"gold": new_gold, "inventory": new_inv}
    await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

    embed = disnake.Embed(
        description=f"You bought **{item_name}** for **{item_cost}G**\n\nBalance: **{new_gold}G**",
        color=BLUE,
    )
    await inter.send(embed=embed, ephemeral=True)


async def Armor(self, inter: disnake.MessageInteraction, button: disnake.ui.Button):
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    armor = fileIO("./data/items.json", "load")

    embed = disnake.Embed(title=f"{location}'s Shop", color=BLUE)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/900274624594575361/1046934688914210906/unknown.png"
    )

    items = []
    for item in armor[location]["armor"]:
        items.append(item)
        item_name = armor[location]["armor"][item]["name"]
        item_min_def = armor[location]["armor"][item]["min_def"]
        item_max_def = armor[location]["armor"][item]["max_def"]
        item_price = armor[location]["armor"][item]["price"]
        embed.add_field(
            name=item_name,
            value=f"Min defence: **{item_min_def}**\nMax defence: **{item_max_def}**\nPrice: **{item_price}**",
        )

    view = Armorbtn(location, items)
    await inter.edit_original_message(embed=embed, view=view)


class Armorbtn(disnake.ui.View):
    def __init__(self, location: str, items: typing.List[str]) -> None:
        super().__init__(timeout=None)

        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await ArmorBuy(self, inter)

        itemsfile = fileIO("./data/items.json", "load")
        for item in items:
            item_name = itemsfile[location]["armor"][item]["name"]
            button = Button(
                label=str(item_name), style=disnake.ButtonStyle.gray, custom_id=item
            )
            button.callback = shared_callback
            self.add_item(button)


async def ArmorBuy(self, inter: disnake.MessageInteraction):
    item = inter.component.custom_id
    data = await inter.bot.players.find_one({"_id": inter.author.id})

    if data["in_fight"]:
        embed = disnake.Embed(
            title="You have a fight dialogue open",
            description=f"Did the fight message get deleted or can you not find it anymore?\nYou can click the button below to end your fight.\n- gold will be removed\n- health will be taken away\n- death count will go up by 1",
            color=0x0077FF,
        )

        view = InFight()
        await inter.send(embed=embed, view=view, ephemeral=True)
        return

    location = data["location"]
    items = fileIO("./data/items.json", "load")
    item_name = items[location]["armor"][item]["name"]
    item_cost = items[location]["armor"][item]["price"]
    gold = data["gold"]

    if item_cost > gold:
        return await inter.send("You do not have enough gold for that!")

    inv = data["inventory"]
    if len(inv) >= 25:
        return await inter.send(
            "Your inventory is full! You can have a max of 25 items"
        )
    new_inv = []
    new_inv.append(item)
    for i in inv:
        new_inv.append(i)

    new_gold = gold - item_cost

    info = {"gold": new_gold, "inventory": new_inv}
    await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

    embed = disnake.Embed(
        description=f"You bought **{item_name}** for **{item_cost}G**\n\nBalance: **{new_gold}G**",
        color=BLUE,
    )
    await inter.send(embed=embed, ephemeral=True)


async def Weapons(self, inter: disnake.MessageInteraction, button: disnake.ui.Button):
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    location = data["location"]
    weapons = fileIO("./data/items.json", "load")

    embed = disnake.Embed(title=f"{location}'s Shop", color=BLUE)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/900274624594575361/1046934688914210906/unknown.png"
    )

    items = []
    for item in weapons[location]["weapons"]:
        items.append(item)
        item_name = weapons[location]["weapons"][item]["name"]
        item_min_dmg = weapons[location]["weapons"][item]["min_dmg"]
        item_max_dmg = weapons[location]["weapons"][item]["max_dmg"]
        item_price = weapons[location]["weapons"][item]["price"]
        embed.add_field(
            name=item_name,
            value=f"Min attack: **{item_min_dmg}**\nMax attack: **{item_max_dmg}**\nPrice: **{item_price}**",
        )

    view = weaponsbtn(location, items)
    await inter.edit_original_message(embed=embed, view=view)


class weaponsbtn(disnake.ui.View):
    def __init__(self, location: str, items: typing.List[str]) -> None:
        super().__init__(timeout=None)

        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await weaponsBuy(self, inter)

        itemsfile = fileIO("./data/items.json", "load")
        for item in items:
            item_name = itemsfile[location]["weapons"][item]["name"]
            button = Button(
                label=str(item_name), style=disnake.ButtonStyle.gray, custom_id=item
            )
            button.callback = shared_callback
            self.add_item(button)


async def weaponsBuy(self, inter: disnake.MessageInteraction):
    item = inter.component.custom_id
    data = await inter.bot.players.find_one({"_id": inter.author.id})

    if data["in_fight"]:
        embed = disnake.Embed(
            title="You have a fight dialogue open",
            description=f"Did the fight message get deleted or can you not find it anymore?\nYou can click the button below to end your fight.\n- gold will be removed\n- health will be taken away\n- death count will go up by 1",
            color=0x0077FF,
        )

        view = InFight()
        await inter.send(embed=embed, view=view, ephemeral=True)
        return

    location = data["location"]
    items = fileIO("./data/items.json", "load")
    item_name = items[location]["weapons"][item]["name"]
    item_cost = items[location]["weapons"][item]["price"]
    gold = data["gold"]

    if item_cost > gold:
        return await inter.send("You do not have enough gold for that!")

    inv = data["inventory"]
    if len(inv) >= 25:
        return await inter.send(
            "Your inventory is full! You can have a max of 25 items"
        )
    new_inv = []
    new_inv.append(item)
    for i in inv:
        new_inv.append(i)
    new_gold = gold - item_cost

    info = {"gold": new_gold, "inventory": new_inv}
    await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

    embed = disnake.Embed(
        description=f"You bought **{item_name}** for **{item_cost}G**\n\nBalance: **{new_gold}G**",
        color=BLUE,
    )
    await inter.send(embed=embed, ephemeral=True)


class Usebtn(disnake.ui.View):
    def __init__(self, inv: typing.List[str]) -> None:
        super().__init__(timeout=None)

        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await UseItem(self, inter)

        inv_dict = {i:inv.count(i) for i in inv}
        for key in inv_dict:
            value = inv_dict[key]

            button = Button(label=f"{key}: {value}", style=disnake.ButtonStyle.gray, custom_id=key)
            button.callback = shared_callback
            self.add_item(button)


async def UseItem(self, inter: disnake.MessageInteraction):
    item = inter.component.custom_id
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    consu = await inter.bot.consumables.find_one({"_id": item})
    if consu is None:
        armors = await inter.bot.armor.find_one({"_id": item})
        if armors == None:
            weapon = data["weapon"]
            inv = data["inventory"]

            new_inv = [i for i in inv]

            new_inv.remove(item)
            new_inv.append(weapon)
            new_weapon = item
            info = {"inventory": new_inv, "weapon": new_weapon}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            embed = disnake.Embed(description=f"You equipped {item}", color=BLUE)
            await inter.send(embed=embed)

        else:
            armor = data["armor"]
            inv = data["inventory"]

            new_inv = [i for i in inv]

            new_inv.remove(item)
            new_inv.append(armor)
            new_armor = item
            info = {"inventory": new_inv, "armor": new_armor}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            embed = disnake.Embed(description=f"You equipped {item}", color=BLUE)
            await inter.send(embed=embed)

    else:
        health = data["health"]
        inv = data["inventory"]
        lvl = data["level"]
        max_health = lvl * 2 / 0.5 + 20

        new_health = health + consu["heal"]
        if new_health >= max_health:
            new_health = max_health

        new_inv = [i for i in inv]

        new_inv.remove(item)
        info = {"inventory": new_inv, "health": new_health}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

        embed = disnake.Embed(description=f"You used **{item}**\nYour health: **{round(new_health)}/{round(max_health)}**", color=BLUE)
        await inter.send(embed=embed)
    inv = new_inv
    view = Usebtn(inv)
    await inter.edit_original_message(view=view)


class Sellbtn(disnake.ui.View):
    def __init__(self, inv) -> None:
        super().__init__(timeout=None)
        async def shared_callback(inter: disnake.MessageInteraction) -> None:
            await inter.response.defer()
            await SellItem(self, inter)

        inv_dict = {i:inv.count(i) for i in inv}
        for key in inv_dict:
            value = inv_dict[key]
            
            button = Button(label=f"{key}: {value}", style=disnake.ButtonStyle.gray, custom_id=key)
            button.callback = shared_callback
            self.add_item(button)

async def SellItem(self, inter):
    item = inter.component.custom_id
    data = await inter.bot.players.find_one({"_id": inter.author.id})
    gold = data["gold"]
    consu = await inter.bot.consumables.find_one({"_id": item})
    if consu == None:
        armors = await inter.bot.armor.find_one({"_id": item})
        if armors == None:
            weapons = await inter.bot.weapons.find_one({"_id": item})
            inv = data["inventory"]
            price = weapons["price"]

            new_inv = []
            for i in inv:
                new_inv.append(i)
            new_inv.remove(item)
            new_price = gold+price/2
            info = {"inventory": new_inv, "gold": new_price}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            em = disnake.Embed(
                description=f"You sold **{item}**\nfor **{price/2}G**",
                color=0x0077ff
            )
            await inter.send(embed=em)
        else: 
            price = armors["price"]
            inv = data["inventory"]

            new_inv = []
            for i in inv:
                new_inv.append(i)
            new_inv.remove(item)
            new_price = gold+price/2
            info = {"inventory": new_inv, "gold": new_price}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            em = disnake.Embed(
                description=f"You sold **{item}**\nfor **{price/2}G**",
                color=0x0077ff
            )
            await inter.send(embed=em)
    else:
        price = consu["price"]
        inv = data["inventory"]

        new_inv = []
        for i in inv:
            new_inv.append(i)
        new_inv.remove(item)
        new_price = gold+price/2
        info = {"inventory": new_inv, "gold": new_price}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

        em = disnake.Embed(
            description=f"You sold **{item}**\nfor **{price/2}G**",
            color=0x0077ff
        )
        await inter.send(embed=em)
    inv = new_inv
    view = Usebtn(inv)
    await inter.edit_original_message(view=view)

class Shop(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot

    @in_battle()
    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def shop(self, inter: disnake.ApplicationCommandInteraction):
        """Buy new items here!"""
        await create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        location = data["location"]
        view = Shopbtn()
        embed = disnake.Embed(
            title=f"{location}'s Shop!",
            color=BLUE,
            description="Choose a category to buy a item from.",
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/900274624594575361/1046934688914210906/unknown.png"
        )
        await inter.send(embed=embed, view=view)

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def crates(self, inter: disnake.ApplicationCommandInteraction):
        """Open your crates!"""
        await create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        standard = data["standard crate"]
        determin = data["determination crate"]
        soul = data["soul crate"]
        void = data["void crate"]
        event = data["event crate"]
        embed = disnake.Embed(
            title="Your crates",
            description="You can earn crates by exploring, voting, defeating bosses or in events.",
            color=BLUE,
        )
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/900274624594575361/1024789274840813568/Untitled379_202209282004321.png"
        )
        embed.add_field(
            name="Your boxes",
            value=f"""
                Standard crates: {standard}
                Determination crates: {determin}
                Soul crates: {soul}
                Void crates: {void}
                Event crates: {event}
            """,
        )
        embed.add_field(
            name="How to get",
            value=f"""
                (Voting)
                (/explore)
                (Bosses)
                (Resets)
                (Events)
            """,
        )

        view = Cratesbtn()
        await inter.send(view=view, embed=embed, ephemeral=True)

        await view.wait()
        if view.value is None:
            return await inter.edit_original_message("You took to long to reply!")

        crates = fileIO("data/crates.json", "load")
        image = crates[view.value]["image"]
        if data[view.value] <= 0:
            return await inter.edit_original_message(
                content=f"You don't have any **{view.value}**",
                embed=None,
                components=[],
            )

        data[view.value] -= 1
        earned_gold = crates[view.value]["gold"] * data["multi_g"]
        gold = data["gold"] + earned_gold

        info = {"gold": gold, view.value: data[view.value]}
        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

        await inter.edit_original_message(
            content=f"You are opening a **{view.value}**...",
            embed=None,
            components=[],
        )

        embed = disnake.Embed(
            title=f"You opened a {view.value}!",
            color=BLUE,
            description=f"""
                You found the following inside the crate.

                Gold: {round(earned_gold)}
                Items: None
            """,
        )
        embed.set_thumbnail(url=image)

        await asyncio.sleep(3)
        await inter.edit_original_message(content=None, embed=embed)

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def inventory(self, inter: disnake.ApplicationCommandInteraction):
        """Check all items in your inventory."""
        await create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        inv = data["inventory"]
        inv_dict = {i:inv.count(i) for i in inv}
        if len(inv) == 0:
            inv = "None"

        else:
            inv = ""
            for key in inv_dict:
                value = inv_dict[key]
                inv += f"**{key}**: {value}\n"

        embed = disnake.Embed(title=f"{inter.user.name}'s inventory", color=BLUE, description=f"{inv}")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/900274624594575361/1034392719675633745/unknown.png")

        await inter.send(embed=embed)

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def use(self, inter: disnake.ApplicationCommandInteraction):
        """Equip/use items from your inventory."""
        await create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        inv = data["inventory"]

        view = Usebtn(inv)

        embed = disnake.Embed(title="Use a item", color=BLUE)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/900274624594575361/1034392719675633745/unknown.png?width=671&height=676"
        )

        await inter.send(embed=embed, view=view)

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def sell(self, inter):
        """sell items"""
        await create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        inv = data["inventory"]

        view = Sellbtn(inv)

        em = disnake.Embed(
            title="Sell a item",
            color=0x0077ff
        )
        em.set_thumbnail(url="https://media.discordapp.net/attachments/900274624594575361/1034392719675633745/unknown.png?width=671&height=676")

        await inter.send(embed=em, view=view)

def setup(bot):
    bot.add_cog(Shop(bot))
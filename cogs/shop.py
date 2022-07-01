import disnake
import asyncio
import time

from disnake.ext import commands, components
from disnake.ui import Button, ActionRow
from disnake import ButtonStyle

from utility.utils import occurrence, in_shop, in_battle, create_player_info


class ShopMenu:
    def __init__(
            self,
            bot,
            inter,
            author,
            msg,
            channel,
            data,
            shop
    ):
        self.bot = bot
        self.inter = inter
        self.author = author
        self.msg = msg
        self.shop = shop
        self.channel = channel
        self.edit = msg.edit
        self.data = data
        self.latest_inter = None
        self.time = int(time.time())
        self.menus = []

    async def menu(self):
        comps = [
            Button(
                label="Buy",
                custom_id=ShopCog.shop_listener.build_custom_id(
                    action="buy",
                    uid=str(self.author.id)
                ),
                style=ButtonStyle.green
            ),
            Button(
                label="Talk",
                custom_id=ShopCog.shop_listener.build_custom_id(
                    action="talk",
                    uid=str(self.author.id)
                ),
                disabled=True
            ),
            Button(
                label="Sell",
                custom_id=ShopCog.shop_listener.build_custom_id(
                    action="sell",
                    uid=str(self.author.id)
                )
            ),
            Button(
                label="End",
                custom_id=ShopCog.shop_listener.build_custom_id(
                    action="end",
                    uid=str(self.author.id)
                ),
                style=ButtonStyle.red
            )
        ]
        embed = disnake.Embed(
            title=f"Welcome to the {self.shop}",
            description=self.data["s_talk"],
            color=disnake.Color.random()
        )
        embed.set_thumbnail(url=self.data["image"])

        await self.edit(embed=embed, components=[comps])

    async def buy(self):
        info = await self.bot.players.find_one({"_id": self.author.id})
        if len(info["inventory"]) >= 10:
            await self.latest_inter.send(content="You don't have enough inventory", ephemeral=True)
            return await self.menu()

        items_list = []
        gold = info["gold"]

        for i in self.data["items"]:
            items_list.append(i)
        s_talk = self.data["s_talk"]
        embed = disnake.Embed(
            title="Shop",
            description=f"{s_talk}\n\nYour gold: **{int(gold)}**",
            color=disnake.Colour.random(),
        )

        embed.set_thumbnail(self.data["image"])

        rows = []
        lista = []
        for item in items_list:
            price = self.data["items"][item]
            if price > info["gold"]:
                lista.append(
                    Button(
                        label=f"{item.title()} | {price} G",
                        style=ButtonStyle.red,
                        disabled=True
                    )
                )
            else:
                lista.append(
                    Button(
                        label=f"{item.title()} | {price} G",
                        custom_id=ShopCog.selected.build_custom_id(
                            item=item.lower(),
                            uid=self.author.id
                        ),
                        style=ButtonStyle.grey
                    )
                )
        lista.append(
            Button(
                label="Go Back",
                custom_id=ShopCog.shutdown.build_custom_id(uid=str(self.author.id)),
                style=ButtonStyle.red)
        )

        for i in range(0, len(lista), 5):
            rows.append(ActionRow(*lista[i: i + 5]))

        msg = await self.edit(embed=embed, components=rows)

        self.menus.append(msg.id)
        await asyncio.sleep(60)

        if msg.id in self.menus:
            await msg.edit(content=f"{self.author.mention} You took to long to reply", components=[])
            return await self.timeout()
        return

    async def talk(self):
        await self.edit(content="How tf r u here?")

    async def sell(self):
        info = await self.bot.players.find_one({"_id": self.author.id})
        items = [key for key in info["inventory"]]
        if not items:
            await self.latest_inter.send("You don't have anything to sell!", ephemeral=True)
            await asyncio.sleep(3)
            return await self.menu()

        s_talk = self.data["s_talk"]
        embed = disnake.Embed(
            title="Shop",
            description=f"{s_talk}, Selling dialogue!",
            color=disnake.Colour.random(),
        )
        embed.set_thumbnail(url=self.data["image"])

        rows = []
        lista = []
        inventory = []
        store = {}
        for data in info["inventory"]:
            occurrence(store, data)
        for k, v in store.items():
            inventory.append({f"{k}": f"{v}x"})
        for item in inventory:
            for key in item:
                price = self.bot.items[key]["price"]
                lista.append(
                    Button(
                        label=f"{key.title()} {item[key]} | {price / 2}",
                        custom_id=ShopCog.s_selected.build_custom_id(item=key.lower(), uid=self.author.id),
                        style=ButtonStyle.grey,
                    )
                )

        lista.append(
            Button(
                label="Go Back",
                custom_id=ShopCog.shutdown.build_custom_id(uid=str(self.author.id)),
                style=ButtonStyle.red)
        )

        for i in range(0, len(lista), 5):
            rows.append(ActionRow(*lista[i: i + 5]))

        msg = await self.edit(embed=embed, components=rows)

        self.menus.append(msg.id)
        await asyncio.sleep(60)

        if msg.id in self.menus:
            return await self.timeout()
        return

    async def end(self):
        await self.edit(content="Shop is closed", components=[])
        if str(self.author.id) not in self.bot.shops:
            return
        del self.bot.shops[str(self.author.id)]

    async def timeout(self):
        await self.edit(content=f"{self.author.mention} You took to long to reply", components=[])
        if str(self.author.id) not in self.bot.shops:
            return
        del self.bot.shops[str(self.author.id)]
        return


class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    @in_shop()
    @in_battle()
    async def shop(self, inter):
        await create_player_info(inter, inter.author)
        info = await self.bot.players.find_one({"_id": inter.author.id})

        location = info["location"]
        lista = []
        if location not in inter.bot.shopping:
            return await inter.send("There is no shops out here!")

        for i in inter.bot.shopping[location]:
            lista.append(
                Button(
                    label=i.title(),
                    custom_id=ShopCog.shop_selector_listener.build_custom_id(
                        shop=i,
                        loc=location,
                        uid=str(inter.author.id)
                    )
                )
            )

        await inter.send("Select a Shop", components=[lista])

    @components.button_listener()
    async def shutdown(self, inter: disnake.MessageInteraction, uid: str) -> None:
        if inter.author.id != int(uid):
            await inter.send('This is not your kiddo!', ephemeral=True)
            return

        await inter.response.defer()

        return await inter.bot.shops[uid].menu()

    @components.button_listener()
    async def shop_listener(self, inter: disnake.MessageInteraction, action: str, uid: str) -> None:
        if str(inter.author.id) != uid:
            return await inter.send("This is not yours kiddo!", ephemeral=True)

        # noinspection PyUnresolvedReferences
        try:
            await inter.response.defer()
        except:
            pass

        inter.bot.shops[uid].latest_inter = inter
        await getattr(inter.bot.shops[uid], action)()

    @components.button_listener()
    async def shop_selector_listener(self, inter: disnake.MessageInteraction, shop: str, loc: str, uid: str) -> None:
        if str(inter.author.id) != uid:
            return await inter.send("This is not yours kiddo!", ephemeral=True)

        data = inter.bot.shopping[loc][shop]

        try:
            await inter.response.defer()
        except:
            pass

        msg = await inter.original_message()
        shop_obj = ShopMenu(inter.bot, inter, inter.author, msg, inter.channel, data, shop)
        shop_obj.bot.shops[str(inter.author.id)] = shop_obj
        print(f"{str(inter.author)} has entered a shop")
        await shop_obj.menu()

    @components.button_listener()
    async def selected(self, inter: disnake.MessageInteraction, item: str, uid: str) -> None:
        if inter.author.id != int(uid):
            await inter.send('This is not your kiddo!', ephemeral=True)
            return

        try:
            msg_id = inter.bot.shops[uid].menus[0]
            inter.bot.shops[uid].menus.remove(msg_id)
        except:
            pass

        incoming = await inter.bot.players.find_one({"_id": inter.author.id})
        price = inter.bot.shops[uid].data["items"][item.lower()]

        try:
            await inter.response.defer()
        except:
            pass

        if incoming["gold"] < price:
            return await inter.send("Your gold is not enough.", ephemeral=True)

        if len(incoming["inventory"]) >= 10:
            return await inter.send("You are carrying alot of items.", ephemeral=True)

        incoming["gold"] -= price
        gold = incoming["gold"]
        incoming["inventory"].append(item)

        incoming = {
            "inventory": incoming["inventory"],
            "gold": incoming["gold"]
        }
        await inter.bot.players.update_one(
            {"_id": inter.author.id}, {"$set": incoming}
        )
        s_talk = inter.bot.shops[uid].data["s_talk"]
        emb = disnake.Embed(
            title="Shop",
            description=f"{s_talk}\n\nYour gold: **{int(gold)}**",
            color=disnake.Colour.random(),
        )

        emb.set_thumbnail(inter.bot.shops[uid].data["image"])
        await inter.edit_original_message(embed=emb)
        await inter.send(f"Successfully bought **{item}**", ephemeral=True)

    @components.button_listener()
    async def s_selected(self, inter: disnake.MessageInteraction, item: str, uid: str) -> None:
        if inter.author.id != int(uid):
            await inter.send('This is not your kiddo!', ephemeral=True)
            return

        try:
            msg_id = inter.bot.shops[uid].menus[0]
            inter.bot.shops[uid].menus.remove(msg_id)
        except:
            pass

        info = await inter.bot.players.find_one({"_id": inter.author.id})

        returned = inter.bot.items[item]["price"] / 2
        try:
            info["inventory"].remove(item)
        except:
            return

        info["gold"] = info["gold"] + returned

        output = {
            "gold": info["gold"],
            "inventory": info["inventory"]
        }
        await inter.response.defer()

        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": output})

        await inter.send(f"You sold {item} for {round(returned, 1)} G", ephemeral=True)
        if len(info["inventory"]) <= 0:
            return

        return await inter.bot.shops[uid].sell()


def setup(bot):
    bot.add_cog(ShopCog(bot))

import asyncio

import disnake
from disnake.ext import commands, components

from disnake import ButtonStyle
from disnake.ui import Button, ActionRow
from utility.utils import occurrence, in_shop, in_battle, create_player_info


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    async def weapon(self, inter, item):
        data = await self.bot.players.find_one({"_id": inter.author.id})
        data["inventory"].remove(item)
        data["inventory"].append(data["weapon"])
        data = {
            "weapon": item,
            "inventory": data["inventory"]
        }
        await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
        return await inter.send(f"Successfully equipped {item.title()}")

    async def armor(self, inter, item):
        data = await self.bot.players.find_one({"_id": inter.author.id})
        data["inventory"].remove(item)
        data["inventory"].append(data["armor"])

        data = {
            "armor": item,
            "inventory": data["inventory"]
        }
        await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
        return await inter.send(f"Successfully equipped {item.title()}")

    async def food(self, inter, item):
        data = await self.bot.players.find_one({"_id": inter.author.id})
        data["inventory"].remove(item)
        heal = self.bot.items[item]["HP"]
        data["health"] += heal
        lvl = data["level"]

        if data["health"] >= self.bot.levels[str(lvl)]["HP"]:
            data["health"] = self.bot.levels[str(lvl)]["HP"]
            data = {
                "health": self.bot.levels[str(lvl)]["HP"],
                "inventory": data["inventory"]
            }
            await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
            await inter.send("Your health maxed out")
            return
        health = data["health"]
        data = {
            "health": health,
            "inventory": data["inventory"]
        }
        await self.bot.players.update_one({"_id": inter.author.id}, {"$set": data})
        return await inter.send(
            f"You consumed {item}, restored {heal}HP\n\nCurrent health: {health}HP"
        )

    @commands.command(aliases=["inv"])
    async def inventory(self, inter):
        """Shows your inventory"""
        author = inter.author
        await create_player_info(inter, inter.author)
        info = await self.bot.players.find_one({"_id": author.id})

        gold = info["gold"]

        # func
        store = {}
        inventory = ""
        for data in info["inventory"]:
            occurrence(store, data)
        for k, v in store.items():
            inventory += f"{k} {v}x\n"

        em = disnake.Embed(title="Your Inventory", color=disnake.Colour.random())
        em.add_field(name="▫️┃Gold:", value=f"**{int(gold)}**", inline=False)
        em.add_field(name="📦┃Items:", value=f"**{inventory}**", inline=False)
        em.set_thumbnail(url=inter.author.display_avatar)

        await inter.send(embed=em)

    @commands.command(aliases=["equip", "heal"])
    @in_shop()
    @in_battle()
    async def use(self, inter, *, item: str = None):

        await create_player_info(inter, inter.author)
        if item is None:
            data = await inter.bot.players.find_one({"_id": inter.author.id})
            if len(data["inventory"]) == 0:
                return await inter.send("You have nothing to use")
            items_list = []
            for i in data["inventory"]:
                items_list.append(i)

            embed = disnake.Embed(
                title="Inventory",
                description="Welcome to your Inventory!",
                color=disnake.Colour.random(),
            )

            rows = []
            lista = []
            inventory = []
            store = {}
            for data in data["inventory"]:
                occurrence(store, data)

            for k, v in store.items():
                inventory.append({f"{k}": f"{v}x"})

            for item in inventory:
                for key in item:
                    lista.append(
                        Button(
                            label=f"{key.title()} {item[key]}",
                            custom_id=await self.u_selected.build_custom_id(
                                item=key.lower(),
                                uid=inter.author.id
                            ),
                            style=ButtonStyle.grey,
                        )
                    )

            for i in range(0, len(lista), 5):
                rows.append(ActionRow(*lista[i: i + 5]))

            await inter.send(embed=embed, components=rows)
            return

        item = item.lower()
        if item not in self.bot.items:
            await inter.send("This item does not exist")
            return

        data = await inter.bot.players.find_one({"_id": inter.author.id})

        if len(data["inventory"]) == 0:
            await inter.send("Your inventory is empty!")
            return

        if item not in data["inventory"]:
            await inter.send("You don't have this item in your inventory!")
            return

        await getattr(Shop, self.bot.items[item]["func"])(self, inter, item)

    @components.button_listener()
    async def u_selected(self, inter: disnake.MessageInteraction, *, item: str, uid: str) -> None:
        if inter.author.id != int(uid):
            await inter.send('This is not your kiddo!', ephemeral=True)
            return

        await inter.response.defer()

        await inter.edit_original_message(components=[])
        await getattr(Shop, self.bot.items[item]["func"])(self, inter, item)

    @commands.command()
    @in_shop()
    @in_battle()
    async def open(self, inter):

        await create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        standard = data["standard crate"]
        determin = data["determination crate"]
        soul = data["soul crate"]
        void = data["void crate"]
        embed = disnake.Embed(
            title="Your boxes",
            description="You can earn boxes by fighting, voting or defeating specific bosses",
            color=disnake.Colour.blue(),
        )
        embed.add_field(
            name="Your boxes",
            value=f"""
Standard crates: {standard}
Determination crates: {determin}
soul crates: {soul}
void crates: {void}
                              """,
        )
        row = ActionRow(
            Button(
                style=ButtonStyle.grey,
                label="Standard Crate",
                custom_id=await self.c_selected.build_custom_id(
                    item="standard crate",
                    uid=inter.author.id
                ),
            ),
            Button(
                style=ButtonStyle.grey,
                label="Determination Crate",
                custom_id=await self.c_selected.build_custom_id(
                    item="determination crate",
                    uid=inter.author.id
                ),
            ),
            Button(
                style=ButtonStyle.grey,
                label="Soul Crate",
                custom_id=await self.c_selected.build_custom_id(
                    item="soul crate",
                    uid=inter.author.id
                ),
            ),
            Button(
                style=ButtonStyle.grey,
                label="Void Crate",
                custom_id=await self.c_selected.build_custom_id(
                    item="void crate",
                    uid=inter.author.id
                ),
            ),
        )
        await inter.send(embed=embed, components=[row])

    @components.button_listener()
    async def c_selected(self, inter: disnake.MessageInteraction, *, item: str, uid: str) -> None:
        if inter.author.id != int(uid):
            await inter.send('This is not your kiddo!', ephemeral=True)
            return

        data = await inter.bot.players.find_one({"_id": inter.author.id})
        await inter.response.defer()

        if data[item] == 0:
            return await inter.edit_original_message(
                content=f"You don't have any {item.title()}",
                embed=None,
                components=[],
            )

        await inter.edit_original_message(
            content=f"{inter.author.mention} opened a {item.title()}...",
            embed=None,
            components=[],
        )
        data[item] -= 1
        earned_gold = inter.bot.crates[item]["gold"] + data["level"]
        gold = data["gold"] + earned_gold
        await asyncio.sleep(3)
        await inter.edit_original_message(
            content=f"{inter.author.mention} earned {earned_gold}G from a {item.title()}"
        )
        info = {
            "gold": gold,
            item: data[item]
        }
        return await inter.bot.players.update_one(
            {"_id": inter.author.id}, {"$set": info}
        )


def setup(bot):
    bot.add_cog(Shop(bot))

import asyncio
import random
import time

import disnake
from disnake.enums import ButtonStyle
from disnake.ext import commands, components
from disnake.ui import Button, ActionRow

from utility import utils


async def count(keys, value):
    try:
        keys[str(value)] = keys[value] + 1
    except KeyError:
        keys[str(value)] = 1
        return


class Battle:
    def __init__(
            self,
            author: disnake.Member,
            bot: commands.AutoShardedBot,
            monster: str,
            monster_hp: int,
            inter: disnake.CommandInteraction,
            kind: int,
            channel: disnake.TextChannel
    ) -> None:

        self.bot = bot
        self.channel = channel
        self.author = author
        self.monster = monster
        self.inter = inter
        self.msg = None
        self.time = int(time.time())
        self.kind = kind  # 0 for monster, 1 for boss, 2 for special.
        self.menus = []
        self.monster_hp = monster_hp

    # ending the fight with the id
    async def end(self):
        if str(self.author.id) not in self.bot.fights:
            return
        del self.bot.fights[str(self.author.id)]

    async def check_levelup(self):
        info = await self.bot.players.find_one({"_id": self.author.id})
        xp = info["exp"]
        lvl = info["level"]
        lvlexp = self.bot.levels[str(lvl)]["EXP_TO_LVLUP"]
        if xp >= lvlexp:

            new_level = info["level"] + 1
            new_xp = xp - lvlexp

            data = {
                "level": new_level,
                "exp": xp - lvlexp,
            }
            await self.bot.players.update_one({"_id": self.author.id}, {"$set": data})
            if new_xp >= self.bot.levels[str(lvl + 1)]["EXP_TO_LVLUP"]:
                return await self.check_levelup()

            embed = disnake.Embed(
                title="LOVE Increased",
                description=(f"Your LOVE Increased to **{new_level}**\nDamage increased by 1"
                             f"\nHealth increased by 4"),
                color=disnake.Colour.red(),
            )
            await self.channel.send(self.author.mention, embed=embed)
            for i in self.bot.locations:
                if self.bot.locations[i]["RQ_LV"] == info["level"]:
                    await asyncio.sleep(3)
                    await self.channel.send(
                        f"{self.author.mention}\n\n" +
                        f"Congrats, You unlocked {i}, you can go there by running u?travel"
                    )
            return True
        return False

    async def menu(self):

        info = await self.bot.players.find_one({"_id": self.author.id})

        buttons = [
            disnake.ui.Button(
                style=disnake.ButtonStyle.red,
                label='Fight',
                custom_id=Fight.action.build_custom_id(action="attack", uid=self.author.id)
            ),
            disnake.ui.Button(
                style=disnake.ButtonStyle.gray,
                label='Items',
                custom_id=Fight.action.build_custom_id(action="use", uid=self.author.id)
            ),
            disnake.ui.Button(
                style=disnake.ButtonStyle.grey,
                label='Act',
                disabled=True
            ),
            disnake.ui.Button(
                style=disnake.ButtonStyle.green,
                label='Mercy',
                custom_id=Fight.action.build_custom_id(action="spare", uid=self.author.id)
            ),
        ]

        health = info["health"]
        monster = self.monster
        title = self.bot.monsters[monster]["title"]
        enemy_hp = self.monster_hp
        damage = self.bot.monsters[monster]["atk"]

        embed = disnake.Embed(
            title=f"{monster}, {title}",
            description=f"**Your HP is {health}\nMonster health: {enemy_hp}HP\ncan deal up to {damage}ATK**",
            color=disnake.Colour.blue()
        )
        image = self.bot.monsters[monster]["im"]
        embed.set_thumbnail(url=image)

        msg = await self.inter.send(self.author.mention, embed=embed, components=buttons)
        self.msg = msg

        self.menus.append(msg.id)
        await asyncio.sleep(60)

        if msg.id in self.menus:
            await msg.edit(content=f"{self.author.mention} You took to long to reply", components=[])
            return await self.end()
        return

    async def attack(self):
        event = self.bot.events
        data = self.bot.monsters
        author = self.author
        info = await self.bot.players.find_one({"_id": self.author.id})
        lvl = info["level"]
        user_wep = info["weapon"]
        monster = self.monster
        damage = self.bot.levels[str(lvl)]["AT"]
        enemy_hp = self.monster_hp

        DMG = self.bot.items[user_wep]["ATK"]

        enemy_gold = self.bot.monsters[monster]["GOLD"]
        enemy_xp = self.bot.monsters[monster]["XP"]
        atem = disnake.Embed(title="You Attack")

        # player attack
        damage = int(DMG) + int(damage)
        enemy_hp_after = int(enemy_hp) - damage
        enemy_hp_after = max(enemy_hp_after, 0)
        atem.description = f"You Damaged **{monster}**\n**-{DMG}HP**\ncurrent monster hp: **{enemy_hp_after}HP**"
        atem.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/793382520665669662/803885802588733460/image0.png"
        )
        if damage <= 0:
            atem.description = f"You Missed!"

        await self.channel.send(self.author.mention, embed=atem)
        if enemy_hp_after <= 0:
            await asyncio.sleep(1)
            embed = disnake.Embed(
                title="You Won!",
                description=f"You Earned **{int(enemy_xp)} XP** and **{int(enemy_gold)} G**",
                color=disnake.Colour.gold(),
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/850983850665836544/878997428840329246/image0.png"
            )
            xp_multi = round(info["multi_xp"], 1)
            gold_multi = round(info["multi_g"], 1)
            gold = enemy_gold
            exp = enemy_xp
            # Multiplier
            if info["multi_g"] > 1 and info["multi_xp"] > 1:
                gold = gold * info["multi_xp"]
                exp = exp * info["multi_g"]
                embed.description += (
                    f"\n\n**[MULTIPLIER]**\n> **[{xp_multi}x]** XP: **+{int(exp - enemy_xp)}**"
                    f" ({int(exp)})\n> **[{gold_multi}x]** GOLD: **+{int(gold - enemy_gold)}** ({int(gold)})")
            # booster
            if self.author.id in self.bot.boosters["boosters"]:
                exp = exp * 2
                gold = gold * 2
                embed.description += (
                    f"\n\n**[BOOSTER MULTIPLIER]**\n> **[2x]** XP: **+{int(exp - enemy_xp)}**"
                    f" ({int(exp)})\n> **[2x]** GOLD: **+{int(gold - enemy_gold)}** ({int(gold)})"
                                      )

            if event is not None:
                xp_multi = int(event["multi_xp"])
                gold_multi = int(event["multi_g"])
                gold = gold * event["multi_g"]
                exp = exp * event["multi_xp"]
                name = event["name"]

                embed.description += (
                    f"\n\n**[{name.upper()} EVENT!]**\n> **[{xp_multi}x]** XP: **+{int(exp - enemy_xp)}**"
                    f"({int(exp)})\n> **[{gold_multi}x]** GOLD: **+{int(gold - enemy_gold)}** ({int(gold)})")

            if self.kind == 1:
                location = info["location"]

                info[f"{location}_boss"] = True
                info["rest_block"] = time.time()
            else:
                location = info["location"]

                info[f"{location}_kills"] = info[f"{location}_kills"] + 1


            info["gold"] = info["gold"] + gold
            info["exp"] = info["exp"] + exp

            if len(self.bot.monsters[monster]["loot"]) > 0:
                num = random.randint(0, 6)
                crate = self.bot.monsters[monster]["loot"][0]
                if num < 2:
                    info[crate] += 1
                    embed.description += (
                        f"\n\n**You got a {crate}, check u?crate command**"
                    )
            info["kills"] = info["kills"] + 1
            await self.bot.players.update_one({"_id": author.id}, {"$set": info})
            await self.check_levelup()
            await self.channel.send(embed=embed)
            print(f"{self.author} has ended the fight")
            return await self.end()
        else:
            self.monster_hp = enemy_hp_after
            await self.bot.players.update_one({"_id": author.id}, {"$set": info})
            await asyncio.sleep(2)
            return await self.counter_attack()

    async def counter_attack(self):
        data = self.bot.monsters

        info = await self.bot.players.find_one({"_id": self.author.id})
        enemy_define = self.monster
        enemy_dmg = data[enemy_define]["atk"]
        user_ar = info["armor"].lower()
        user_dfs = self.bot.items[user_ar]["DF"]
        user_hp = info["health"]
        lvl = info["level"]
        health = "HP"

        enemy_dmg = enemy_dmg - int(user_dfs)
        if enemy_dmg <= 0:
            await self.channel.send("The monster has missed!")
            await asyncio.sleep(3)
            return await self.menu()

        atem = disnake.Embed(title=f"{enemy_define} Attacks")

        user_hp_after = int(user_hp) - int(enemy_dmg)
        gold_lost = random.randint(10, 40) + info["level"]
        atem.description = (
            f"**{enemy_define}** Attacks\n**-{enemy_dmg}HP**\ncurrent hp: **{user_hp_after}HP\n"
            f"{await utils.get_bar(user_hp_after, self.bot.levels[str(lvl)][health])}**"
        )
        atem.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/793382520665669662/803885802588733460/image0.png"
        )
        await asyncio.sleep(2)
        await self.channel.send(self.author.mention, embed=atem)

        if user_hp_after <= 0:
            info["gold"] = info["gold"] - gold_lost
            info["gold"] = max(info["gold"], 0)
            info["deaths"] = info["deaths"] + 1
            info["health"] = 20
            await self.bot.players.update_one({"_id": self.author.id}, {"$set": info})

            await asyncio.sleep(3)
            femb = disnake.Embed(
                title="You Lost <:broken_heart:865088299520753704>",
                description=f"**Stay Determines please!, You lost {gold_lost} G**",
                color=disnake.Colour.red(),
            )
            print(f"{self.author} has ended the fight (Died)")
            await self.channel.send(self.author.mention, embed=femb)
            return await self.end()
        else:
            info["health"] = user_hp_after
            await self.bot.players.update_one({"_id": self.author.id}, {"$set": info})
            await asyncio.sleep(3)
            return await self.menu()

    async def weapon(self, item):
        try:
            data = await self.bot.players.find_one({"_id": self.author.id})
            data["inventory"].remove(item)
            data["inventory"].append(data["weapon"])
            data["weapon"] = item
            await self.bot.players.update_one({"_id": self.author.id}, {"$set": data})
            await self.channel.send(f"Successfully equipped {item.title()}")

            return await self.counter_attack()
        except Exception as e:
            await self.bot.get_channel(827651947678269510).send(e)
            await self.end()

    async def armor(self, item):
        try:

            data = await self.bot.players.find_one({"_id": self.author.id})
            data["inventory"].remove(item)
            data["inventory"].append(data["armor"])

            data["armor"] = item
            await self.bot.players.update_one({"_id": self.author.id}, {"$set": data})
            await self.channel.send(f"Successfully equipped {item.title()}")

            return await self.counter_attack()

        except Exception as e:
            await self.bot.get_channel(827651947678269510).send(e)
            await self.end()

    async def food(self, item):
        try:
            data = await self.bot.players.find_one({"_id": self.author.id})
            lvl = data["level"]
            data["inventory"].remove(item)
            heal = self.bot.items[item]["HP"]
            data["health"] += heal

            if data["health"] >= self.bot.levels[str(lvl)]["HP"]:
                data["health"] = self.bot.levels[str(lvl)]["HP"]
                await self.bot.players.update_one({"_id": self.author.id}, {"$set": data})
                await self.channel.send("Your health maxed out")
                return await self.counter_attack()

            health = data["health"]
            await self.bot.players.update_one({"_id": self.author.id}, {"$set": data})
            await self.channel.send(
                f"You consumed {item}, restored {heal}HP\n\nCurrent health: {health}HP"
            )
            return await self.counter_attack()

        except Exception as e:
            await self.bot.get_channel(827651947678269510).send(e)
            await self.end()

    async def use(self):
        await utils.create_player_info(self.inter, self.author)
        data = await self.bot.players.find_one({"_id": self.author.id})
        if len(data["inventory"]) == 0:
            await self.channel.send(f"{self.author.mention} You have nothing to use")
            await asyncio.sleep(3)
            return await self.menu()

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
        keys = {}
        for data in data["inventory"]:
            await count(keys, data)
        for k, v in keys.items():
            inventory.append({f"{k}": f"{v}x"})
        for item in inventory:
            for key in item:
                lista.append(
                    Button(
                        label=f"{key.title()} {item[key]}",
                        custom_id=Fight.food.build_custom_id(item=key.lower(), uid=self.author.id),
                        style=ButtonStyle.grey
                    )
                )

        lista.append(
            Button(label=f"Return",
                   custom_id=Fight.food.build_custom_id(
                       item="back",
                       uid=self.author.id),
                   style=ButtonStyle.green
                   )
        )
        for i in range(0, len(lista), 5):
            rows.append(ActionRow(*lista[i: i + 5]))

        msg = await self.channel.send(embed=embed, components=rows)

        self.menus.append(msg.id)
        await asyncio.sleep(60)

        if msg.id in self.menus:
            await msg.edit(content=f"{self.author.mention} You took to long to reply", components=[])
            return await self.end()
        return

    async def spare(self):
        try:
            info = await self.bot.players.find_one({"_id": self.author.id})
            monster = self.monster

            if monster == "sans":
                await self.channel.send(
                    "Get dunked on!!, if were really friends... **YOU WON'T COME BACK**"
                )
                info["health"] = 24
                info["rest_block"] = time.time()
                await self.bot.players.update_one({"_id": self.author.id}, {"$set": info})
                await self.end()

            func = ["spared", "NotSpared", "spared"]
            sprfunc = random.choice(func)
            embed1 = disnake.Embed(
                title="Mercy", description=f"You tried to spare {monster}"
            )
            embed1.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/793382520665669662/803887253927100436/image0.png"
            )
            msg = await self.channel.send(self.author.mention, embed=embed1)
            await asyncio.sleep(5)
            embed2 = disnake.Embed(
                title="Mercy", description="They didn't accepted your mercy"
            )

            embed2.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/793382520665669662/803889297936613416/image0.png"
            )
            embed3 = disnake.Embed(title="Mercy", description="They accepted your mercy")
            embed3.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/793382520665669662/803887253927100436/image0.png"
            )
            if sprfunc == "spared":
                if self.kind == 1:
                    info["rest_block"] = time.time()

                print(f"{self.author} has ended the fight (sparing)")
                # inter.command.reset_cooldown(inter)
                await msg.edit(embed=embed3)
                info["spares"] = info["spares"] + 1

                await self.bot.players.update_one({"_id": self.author.id}, {"$set": info})
                await self.end()
            elif sprfunc == "NotSpared":
                await msg.edit(embed=embed2)

                await asyncio.sleep(4)
                await self.counter_attack()

        except Exception as e:
            await self.bot.get_channel(827651947678269510).send(e)
            await self.end()


class Fight(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @components.button_listener()
    async def food(self, inter: disnake.MessageInteraction, item: str, uid: int) -> None:
        if inter.author.id != uid:
            await inter.send('This is not yours kiddo!', ephemeral=True)
            return

        try:
            msg_id = inter.bot.fights[str(uid)].menus[0]
            inter.bot.fights[str(uid)].menus.remove(msg_id)
        except:
            pass

        try:
            await inter.response.defer()
        except:
            pass
        if item == "back":
            await inter.edit_original_message(components=[])

            return await inter.bot.fights[str(uid)].menu()

        await inter.edit_original_message(components=[])

        return await getattr(inter.bot.fights[str(uid)], inter.bot.items[item]["func"])(item)

    @components.button_listener()
    async def action(self, inter: disnake.MessageInteraction, action: str, uid: int) -> None:
        if inter.author.id != uid:
            await inter.send('This is not yours kiddo!', ephemeral=True)
            return

        try:
            await inter.response.defer()
        except:
            pass

        await inter.edit_original_message(components=[])
        try:
            msg_id = inter.bot.fights[str(uid)].menus[0]
            inter.bot.fights[str(uid)].menus.remove(msg_id)
        except:
            pass

        return await getattr(inter.bot.fights[str(uid)], action)()

    @commands.command(aliases=["fb"])
    @utils.in_shop()
    @utils.in_battle()
    async def boss(self, inter):

        await utils.create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})

        location = data["location"]

        if data[f"{location}_boss"]:
            embed = disnake.Embed(
                title="BUT NOBODY CAME",
                description="You did it, killed the boss here, whatcha' lookin for now?",
                color=disnake.Color.red()
            )
            return await inter.send(embed=embed)

        curr_time = time.time()
        delta = int(curr_time) - int(data["rest_block"])

        if 1800.0 >= delta > 0:
            seconds = 1800 - delta
            em = disnake.Embed(
                description=(
                    f"**You can't fight a boss yet!**\n\n"
                    f"**You can fight a boss <t:{int(time.time()) + int(seconds)}:R>**"
                ),
                color=disnake.Color.red(),
            )
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/850983850665836544/878024511302271056/image0.png"
            )
            await inter.send(embed=em)
            return

        location = data["location"]
        random_monster = []

        for i in inter.bot.monsters:
            if inter.bot.monsters[i]["location"] == location:
                if inter.bot.monsters[i]["boss"]:
                    random_monster.append(i)
                else:
                    continue

        monster = random.choice(random_monster)

        info = inter.bot.monsters

        enemy_hp = info[monster]["HP"]

        print(f"{inter.author} has entered a boss fight")
        fight = Battle(inter.author, inter.bot, monster, enemy_hp, inter, 1, inter.channel)
        fight.bot.fights[str(inter.author.id)] = fight
        try:
            await fight.menu()
        except Exception as e:
            await inter.bot.get_channel(827651947678269510).send(f"{e}, {str(fight.author)}")
            await inter.send(inter.author.mention + "You have encountered an error, the developers has been notified.")
            await fight.end()

    @commands.command(aliases=["f"])
    @utils.in_shop()
    @utils.in_battle()
    async def fight(self, inter):
        """Fight Monsters and gain EXP and Gold"""
        await utils.create_player_info(inter, inter.author)
        data = await inter.bot.players.find_one({"_id": inter.author.id})

        location = data["location"]

        # if data[f"{location}_kills"] >= self.bot.locations[location]["max_kills"]:
        #    embed = disnake.Embed(
        #         title="BUT NOBODY CAME",
        #         description="You did it, killed everyone here, Now what?",
        #         color=disnake.Color.red()
        #     )
        #     return await inter.send(embed=embed)

        random_monster = []

        for i in inter.bot.monsters:
            if inter.bot.monsters[i]["location"] == location:
                if inter.bot.monsters[i]["boss"]:
                    continue
                else:
                    random_monster.append(i)

        info = inter.bot.monsters

        if len(random_monster) == 0:
            await inter.send(f"There are no monsters here?, You are for sure inside a u?boss area only!")
            return

        monster = random.choice(random_monster)

        enemy_hp = self.bot.monsters[monster]["HP"]

        print(f"{inter.author} has entered a fight")
        fight = Battle(inter.author, inter.bot, monster, enemy_hp, inter, 0, inter.channel)
        fight.bot.fights[str(inter.author.id)] = fight
        try:
            await fight.menu()
        except Exception as e:
            await inter.bot.get_channel(827651947678269510).send(f"{e}, {str(fight.author)}")
            await inter.send(inter.author.mention + "You have encountered an error, the developers has been notified.")
            await fight.end()


def setup(bot):
    bot.add_cog(Fight(bot))

import time
import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from disnake.ui import Button, ActionRow

class ConsoleColors:
    HEADER  = '\033[95m'
    BLUE    = '\033[94m'
    CYAN    = '\033[96m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[1;33m'
    LRED    = '\033[1;31m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'
    BOLD    = '\033[1m'
    UNDER   = '\033[4m'

async def create_player_info(inter, mem):
    dat = await inter.bot.players.find_one({"_id": mem.id})
    if dat is None:
        new_account = {
            # unique idx
            "_id": mem.id,
            "registered_on": int(time.time()),
            "badges": [],
            "character": "",

            # statistics
            "level": 1,
            "resets": 0,
            "health": 20,

            "multi_g": 1,
            "multi_xp": 1,
            "attack": 10,
            "defence": 5,

            "exp": 0,
            "gold": 200,
            "armor": "bandage",
            "inventory": ["monster_candy"],
            "weapon": "stick",
            "location": "ruins",

            # blocks
            "daily_block": 0,
            "supporter_block": 0,
            "booster_block": 0,
            "rest_block": 0,

            # boss booleans
            "ruins_boss": False,
            "snowdin_boss": False,
            "waterfall_boss": False,
            "hotland_boss": False,
            "core_boss": False,
            "the_barrier_boss": False,
            "last_corridor_boss": False,

            # counters
            "ruins_kills": 0,
            "snowdin_kills": 0,
            "waterfall_kills": 0,
            "hotland_kills": 0,
            "core_kills": 0,

            "kills": 0,
            "deaths": 0,
            "spares": 0,

            # crates data
            "standard crate": 1,
            "determination crate": 1,
            "soul crate": 0,
            "void crate": 0,
            "event crate": 0,

            #fight stats
            "in_fight": False,
            "fight_monster": "",
            "fight_hp": 0,
            "fight_def": 0,
            "fight_atk": 0,
        }

        await inter.bot.players.insert_one(new_account)
    else:
        return

class InFight(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="End Fight", style=disnake.ButtonStyle.red)
    async def fight(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()

        data = await inter.bot.players.find_one({"_id": inter.author.id})

        new_deaths = data["deaths"] + 1
        new_health = 20
        new_gold = data["gold"] - 15
        new_in_fight = False
        new_fight_monster = ""
        new_fight_hp = 0
        new_fight_def = 0
        new_fight_atk = 0

        new_data = {"deaths": new_deaths, "health": new_health, "gold": new_gold, "in_fight": new_in_fight, "fight_monster": new_fight_monster, "fight_hp": new_fight_hp, "fight_def": new_fight_def, "fight_atk": new_fight_atk}

        await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": new_data})

        em = disnake.Embed(
            title="The fight has been stopped do /explore to start a new one",
            color=0x0077ff
        )
        await inter.edit_original_message(embed=em, view=None)

def in_battle():
    async def predicate(inter):
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        if data["in_fight"] == True:
            embed = disnake.Embed(
                title="You have a fight dialogue open",
                description=f"Did the fight message get deleted or can you not find it anymore?\nYou can click the button below to end your fight.\n- gold will be removed\n- health will be taken away\n- death count will go up by 1",
                color=0x0077ff
            )

            view = InFight()
            await inter.send(embed=embed, view=view)
            return False
        return True

    return commands.check(predicate)

def occurrence(stored, value):
    try:
        stored[value] = stored[value] + 1
    except KeyError:
        stored[value] = 1
        return
import os
import disnake
from disnake.ext import commands

description = """The undertale RPG Beta bot."""

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

class UndertaleBot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invite_url = "https://discord.gg/FQYVpuNz4Q"
        self.vote_url = "https://top.gg/bot/815153881217892372"
        self.patreon_link = "https://www.patreon.com/undertale_rpg"
        self.currency = ":coin:"
        self.activity = disnake.Game("Undertale | /help ")
        self.help_command = None
        
    #async def on_shard_connect(self, shard):
    #    print(
    #        f"----------Shard {shard} is on.-------------\n"
    #        f"Total Guilds: {len(self.guilds)}\n"
    #        f"Total Shards: {len(self.shards)}\n"
    #        f"-------------------------------------------"
    #    )

    def load_all_cogs(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                self.load_extension(f"cogs.{filename[:-3]}")
                print(f"🔁 cogs.{filename[:-3]} is loaded and ready.")
        return


bot = UndertaleBot(
    command_prefix=commands.when_mentioned_or("?"),
    description=description,
    intents=intents,
    owner_ids=[536538183555481601, 513351917481623572]
)


bot.load_all_cogs()
bot.run("ODcxNzU2NzgyMDEwMjY1NjAw.GpSs42.p4uceF-9m68djR9N1a4HQ7sjh39Ur28AX-EZ1s")
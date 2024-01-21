import datetime
from typing import List

import disnake
from disnake.enums import ButtonStyle
from disnake.ext import commands
from disnake.ui import Button

from main import UndertaleBot
from utility.constants import BLUE


class Menu(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.index = 0

        # Sets the footer of the embeds with their respective page numbers.
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")

        self._update_state()

    def _update_state(self) -> None:
        self.prev_page.disabled = self.index == 0
        self.next_page.disabled = self.index == len(self.embeds) - 1

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.blurple)
    async def prev_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(emoji="🗑️", style=disnake.ButtonStyle.red)
    async def remove(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.blurple)
    async def next_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.index += 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)


class Help(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot

    @commands.slash_command(description="Intro to the undertale universe.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def intro(self, inter: disnake.ApplicationCommandInteraction):
        embeds = [
            disnake.Embed(
                title="Long ago, two races ruled over Earth: HUMANS and MONSTERS.",
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685312292593684/0.png"
            ),
            disnake.Embed(
                title="One day, war broke out between the two races.",
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685312561041469/1.png"
            ),
            disnake.Embed(
                title="After a long battle, the humans were victorious.",
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685312791711744/2.png"
            ),
            disnake.Embed(
                title="They sealed the monsters underground with a magic spell.",
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685310686195762/3.png"
            ),
            disnake.Embed(
                title="Many years later...",
                colour=BLUE,
            ),
            disnake.Embed(
                title="MT. EBOTT 201X",
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685310887505970/4.png"
            ),
            disnake.Embed(
                title="Legends say that those who climb the mountain never return.",
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685311093030982/5.png"
            ),
            disnake.Embed(
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685311311138856/6.png"
            ),
            disnake.Embed(
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685311600554044/7.png"
            ),
            disnake.Embed(
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685311793496064/8.png"
            ),
            disnake.Embed(
                colour=BLUE,
            ).set_image(
                url="https://cdn.discordapp.com/attachments/954829219756666890/955685312007397436/9.png"
            ),
        ]

        # Sends first embed with the buttons, it also passes the embeds list into the View class.
        await inter.send(embed=embeds[0], view=Menu(embeds))

    @commands.slash_command(description="Info on any ongoing events.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def event(self, inter: disnake.ApplicationCommandInteraction):
        events = await self.bot.db["events"].find_one({"_id": 0})
        if events["active"] is False:
            embed = disnake.Embed(
                color=BLUE,
                title="There is currently no event going on",
                description="You can join our [support server](https://discord.gg/FQYVpuNz4Q) to learn about any upcoming events.",
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            return await inter.send(embed=embed)

        name = events["name"]
        location = events["location"]
        duration = events["duration"]
        exp_multi = events["exp_multi"]
        gold_multi = events["gold_multi"]
        loot = events["loot"]
        loot_item = "".join(f" {item}, " for item in loot)

        embed = disnake.Embed(
            color=BLUE,
            title=f"{name}",
            description=f"""
            **Location:** {location}
            **Duration:** {duration}
            **Gold multiplier:** {gold_multi}
            **Exp multiplier:** {exp_multi}
            **Custom loot:** {loot_item}
            """,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await inter.send(embed=embed)

    @commands.slash_command(description="Tutorial on how to use the bot.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def tutorial(self, inter: disnake.ApplicationCommandInteraction):
        start = "**This bot is an Undertale Themed RPG!, You can fight monsters from Undertale on discord!**"
        fight = "Using **/explore** You will find all kind of treasure and monsters in your area!"
        travel = "Speaking of areas?, You can travel to other places using **/travel** command!, You gotta grind well tho!, On **Level 5**, You will unlock snowdin."
        shop = "In the **/shop** you can buy armor, weapons, and food to power up and explore even more of the world!"
        help_ = "You can use the command **/help** to see other commands!"
        daily = "There are rewards commands such as **/daily** & **/supporter** with which you can earn based on your level."
        reset = "There is a command called **/reset**, reach level **70**, and you can get multiplier for EXP and GOLD!!"
        crates = "You can vote to get crates!, run the command **/vote**, then vote for us, then run the command **/crates** to open your crates."

        embed = disnake.Embed(
            title="Welcome to Undertale RPG!",
            color=BLUE,
            description=f"{start}\n\n{fight}\n\n{travel}\n\n{shop}\n\n{daily}\n\n{crates}\n\n{reset}\n\n{help_}",
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await inter.send(embed=embed)

    @commands.slash_command(
        description="A complete view of the bot's features and commands with useful links."
    )
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        """Info on how to use the bot and it's commands."""

        em = disnake.Embed(
            title="📜 | Help Menu!", color=BLUE, timestamp=datetime.datetime.now()
        )
        em.set_thumbnail(url=self.bot.user.avatar.url)
        forbid = ["Event", "TopGG", "Errors", "Test"]

        for cog in self.bot.cogs:
            cog = self.bot.get_cog(cog)
            if cog.qualified_name in forbid:
                continue

            cmds = cog.get_slash_commands()
            commands_per = "".join(f" `{command.name}` • " for command in cmds)
            em.add_field(
                name=cog.qualified_name, value=f"• {commands_per} \n\n", inline=False
            )

        em.add_field(
            name="> Useful links",
            value="[Support](https://discord.gg/FQYVpuNz4Q) • [Vote](https://top.gg/bot/815153881217892372)",
            inline=False,
        )

        buttons = [
            Button(
                style=ButtonStyle.link,
                label="FAQ",
                url="https://discord.com/channels/817437132397871135/1198314647879692308",
            ),
            Button(
                style=ButtonStyle.link,
                label="Support",
                url="https://discord.gg/FQYVpuNz4Q",
            ),
        ]

        await inter.send(inter.author.mention, embed=em, components=buttons)


def setup(bot: UndertaleBot):
    bot.add_cog(Help(bot))

import disnake
from disnake import Interaction
from disnake.enums import ButtonStyle
from disnake.ext import commands
from disnake.ui import Button, ActionRow
import datetime
import os

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Info on any ongoing events")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def event(self, inter):
        events = await self.bot.db["events"].find_one({"_id": 0})
        if events["active"] == False:
            em = disnake.Embed(
                color=0x0077ff,
                title="There is currently no event going on",
                description="You can join our [support server](https://discord.gg/FQYVpuNz4Q) to learn about any upcoming events." 
            )
            em.set_thumbnail(url=self.bot.user.avatar.url)
            return await inter.send(embed=em)

        name = events["name"]
        location = events["location"]
        duration = events["duration"]
        exp_multi = events["exp_multi"]
        gold_multi = events["gold_multi"]
        loot = events["loot"]
        loot_item = "".join(f" {item}, " for item in loot)

        em = disnake.Embed(
            color=0x0077ff,
            title=f"{name}",
            description=f"""
            **Location:** {location}
            **Duration:** {duration}
            **Gold multiplier:** {gold_multi}
            **Exp multiplier:** {exp_multi}
            **Custom loot:** {loot_item}
            """
        )
        em.set_thumbnail(url=self.bot.user.avatar.url)
        await inter.send(embed=em)
    
    @commands.slash_command(description="Tutorial on how to use the bot")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def tutorial(self, inter):
        start = "**This bot is an Undertale Themed RPG!, You can fight monsters from Undertale on discord!**"
        fight = "Using **/explore** You will find all kind of treasure and monsters in your area!"
        travel = "Speaking of areas?, You can travel to other places using **/travel** command!, You gotta grind well tho!, On **Level 5**, You will unlock snowdin."
        shop = "In the **/shop** you can buy armor, weapons, and food to power up and explore even more of the world!"
        help_ = "You can use the command **/help** to see other commands!"
        daily = "There are rewards commands, **/daily** & **/supporter**, You can earn based on your level"
        reset = "There is a command called **/reset**, reach level **70**, and you can get multiplier for EXP and GOLD!!"
        crates = "You can vote to get crates!, run the command **/vote**, then vote for us, then run the command **/crates** to open your crates"

        em = disnake.Embed(
            title="Welcome to Undertale RPG!",
            color=0x0077ff,
            description=f"{start}\n\n{fight}\n\n{travel}\n\n{shop}\n\n{daily}\n\n{crates}\n\n{reset}\n\n{help_}"
        )
        em.set_thumbnail(url=self.bot.user.avatar.url)
        await inter.send(embed=em)

    @commands.slash_command(description="a complete view of the bot's features and commands with useful links.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def help(self, inter):
        """Info on how to use the bot and it's commands."""

        em = disnake.Embed(
            title = "📜 | Help Menu!",
            color = 0x0077ff,
            timestamp = datetime.datetime.now()
        )
        em.set_thumbnail(url=self.bot.user.avatar.url)
        forbid = ["Event", "TopGG", "Errors", "Test"]

        for cog in self.bot.cogs:
            cog = self.bot.get_cog(cog)
            if cog.qualified_name in forbid:
                continue

            cmds = cog.get_slash_commands()
            commands_per = "".join(f" `{command.name}` • " for command in cmds)
            em.add_field(name=cog.qualified_name, value=f"• {commands_per} \n\n", inline=False)

        em.add_field(
            name="> Useful links", 
            value="[Website](https://undertalerpg.monster/) • [Support](https://discord.gg/FQYVpuNz4Q) • [Patreon](https://www.patreon.com/UndertaleRPG) • [Vote](https://top.gg/bot/815153881217892372)", inline=False
            )

        buttons = [
            Button(
                style = ButtonStyle.link,
                label = "FAQ",
                url = "https://undertalerpg.monster/faq"
            ),
            Button(
                style = ButtonStyle.link,
                label = "Support",
                url = "https://www.patreon.com/UndertaleRPG"
            )
        ]

        await inter.send(inter.author.mention, embed=em, components=buttons)


def setup(bot):
    bot.add_cog(Help(bot))
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
    
    @commands.slash_command(description="Tutorial on how to use the bot")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def tutorial(self, inter):
        """A tutorial for the undertale rpg bot."""

        await inter.send(content="There is currently no tutorial avaliable", ephemeral=True)

    @commands.slash_command(description="Help command")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def help(self, inter):
        """Info on how to use the bot and it's commands."""

        em = disnake.Embed(
            title = "📜 | Help Menu!",
            color = 0x0077ff,
            timestamp = datetime.datetime.now()
        )

        forbid = ["Event"]

        for cog in self.bot.cogs:
            cog = self.bot.get_cog(cog)
            if cog.qualified_name in forbid:
                continue

            cmds = cog.get_slash_commands()
            commands_per = "".join(f" `{command.name}` • " for command in cmds)
            em.add_field(name=cog.qualified_name, value=f"• {commands_per} \n\n", inline=False)

        em.add_field(name="> Useful links", value="[Website](https://undertalerpg.monster/) • [Support](https://discord.gg/FQYVpuNz4Q) • [Patreon](https://www.patreon.com/UndertaleRPG) • [Vote](https://top.gg/bot/815153881217892372)", inline=False)

        buttons = [
            Button(
                style = ButtonStyle.link,
                label = "Website",
                url = "https://undertalerpg.monster/"
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
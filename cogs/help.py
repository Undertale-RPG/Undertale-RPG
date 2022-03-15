import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        """custom help command for the bot"""
        self.bot = bot

    @commands.command()
    async def tutorial(self, ctx):
        prefix = ctx.prefix
        embed = discord.Embed(title="Welcome to Undertale RPG!")

        text1 = "**This bot is an Undertale Themed RPG!, You can fight monsters from Undertale on discord!**"

        text2 = f"You can run the command **{prefix}fight** To fight any monster in your area"

        text3 = f"Speaking of areas?, You can travel to other places using **{prefix}travel** command!, You gotta " \
                f"grind well tho!, On **'Level' 3**, You will unlock snowdin "

        text4 = f"You can run the command **{prefix}shop** To buy armor, weapons, and food with **gold**"

        text5 = f"You can use the command **{prefix}help** to see other commands!"

        text6 = f"There are rewards commands, **{prefix}daily & {prefix}supporter**, You can earn based on your level"
        text7 = f"There is a command called **{prefix}reset**, reach level 70, and you can get multiplier for EXP " \
                f"and GOLD!! "
        text8 = f"You can vote to get crates!, run the command **{prefix}vote**, then vote for us, then run the " \
                f"command **{prefix}crate** to open your crates "

        embed.description = f"{text1}\n\n{text2}\n\n{text3}\n\n{text4}\n\n{text5}\n\n{text6}\n\n{text7}\n\n{text8}"

        embed.set_image(
            url="https://cdn.discordapp.com/attachments/827651835372240986/906433674558455818/IMG_0173.jpg"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, command: str = None):
        if command is not None:
            command = self.bot.get_command(command)
        if command is not None:
            embed = discord.Embed(
                title=f"{command.name} Command",
                description=f"**Usage:**\n `{ctx.prefix}{command.name} {command.signature}`\n\n**Description:**\n{command.help}",
                color=discord.Colour.random(),
            )
            await ctx.send(embed=embed)
            return
        emb = discord.Embed(
            title="📜┃list of commands and modules of the bot",
            color=discord.Colour.random(),
        )
        forbid = [
            "TopGG",
            "Event",
            "Developer_Tools",
            "Jishaku",
            "Loops",
            "DiscordListsPost",
        ]
        for cog in self.bot.cogs:
            cog = self.bot.get_cog(cog)
            if cog.qualified_name in forbid:
                continue

            commands = cog.get_commands()
            commands_per = "".join(f" `{command}` • " for command in commands)
            emb.add_field(
                name=cog.qualified_name, value=f"• {commands_per} \n\n", inline=False
            )
        emb.set_footer(
            text=f"{ctx.prefix}help <category> or <command>",
            icon_url=ctx.author.avatar_url,
        )

        emb.set_image(
            url="https://cdn.discordapp.com/attachments/850983850665836544/874667836985966682/image0.png"
        )
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))

import disnake
from disnake.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        """custom help command for the bot"""
        self.bot = bot

    @commands.command()
    async def tutorial(self, inter):
        embed = disnake.Embed(title="Welcome to Undertale RPG!")

        text1 = "**This bot is an Undertale Themed RPG!, You can fight monsters from Undertale on discord!**"

        text2 = f"You can run the command **{inter.prefix}fight** To fight any monster in your area"

        text3 = f"Speaking of areas?, You can travel to other places using **{inter.prefix}travel** command!, You gotta " \
                f"grind well tho!, On **'Level' 3**, You will unlock snowdin "

        text4 = f"You can run the command **{inter.prefix}shop** To buy armor, weapons, and food with **gold**"

        text5 = f"You can use the command **{inter.prefix}help** to see other commands!"

        text6 = f"There are rewards commands, **{inter.prefix}daily & {inter.prefix}supporter**, You can earn based on your level"
        text7 = f"There is a command called **{inter.prefix}reset**, reach level 70, and you can get multiplier for EXP " \
                f"and GOLD!! "
        text8 = f"You can vote to get crates!, run the command **{inter.prefix}vote**, then vote for us, then run the " \
                f"command **{inter.prefix}crate** to open your crates "

        embed.description = f"{text1}\n\n{text2}\n\n{text3}\n\n{text4}\n\n{text5}\n\n{text6}\n\n{text7}\n\n{text8}"

        embed.set_image(
            url="https://cdn.discordapp.com/attachments/827651835372240986/906433674558455818/IMG_0173.jpg"
        )
        await inter.send(embed=embed)

    @commands.command()
    async def help(self, ctx, command: str = None):
        if command is not None:
            command = self.bot.get_command(command)
        if command is not None:
            embed = disnake.Embed(
                title=f"{command.name} Command",
                description=f"**Usage:**\n `{ctx.prefix}{command.name} {command.signature}`\n\n**Description:**\n{command.help}",
                color=disnake.Colour.random(),
            )
            await ctx.send(embed=embed)
            return
        emb = disnake.Embed(
            title="📜┃list of commands and modules of the bot",
            color=disnake.Colour.random(),
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

            cmds = cog.get_commands()
            commands_per = "".join(f" `{command}` • " for command in cmds)
            emb.add_field(
                name=cog.qualified_name, value=f"• {commands_per} \n\n", inline=False
            )
        emb.set_footer(
            text=f"{ctx.prefix}help <category> or <command>",
            icon_url=ctx.author.display_avatar,
        )

        emb.set_image(
            url="https://cdn.discordapp.com/attachments/850983850665836544/874667836985966682/image0.png"
        )
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(HelpCommand(bot))

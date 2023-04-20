import disnake
from disnake.enums import ButtonStyle
from disnake.ext import commands
from disnake.ui import Button

from main import UndertaleBot
from utility.constants import BLUE


class Bot(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot

    @commands.slash_command(description="link to the bot invite and support server.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def invite(self, inter: disnake.ApplicationCommandInteraction):
        """Invite the bot to your server and join our support server!"""
        embed = disnake.Embed(
            color=BLUE,
            title="Wanna add me to your server huh?, click the link below!",
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(
            name="Bot invite",
            value="[Click here](https://discord.com/api/oauth2/authorize?client_id=748868577150369852&permissions=415001603136&scope=bot%20applications.commands)",
        )
        embed.add_field(
            name="Support server", value="[Click here](https://discord.gg/FQYVpuNz4Q)"
        )

        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(description="View the bots ping.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        """Latency check for stability"""
        await inter.send(
            f"pong! **{round(self.bot.latency * 1000)}ms**", ephemeral=True
        )

    @commands.slash_command(description="Info on the bot.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def botinfo(self, inter: disnake.ApplicationCommandInteraction):
        """Info on the bot"""
        embed = disnake.Embed(
            title="Undertale RPG",
            description="An undertale rpg themed discord bot.",
            color=BLUE,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Guild count", value=f"`{len(self.bot.guilds)}` Guilds")
        embed.add_field(name="Latency", value=f"`{round(self.bot.latency * 1000)}`ms")
        embed.add_field(name="Shard count", value=f"`{len(self.bot.shards)}` shards")
        embed.add_field(
            name="Creators",
            value="`yaki#8693` (bot dev)\n`Commander R#9371` (website dev)\n`СᏓᎾυdy#4204` (artist)",
        )
        embed.add_field(
            name="Disclaimer",
            value="All the designs/names of the pictures, locations, monsters and bosses belong to the official undertale creator: **Toby Fox**",
        )
        embed.set_footer(text="you can find more info on our website.")

        buttons = [
            Button(style=ButtonStyle.link, label="Website", url=self.bot.website)
        ]

        await inter.send(embed=embed, components=buttons, ephemeral=True)

    @commands.slash_command(description="Vote for our bots and receive rewards.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def vote(self, inter: disnake.ApplicationCommandInteraction):
        """Vote for the bot for special reward"""
        embed = disnake.Embed(title="<:DT:1010165881516609596> Voting", color=BLUE)
        embed.add_field(
            name="Voting on Top.gg",
            value="Vote rewards are coming soon. Any votes are still very much appreciated!",
        )
        embed.add_field(
            name="Claim and support our server",
            value="You can claim an exclusive reward by joining our server and running /supporter",
        )

        buttons = [
            Button(style=ButtonStyle.link, label="Top.gg", url=self.bot.vote_url),
            Button(
                style=ButtonStyle.link,
                label="Support server",
                url="https://discord.gg/FQYVpuNz4Q",
            ),
        ]
        await inter.send(inter.author.mention, embed=embed, components=buttons)

    @commands.slash_command(description="A list of all badges you can earn.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def badges(self, inter: disnake.ApplicationCommandInteraction):
        """A list of all badges you can earn."""
        embed = disnake.Embed(
            title="Here is a showcase of all the badges you can earn",
            color=BLUE,
            description="""
            <:developer:1051266723208241253> -> creator of the bot
            <:staff:1051266679356792923> -> staff of the bot
            <:beta:1051275494601011291> -> public beta tester
            <:bughunter:1051275974702006352> -> find and report a valid bug
            <:resets:1051277356813262858> -> reach max resets
            <:trophy:1051281684894580736> -> get all achievements
            <:booster:1051256363516436571> -> boosting our support server
            <:blacklist:1051266962321317908> -> blacklisted user
            """,
        )
        embed.set_footer(
            "This feature is a work in progress you are not able to earn all these badges at this moment."
        )
        await inter.send(embed=embed)


def setup(bot: commands.AutoShardedInteractionBot):
    bot.add_cog(Bot(bot))

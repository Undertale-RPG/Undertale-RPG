import disnake
from disnake.enums import ButtonStyle
from disnake.ext import commands
from disnake.ui import Button

from utility.constants import BLUE
from main import UndertaleBot

class Bot(commands.Cog):
    def __init__(self, bot: UndertaleBot):
        self.bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def invite(self, inter: disnake.ApplicationCommandInteraction):
        """Invite the bot to your server and join our support server!"""
        embed = disnake.Embed(
            color=BLUE,
            title="Wanna add me to your server?, click the link below!",
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

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        """Latency check for stability"""
        await inter.send(
            f"pong! **{round(self.bot.latency * 1000)}ms**", ephemeral=True
        )

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def botinfo(self, inter: disnake.ApplicationCommandInteraction):
        """Info on the bot"""
        embed = disnake.Embed(
            title="Undertale RPG",
            description="An undertale rpg themed discord bot.",
            color=BLUE,
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Guild count", value=f"`{len(self.bot.guilds)}` Guilds")
        embed.add_field(name="Latency", value=f"`{round(self.bot.latency * 1000)}`ms")
        embed.add_field(name="Shard count", value=f"`{len(self.bot.shards)}` shards")
        embed.add_field(
            name="Creators",
            value="`yakirarage` (developer)\n`СᏓᎾυdy#4204` (artist)",
        )
        embed.add_field(
            name="Disclaimer",
            value="All the designs/names of any original undertale content belong to the official undertale creator: **Toby Fox**",
        )
        embed.set_footer(text="you can find more info on our website.")

        await inter.send(embed=embed)

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def vote(self, inter: disnake.ApplicationCommandInteraction):
        """Vote for the bot for special rewards"""
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

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def badges(self, inter: disnake.ApplicationCommandInteraction):
        """A list of all badges you can earn."""
        embed = disnake.Embed(
            title="Here is a showcase of all the badges you can earn",
            color=BLUE,
            description="""
            <:developer:1051266723208241253> → creator of the bot
            <:bughunter:1051275974702006352> → find and report a valid bug
            ⬅️ → reach max resets
            <:trophy:1051281684894580736> → get all achievements
            <:booster:1051256363516436571> → boosting our support server
            <:blacklist:1051266962321317908> → blacklisted user
            """
        )
        await inter.send(embed=embed)


def setup(bot: commands.AutoShardedInteractionBot):
    bot.add_cog(Bot(bot))

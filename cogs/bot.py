from cProfile import label
from os import link
from tkinter.ttk import Style
import disnake 
from disnake.ext import commands
from disnake.enums import ButtonStyle

from disnake.ui import Button, ActionRow
class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="link to the bot invite and support server")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def invite(self, inter):
        em = disnake.Embed(
            color=0x0077ff,
            title="Wanna add me to your server huh?, click the link below!"
        )
        em.set_thumbnail(url=self.bot.user.avatar.url)
        em.add_field(name="Bot invite", value="[Click here](https://discord.com/api/oauth2/authorize?client_id=815153881217892372&permissions=412421053760&scope=bot%20applications.commands)")
        em.add_field(name="Support server", value="[Click here](https://discord.gg/FQYVpuNz4Q)")

        await inter.send(embed=em)

    @commands.slash_command(description="ping, pong")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def ping(self, inter):
        """Latency check for stability"""
        await inter.send(f"pong! **{round(self.bot.latency * 1000)}ms**")

    @commands.slash_command(description="Info on the bot")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def botinfo(self, inter):
        """Info on the bot"""
        em = disnake.Embed(
            title = "Undertale RPG",
            description = "An undertale rpg themed discord bot.",
            color = 0x0077ff
        )
        em.set_thumbnail(url=self.bot.user.avatar.url)
        em.add_field(name="Guild count", value=f"`{len(self.bot.guilds)}` Guilds")
        em.add_field(name="Latency", value=f"`{round(self.bot.latency * 1000)}`ms")
        em.add_field(name="Shard count", value=f"`{len(self.bot.shards)}` shards")
        em.add_field(name="Creators", value="`LetsChill#2911` (founder)\n`yaki#8693` (bot dev)\n`Commander R#9371` (website dev)\n`СᏓᎾυdy#4204` (artist)")
        em.add_field(name="Disclaimer", value="All the designs/names of the pictures, locations, monsters and bosses belong to the official undertale creator: **Toby Fox**")

        await inter.send(inter.author.mention, embed=em)

    @commands.slash_command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def vote(self, inter):
        """Vote for the bot for special reward"""
        em = disnake.Embed(
            title="<:DT:1010165881516609596> Voting",
            color=0x0077ff
            )
        em.add_field(name="Voting on Top.gg", value="You will earn 500G and a standard crate.", inline=True)
        em.add_field( name="Claim and support our server", value="You can claim an exclusive reward by joining our server and running u?supporter", inline=True)

        buttons = [
            Button(
                style=ButtonStyle.link,
                label="Click to vote!",
                url=self.bot.vote_url
            ),
            Button(
                style=ButtonStyle.link,
                label="Support server",
                url="https://discord.gg/FQYVpuNz4Q"
            )
        ]
        await inter.send(inter.author.mention, embed=em, components=buttons)

def setup(bot):
    bot.add_cog(Bot(bot))
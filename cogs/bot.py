import disnake 
from disnake.ext import commands
from disnake.enums import ButtonStyle

from disnake.ui import Button, ActionRow
class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="link to the bot invite and support server.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def invite(self, inter):
        em = disnake.Embed(
            color=0x0077ff,
            title="Wanna add me to your server huh? Click the link below!"
        )
        em.set_thumbnail(url=self.bot.user.avatar.url)
        em.add_field(name="Bot invite", value="[Click here](https://discord.com/api/oauth2/authorize?client_id=748868577150369852&permissions=415001603136&scope=bot%20applications.commands)")
        em.add_field(name="Support server", value="[Click here](https://discord.gg/FQYVpuNz4Q)")

        await inter.send(embed=em)

    @commands.slash_command(description="Ping the bot.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def ping(self, inter):
        """Latency check for stability"""
        await inter.send(f"pong! **{round(self.bot.latency * 1000)}ms**")

    @commands.slash_command(description="Info on the bot.")
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
        em.add_field(name="Creators", value="`LetsChill#0001` (founder)\n`yaki#8693` (bot dev)\n`Commander R#9371` (website dev)\n`СᏓᎾυdy#4204` (artist)")
        em.add_field(name="Disclaimer", value="All the designs/names of the pictures, locations, monsters, and bosses belong to the official undertale creator: **Toby Fox**")
        em.set_footer(text="You can find more info on our website")

        buttons = [
            Button(
                style=ButtonStyle.link,
                label="Website",
                url=self.bot.website
            )]

        await inter.send(embed=em, components=buttons)

    @commands.slash_command(description="Vote for our bots and recieve rewards.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def vote(self, inter):
        """Vote for the bot for special reward"""
        em = disnake.Embed(
            title="<:DT:1010165881516609596> Voting",
            color=0x0077ff
            )
        em.add_field(name="Voting on Top.gg", value="You will earn 500G and a standard crate.", inline=True)
        em.add_field( name="Claim and support our server", value="You can claim an exclusive reward by joining our server and running /supporter", inline=True)

        buttons = [
            Button(
                style=ButtonStyle.link,
                label="Top.gg",
                url=self.bot.vote_url
        	),
            Button(
                style=ButtonStyle.link,
                label="Univers-list",
                url="https://universe-list.xyz/bots/815153881217892372"
            ),
            Button(
                style=ButtonStyle.link,
                label="Support server",
                url="https://discord.gg/FQYVpuNz4Q"
            ),
        ]
        await inter.send(inter.author.mention, embed=em, components=buttons)

    @commands.slash_command(description="A list of all badges you can earn.")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def badges(self, inter):
        em = disnake.Embed(
            title="Here is a showcase of all the badges you can earn",
            color=0x0077ff,
            description="""
            **__Disclaimer:__ This feature is a work in progress. You are not able to earn all these badges at this moment.**
            
            <:developer:1051266723208241253> -> creator of the bot
            <:staff:1051266679356792923> -> staff of the bot
            <:beta:1051275494601011291> -> public beta tester
            <:bughunter:1051275974702006352> -> find and report a valid bug
            <:resets:1051277356813262858> -> reach max resets
            <:trophy:1051281684894580736> -> get all achievements
            <:booster:1051256363516436571> -> boosting our support server
            <:blacklist:1051266962321317908> -> blacklisted user
            """
        )
        await inter.send(embed=em)

def setup(bot):
    bot.add_cog(Bot(bot))

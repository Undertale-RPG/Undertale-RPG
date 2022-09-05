from turtle import title
import disnake 
from disnake.ext import commands

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = disnake.Embed(
                title="This command is on cooldown!",
                description=f"Try again in **{error.retry_after:.2f}** seconds",
                color=0x0077ff
            )
            return await inter.send(embed=em, ephemeral=True)
        

        em = disnake.Embed(
            title=f"An error has occured",
            description=error,
            color=0x0077ff
        )
        em.set_footer(text=f"{inter.author.id} • {inter.author}")

        #channel = self.bot.get_channel(1015768862450536519)
        #await channel.send(embed=em)


def setup(bot):
    bot.add_cog(Errors(bot))
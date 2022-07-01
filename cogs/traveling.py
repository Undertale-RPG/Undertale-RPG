from disnake.ext import commands, components
import disnake
from disnake.ui import Button, ActionRow
from disnake import ButtonStyle

from utility.dataIO import fileIO
from utility.utils import in_shop, in_battle, create_player_info


class Traveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    @in_shop()
    @in_battle()
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def travel(self, inter):
        """Travel to other spots of the world"""

        await create_player_info(inter, inter.author)
        info = await self.bot.players.find_one({"_id": inter.author.id})
        data = self.bot.locations
        lista = []

        for key in data:
            if data[key]["RQ_LV"] > info["level"]:
                level = data[key]["RQ_LV"]
                lista.append(
                    Button(label=f"{key.title()} (LV {level})",
                           style=ButtonStyle.grey,
                           disabled=True
                           )
                )
                continue
            lista.append(
                Button(
                    label=key.title(),
                    custom_id=self.t_selected.build_custom_id(
                        place=key.lower(),
                        uid=inter.author.id
                    ),
                    style=ButtonStyle.blurple, disabled=False
                )
            )

        lista.append(
            Button(
                label="Close Interaction",
                custom_id=self.t_selected.build_custom_id(
                    place="end",
                    uid=inter.author.id
                ),
                style=ButtonStyle.red, disabled=False
            )
        )

        rows = []
        for i in range(0, len(lista), 5):
            rows.append(ActionRow(*lista[i: i + 5]))

        em = disnake.Embed(
            title="Where would you like to go?", color=disnake.Color.blue()
        )
        lvl = info["level"]
        loc = info["location"]
        em.description = f"Your Level is **{lvl}**"
        em.description += f"\nYour current location is **{loc.title()}**"
        await inter.send(embed=em, components=rows)

    @components.button_listener()
    async def t_selected(self, inter: disnake.MessageInteraction, place: str, uid: str) -> None:
        if inter.author.id != int(uid):
            await inter.send('This is not your kiddo!', ephemeral=True)
            return

        info = await self.bot.players.find_one({"_id": inter.author.id})
        data = inter.bot.locations
        answer = place
        await inter.response.defer()

        if answer == "end":
            await inter.edit_original_message(components=[])
            return await inter.send("closed", ephemeral=True)

        if answer == info["location"]:
            return await inter.send(f"You are Already At {answer}.", ephemeral=True)

        if answer in data:
            location = info["location"]

            if info[f"{location}_boss"] is not True:
                if info[f"{answer}_boss"]:
                    pass
                else:
                    return await inter.send("You have to kill this boss's area before going on!", ephemeral=True)

            info["location"] = answer
            out = {
                "location": answer
            }
            await self.bot.players.update_one(
                {"_id": inter.author.id}, {"$set": out}
            )
            em = disnake.Embed(
                description=f"**{inter.author.name}\n\nYou have arrived {answer}**",
                color=disnake.Color.red(),
            )
            await inter.edit_original_message(components=[])

            return await inter.send(embed=em)


def setup(bot):
    bot.add_cog(Traveling(bot))

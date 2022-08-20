import disnake
from disnake.ext import commands, components
from disnake.ui import Button, ActionRow
from disnake.enums import ButtonStyle
import asyncio

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Open your crates!")
    async def crates(self, inter):
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        standard = data["standard crate"]
        determin = data["determination crate"]
        soul = data["soul crate"]
        void = data["void crate"]
        embed = disnake.Embed(
            title="Your crates",
            description="You can earn crates by exploring, voting or defeating specific bosses",
            color=0x0077ff,
        )
        embed.add_field(
            name="Your boxes",
            value=f"""
Standard crates: {standard}
Determination crates: {determin}
soul crates: {soul}
void crates: {void}
event crates: 0
                              """,
        )
        row = ActionRow(
            Button(
                style=ButtonStyle.grey,
                label="Standard Crate",
                custom_id=self.c_selected.build_custom_id(
                    item="standard crate",
                    uid=inter.author.id
                ),
            ),
            Button(
                style=ButtonStyle.grey,
                label="Determination Crate",
                custom_id=self.c_selected.build_custom_id(
                    item="determination crate",
                    uid=inter.author.id
                ),
            ),
            Button(
                style=ButtonStyle.grey,
                label="Soul Crate",
                custom_id=self.c_selected.build_custom_id(
                    item="soul crate",
                    uid=inter.author.id
                ),
            ),
            Button(
                style=ButtonStyle.grey,
                label="Void Crate",
                custom_id=self.c_selected.build_custom_id(
                    item="void crate",
                    uid=inter.author.id
                ),
            ),
        )
        await inter.send(embed=embed, components=[row])
    
    @components.button_listener()
    async def c_selected(self, inter: disnake.MessageInteraction, item: str, uid: str) -> None:
        if inter.author.id != int(uid):
            await inter.send('This is not your kiddo!', ephemeral=True)
            return

        data = await inter.bot.players.find_one({"_id": inter.author.id})
        await inter.response.defer()

        if data[item] == 0:
            return await inter.edit_original_message(
                content=f"You don't have any {item.title()}",
                embed=None,
                components=[],
            )

        await inter.edit_original_message(
            content=f"{inter.author.mention} opened a {item.title()}...",
            embed=None,
            components=[],
        )
        data[item] -= 1
        earned_gold = inter.bot.crates[item]["gold"] + data["level"]
        gold = data["gold"] + earned_gold
        await asyncio.sleep(3)
        await inter.edit_original_message(
            content=f"{inter.author.mention} earned {earned_gold}G from a {item.title()}"
        )
        info = {
            "gold": gold,
            item: data[item]
        }
        return await inter.bot.players.update_one(
            {"_id": inter.author.id}, {"$set": info}
        )


def setup(bot):
    bot.add_cog(Shop(bot))
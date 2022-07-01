import disnake
from disnake.ext import commands, components

intro = [
    [
        'Long ago, two races ruled over Earth: HUMANS and MONSTERS.',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685312292593684/0.png'
    ],
    [
        'One day, war broke out between the two races.',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685312561041469/1.png'
    ],
    [
        'After a long battle, the humans were victorious.',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685312791711744/2.png'
    ],
    [
        'They sealed the monsters underground with a magic spell.',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685310686195762/3.png'
    ],
    [
        'Many years later...',
        ''
    ],
    [
        'MT. EBOTT 201X',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685310887505970/4.png'
    ],
    [
        'Legends say that those who climb the mountain never return.',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685311093030982/5.png'
    ],
    [
        '',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685311311138856/6.png'
    ],
    [
        '',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685311600554044/7.png',
    ],
    [
        '',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685311793496064/8.png',
    ],
    [
        '',
        'https://cdn.discordapp.com/attachments/954829219756666890/955685312007397436/9.png'
    ]
]

intro_embs = []
for n, i in enumerate(intro):
    if len(i[0]) != 0:
        desc = f"`{i[0]}`"
    else:
        desc = ''
    emb = disnake.Embed.from_dict(
        {
            "description": desc,
            "color": 0xbe8226,
            "image": {"url": i[1]},
            "footer": {"text": f"{str(n + 1)} / {len(intro)}"}
        }
    )
    if len(i[1]) != 0:
        emb.set_image(url=i[1])
    intro_embs.append(emb)


def intro_build_comps(author_id: str, index: int) -> list:
    disable_l, disable_r = [False] * 2
    if index == 0:
        disable_l = True
    elif index == len(intro_embs) - 1:
        disable_r = True
    return [
        disnake.ui.Button(
            style=disnake.ButtonStyle.gray,
            label='<',
            custom_id=Intro.intro_controller.build_custom_id(act="intro_left", uid=author_id),
            disabled=disable_l
        ),
        disnake.ui.Button(
            style=disnake.ButtonStyle.gray,
            label='>',
            custom_id=Intro.intro_controller.build_custom_id(act="intro_right", uid=author_id),
            disabled=disable_r
        ),
        disnake.ui.Button(
            style=disnake.ButtonStyle.danger,
            label='x',
            custom_id=Intro.intro_controller.build_custom_id(act="intro_exit", uid=author_id),
        ),
    ]


async def intro_proc_nav(inter: disnake.MessageCommandInteraction, val: int, uid: str) -> None:
    if inter.author.id != int(uid):
        await inter.send('not allowed!', ephemeral=True)
        return
    await inter.response.defer()
    index = int(inter.message.embeds[0].footer.text.split(' / ')[0]) - (val * 2)
    await inter.message.edit(
        embed=intro_embs[index],
        components=intro_build_comps(
            author_id=str(inter.author.id),
            index=index
        )
    )


class Intro(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        

    @commands.command()
    async def intro(self, inter) -> None:
        await inter.send(
            embed=intro_embs[0],
            components=intro_build_comps(
                author_id=str(inter.author.id),
                index=0
            )
        )

    @components.button_listener()
    async def intro_controller(self, inter: disnake.MessageInteraction, act: str, uid: str) -> None:
        if act == "intro_exit":
            if inter.author.id != int(uid):
                await inter.send('not allowed!', ephemeral=True)
                return
            await inter.response.defer()
            return await inter.message.delete()

        if act == "intro_right":
            return await intro_proc_nav(inter=inter, val=0, uid=uid)

        if act == "intro_left":
            await intro_proc_nav(inter=inter, val=1, uid=uid)


def setup(bot: commands.Bot):
    bot.add_cog(Intro(bot))

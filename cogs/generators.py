#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord import Embed
from discord.ext import commands
from random import choice, randint
from pengaelicutils import list2str, syllables, abilities, quirks


class Generators(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yellow = 0xFFFF00

    name = "generators"
    description = "Make stuff at random."

    description_long = description

    @commands.command(
        name="name",
        help="Generate a random name! They tend to be mystic-sounding :eyes:",
        aliases=["namegen"],
        usage="[names to generate (1)] [max syllables (3)] [min syllables (2)]",
    )
    async def name_generator(
        self, ctx, amount: int = 1, upper_limit: int = 3, lower_limit: int = 2
    ):
        if amount > 0 and upper_limit > 0 and lower_limit > 0:
            if not lower_limit > upper_limit:
                await ctx.send(
                    list2str(
                        [
                            "".join(
                                [
                                    choice(syllables)
                                    for _ in range(randint(lower_limit, upper_limit))
                                ]
                            ).capitalize()
                            for _ in range(amount)
                        ],
                        3,
                    )
                )
            else:
                await ctx.send("The lower limit cannot be higher than the upper limit.")
        else:
            await ctx.send("Values can't be zero.")

    @commands.command(name="ability", help="Generate a random ability.")
    async def gena(self, ctx):
        await ctx.send(
            (choice((abilities["part1"])) + choice(abilities["part2"])).capitalize()
        )

    @commands.command(name="quirk", help="Generate a random quirk.")
    async def genq(self, ctx):
        middle = choice([" of the ", "'s "])
        if middle == "'s ":
            await ctx.send(
                choice((quirks["part1"])).capitalize()
                + middle
                + choice(quirks["part2"]).capitalize()
            )
        else:
            await ctx.send(
                choice((quirks["part2"])).capitalize()
                + middle
                + choice(quirks["part1"]).capitalize()
            )


def setup(client):
    client.add_cog(Generators(client))

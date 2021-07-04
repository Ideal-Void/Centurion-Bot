#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord import Embed
from discord.ext import commands
from subprocess import check_output as shell
from random import choice, randint
from pengaelicutils import list2str, Stopwatch, syllables


class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yellow = 0xFFFF00

    name = "other"
    description = "Various other things."
    description_long = description + " All commands taken from Pengaelic Bot!"

    @commands.command(name="os", help="Read what OS I'm running on!", aliases=["getos"])
    async def showOS(self, ctx):
        async with ctx.typing():
            system = (
                shell(
                    'neofetch | grep OS | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g"',
                    shell=True,
                )
                .decode()
                .split(":")[1][1:-2]
                .split("x86")[0][:-1]
            )
            kernel = (
                shell(
                    'neofetch | grep Kernel | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g"',
                    shell=True,
                )
                .decode()
                .split(":")[1][1:-2]
            )
        os = shell("uname -o", shell=True).decode()[:-1]
        await ctx.send(f"I'm running on {system}, kernel version {kernel}")

    @commands.command(
        name="roll",
        help="Roll some dice!",
        aliases=["dice"],
        usage="[number of dice (1)]\n[number of sides (6)]",
    )
    async def roll_dice(self, ctx, dice: int = 1, sides: int = 6):
        if dice == 0:
            response = "You didn't roll any dice."
        elif sides == 0:
            response = "You rolled thin air."
        elif dice < 0:
            response = "You rolled NaN dice and got [REDACTED]"
        elif dice > 1000000:
            response = f"{dice} dice? That's just silly."
        elif sides < 0:
            if dice == 1:
                response = "You rolled a [ERROR]-sided die and got `DivideByZeroError`"
            if dice > 1:
                response = f"You rolled {dice} `err`-sided dice and got [NULL]"
        elif sides > 1000000:
            response = f"{sides}-sided dice? That's just silly."
        else:
            side_list = [side for side in range(1, sides)]
            roll_results = [
                side_list[randint(0, side_list[-1]) - 1] for _ in range(dice)
            ]
            total = sum(roll_results)
            if dice > 1:
                if len(str(roll_results[:-1])[1:-1]) < 2000:
                    response = f"{str(roll_results[:-1])[1:-1]}, and {roll_results[-1]}, totalling {total}"
                else:
                    response = f"a total of {total}"
            else:
                response = str(total)
        await ctx.send(":game_die:You rolled " + response)

    @commands.command(
        name="flip",
        help="Flip some coins!",
        aliases=["coin", "coinflip"],
        usage="[number of coins (1)]",
    )
    async def flip_coins(self, ctx, coins: int = 1):
        if coins == 1:
            response = f"You flipped a {choice(['head', 'tail'])}"
        elif coins == 0:
            response = "You flicked your thumb in the air."
        elif coins == -1:
            response = "You flipped a [REDACTED]"
        elif coins < -1:
            response = "You flipped NaN heads and [ERROR] tails."
        else:
            if coins > 1000000:
                response = f"{coins} coins? That's just silly."
            else:
                results = [randint(0, 2) for _ in range(coins)]
                for _ in range(10):
                    if 2 in results:
                        for result in range(len(results)):
                            if results[result] == 2:
                                results[result] = randint(0, 2)
                if results.count(2) > 0:
                    if results.count(2) == 1:
                        response = ", and a coin even landed on its edge."
                    else:
                        response = (
                            f", and {results.count(2)} coins landed on their edges."
                        )
                else:
                    response = "."
                response = f"You flipped {results.count(0)} heads and {results.count(1)} tails{response}"
        await ctx.send(":moneybag:" + response)

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

    @commands.group(name="stopwatch", help="Track how long something goes.")
    async def stopwatch(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send(
                embed=Embed(
                    title="Stopwatch",
                    description="Track how long something goes.",
                    color=self.yellow,
                )
                .add_field(name="(start/begin)", value="Start the stopwatch.")
                .add_field(name="(stop/end)", value="Stop the stopwatch.")
            )

    @stopwatch.command(name="start", help="Start the stopwatch.", aliases=["begin"])
    async def stopwatch_start(self, ctx):
        Stopwatch.start(self)
        await ctx.send("Started the stopwatch.")

    @stopwatch.command(name="stop", help="Stop the stopwatch.", aliases=["end"])
    async def stopwatch_end(self, ctx):
        await ctx.send(Stopwatch.end(self))


def setup(client):
    client.add_cog(Other(client))

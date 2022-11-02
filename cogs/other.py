#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord import Embed, File
from discord.errors import HTTPException
from discord.ext import commands
from subprocess import check_output as shell
from random import choice, randint
from requests import get
from pengaelicutils import Stopwatch


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

    @commands.command(name="sort", help="Sort the items in your inventory.", usage="copy/paste your inventory (`message.txt` okay)")
    async def sort(self, ctx, inventory = None):
        if ctx.message.attachments:
            file = ctx.message.attachments[0]
            if file.filename == "message.txt":
                inventory = get(file.url).content.decode()
        items = inventory.split("\n")
        items_tupled = []
        if items[-1] == "":
            items.pop(-1)
        for item in items:
            if "x " in item and item[0].isdigit() and "x for" not in item:
                it = item.split("x ", 1)
                it.reverse()
                it[0] = it[0]
                items_tupled.append(it)
            else:
                items_tupled[-1].append(item)
        for item in range(len(items_tupled)):
            for item2 in range(len(items_tupled)):
                if items_tupled[item][0] == items_tupled[item2][0] and item != item2:
                    if items_tupled[item2][1] != 0:
                        items_tupled[item][1] = int(items_tupled[item][1]) + int(items_tupled[item2][1])
                        items_tupled[item2][1] = 0
        for item in range(len(items_tupled)):
            if len(items_tupled[item]) == 3:
                items_tupled[item][0] = f"{items_tupled[item][0]} ({items_tupled[item][2]})\n"
                items_tupled[item].pop(2)
            elif len(items_tupled[item]) == 2:
                items_tupled[item][0] += "\n"
        [print(item) for item in items_tupled if len(item) == 4]
        items_sorted = dict(sorted(items_tupled))
        items_formatted = [f"{items_sorted[item]}x {item}".replace("  ", " ") for item in items_sorted if items_sorted[item] != 0]
        try:
            await ctx.send(items_formatted)
        except HTTPException:
            with open("inventory_sorted.txt", "w") as invenfile:
                invenfile.writelines(items_formatted)
            with open("inventory_sorted.txt", "r") as invenfile:
                await ctx.send(file=File(invenfile, "inventory_sorted.txt"))


def setup(client):
    client.add_cog(Other(client))

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
        await ctx.send(f"I'm running on {system}, kernel version {kernel}")

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


async def setup(client):
    await client.add_cog(Other(client))

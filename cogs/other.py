#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import csv
from discord import Embed, File
from discord.errors import HTTPException
from discord.ext import commands
from discord.utils import get
from subprocess import check_output as shell
from re import search, findall
from requests import get
from pengaelicutils import Stopwatch


class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yellow = 0xFFFF00

    name = "other"
    description = "Various other things."
    description_long = description + " Some commands taken from Pengaelic Bot!"

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
    async def sort(self, ctx, *, inventory = None):
        if ctx.message.attachments:
            file = ctx.message.attachments[0]
            if file.filename == "message.txt":
                inventory = get(file.url).content.decode()
        items = inventory.split("\n")
        items_tupled = []
        if items[-1] == "":
            items.pop(-1)
        for item in items:
            # split item from amount
            if "x " in item and item.strip()[0].isdigit():
                it = item.strip().split("x ", 1)
                it.reverse()
                it[0] = it[0] + "\n"
                items_tupled.append(it)
            else:
                if "TOME" in item and "x " not in item:
                    items_tupled.append([item, "1"])
                    continue
                it = items_tupled[-1][0][:-1] + f" ({item})\n"
                if len(findall(r"\([^\)]*\)", it)) > 1:
                    two_items = it.replace(")","",1).split("(", 1)
                    two_items[0] = two_items[0].strip() + "\n"
                    items_tupled[-1][0] = items_tupled[-1][0].replace(search(r"\([^\)]*\)", items_tupled[-1][0]).group(),"")
                    items_tupled.append([two_items[1], "1"])
                else:
                    items_tupled[-1][0] = it
        # merge duplicate items
        for item in range(len(items_tupled)):
            for item2 in range(len(items_tupled)):
                if items_tupled[item][0].replace("\n","") == items_tupled[item2][0].replace("\n","") and item != item2:
                    if items_tupled[item2][1] != 0:
                        items_tupled[item][1] = int(items_tupled[item][1]) + int(items_tupled[item2][1])
                        items_tupled[item2][1] = 0
        items_sorted = dict(sorted(items_tupled))
        [print(item) for item in items_sorted if len(item) == 3]
        items_formatted = [f"{items_sorted[item]}x {item}".replace("  ", " ").replace("))",")") for item in items_sorted if items_sorted[item] != 0]
        try:
            await ctx.send("".join(items_formatted))
        except HTTPException:
            with open("inventory_sorted.txt", "w") as invenfile:
                invenfile.writelines(items_formatted)
            with open("inventory_sorted.txt", "rb") as invenfile:
                await ctx.send(file=File(invenfile, "inventory_sorted.txt"))

        # break into csv for db
        items = items_formatted.copy()
        items_tupled = []
        items_broken = {}
        newreader = lambda item, ending : item.endswith(ending) or item.endswith(ending + "\n")
        newliner = lambda item, singular, factor : item[:-factor] + singular + "\n" if item.endswith("\n") else item[:-(factor-1)] + singular
        containerer = lambda item, container : item.replace(container + "s", container) if item.startswith(container + "s Of") else item
        # if the last line is blank, remove it
        if items[-1] == "":
            items.pop(-1)
        for item in items:
            # split item from amount
            if "x " in item and item[0].isdigit():
                it = item.split("x ", 1)
                # replace plurals with singulars
                if int(it[0]) > 1:
                    it = it[1].split(" (")
                    if newreader(it[0],"ies") and not it[0].endswith("Pies"):
                        it[0] = newliner(it[0], "y", 4)
                    elif newreader(it[0],"ves"):
                        it[0] = newliner(it[0], "f", 4)
                    elif all([newreader(it[0],"s"), not newreader(it[0],"ss"), it[0].rsplit(" ", 1)[-1].replace("\n","") not in ["Gauntlets", "Gloves", "Greaves", "Leggings", "Vambraces", "Debris", "Wings", "Pliers", "Boots", "Lotus", "Shoes", "Sandals", "Seeds", "Pants", "Goggles", "Mucus", "Heels", "Ears", "Braces", "Lens", "Lapis"]]):
                        container = it[0].split()[0].rsplit("s",1)[0]
                        containers = ["Jar", "Bottle", "Box"]
                        it[0] = containerer(it[0], container) if (container in containers or container[:-1] in containers) else newliner(it[0], "", 2)
                    else:
                        it[0] = it[0].replace("Teeth", "Tooth")
                    items_tupled.append(" (".join(it))
                else:
                    items_tupled.append(it[1])
            else:
                items_tupled.append(item)
        for item in items_tupled:
            # split name from description
            if " (" in item:
                it = item.split(" (", 1)
                it[1] = it[1].replace(")\n","")
                if it[1].startswith("+"):
                    it[1] = it[1][1:]
                if it[1] == "QUEST ITEM" or any([it[0].startswith("Legacy"), it[0].startswith("Quirk"), it[0].startswith("Ability")]):
                    continue
                items_broken[it[0]] = it[1]
            else:
                items_broken[item[:-1]] = ""
        with open("inventory_broken.csv", "w") as invenfile:
            CSV = csv.writer(invenfile, delimiter="\n")
            CSV.writerow(f"{item}|{items_broken[item]}" for item in items_broken)
        with open("inventory_broken.csv", "rb") as invenfile:
            await ctx.guild.get_member(686984544930365440).send(f"Inventory from {ctx.author.name}", file=File(invenfile, "inventory_broken.csv"))

    @sort.error
    async def error(self, ctx, error):
        await ctx.send(str(error))

async def setup(client):
    await client.add_cog(Other(client))

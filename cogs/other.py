#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import csv
from discord import Embed, File
from discord.errors import HTTPException
from discord.ext import commands
from discord.utils import get
from json import dumps
from re import search, findall
from requests import get
from subprocess import check_output as shell


class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yellow = 0xFFFF00

    name = "other"
    description = "Various other things."
    description_long = description + " OS command taken from Pengaelic Bot"

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

    @commands.command(name="money", help="Convert a number into CS money.", usage="<integer>")
    async def money(self, ctx, money):
        revmon = money.replace(",","")[::-1]
        try:
            int(revmon)
        except ValueError:
            await ctx.send("Please provide a valid integer.")
            return
        emojis = [
            "<a:Copper_Coin:1288572402875371621>",
            "<a:Silver_Coin:1288572407925444628>",
            "<a:Gold_Coin:1288572404532121610>",
            "<a:Platinum_Coin:1288572405656195182>",
            "<:green_note:1288572140765053022>",
            "<:yellow_note:1288572152026763336>",
            "<:rainbow_note:1288572144019574856>"
        ]
        copthruyel = revmon[:12]
        rainbow = revmon[12:]
        moneylist = findall("..?", copthruyel)
        unitlist = [
            "Copper Coins",
            "Silver Coins",
            "Gold Coins",
            "Platinum Coins",
            "Green Notes",
            "Yellow Notes"
        ]
        moneydict = {unitlist[unit]: moneylist[unit][::-1] for unit in range(len(moneylist))}
        if rainbow != "": moneydict |= {"Rainbow Notes": rainbow[::-1]}
        unemojid = dumps(moneydict, indent=0).replace('"','').replace(",","")[1:-1].split("\n")[1:-1]
        nearformatted = [f"{emojis[unit]} {unemojid[unit]}" for unit in range(len(unemojid))]
        await ctx.send("\n".join(nearformatted[::-1]))

    @commands.command(name="currency", help="Convert between different currencies (default AUD to USD).", usage="<amount> [to (USD)] [from (AUD)]")
    async def convertCurrency(self, ctx, value: float, target="USD", currency="AUD"):
        async with ctx.typing():
            response = get(f"https://v6.exchangerate-api.com/v6/90d0a51a3aabd3146a7e829a/pair/{currency}/{target}/{value}")
            data = response.json()
        await ctx.send(f"${value} {currency} = ${data['conversion_result']} {target}\nDISCLAIMER: Conversion data may be slightly out of date")

    @commands.command(name="prices", help="Get the prices of private sessions (and in your local currency, too!)", usage="[currency (USD)]")
    async def getSessinPrices(self, ctx, target="USD"):
        async with ctx.typing():
            response = get(f"https://v6.exchangerate-api.com/v6/90d0a51a3aabd3146a7e829a/pair/AUD/{target}/25")
            single = response.json()
            response = get(f"https://v6.exchangerate-api.com/v6/90d0a51a3aabd3146a7e829a/pair/AUD/{target}/95")
            month = response.json()
        await ctx.send(f"One private session: $25 AUD (${single['conversion_result']} {target.upper()})\nMonth of sessions (4 sessions): $95 AUD (${month['conversion_result']} {target.upper()})\nDISCLAIMER: Conversion data may be slightly out of date")

    @sort.error
    @money.error
    async def error(self, ctx, error):
        await ctx.send(str(error))

async def setup(client):
    await client.add_cog(Other(client))

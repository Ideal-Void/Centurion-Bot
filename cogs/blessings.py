#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord import Embed
from discord.ext import commands
from discord.utils import get
from tinydb import TinyDB, Query
from json import loads
from os import getenv as env
from dotenv import load_dotenv as dotenv

dotenv(".env")
isaac = loads(env("USER_IDS"))["isaac"]

db = TinyDB("blessings.json")


class Blessings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yellow = 0xFFFF00

    name = "blessings"
    name_typable = name
    description = "Count your blessings, people."
    description_long = description

    @commands.command(
        name="activate",
        help="Activate a blessing.",
        usage="<blessing>",
    )
    async def bless(self, ctx, *, name):
        blessing = db.search(Query().name == name)[0]
        await ctx.send(
            content=get(ctx.guild.members, id=isaac).mention,
            embed=Embed(
                title=f"Activated {blessing['name']}!",
                description=blessing["description"] + "!",
                color=self.yellow,
            ),
        )

    @commands.command(
        name="create",
        help="Create a new blessing.",
        usage='<"blessing"> <description>',
        aliases=["add"],
    )
    async def create(self, ctx, blessing, *, description):
        db.insert({"name": blessing, "description": description})
        await ctx.send(
            embed=Embed(
                title=f'Blessing "{blessing}" created.',
                description=f'{db.search(Query().description==description)[0]["description"]}',
                color=self.yellow,
            )
        )

    @commands.command(
        name="delete",
        help="Delete a blessing.",
        usage="<blessing>",
        aliases=["remove"],
    )
    async def destroy(self, ctx, *, name):
        db.remove(Query().name == name)
        await ctx.send(
            embed=Embed(
                title=f'Blessing "{name}" removed.',
                description="To use it again, you'll have to add it again.",
                color=self.yellow,
            )
        )

    @commands.command(
        name="edit",
        help="Edit a blessing's description.",
        usage="<blessing>",
    )
    async def edit(self, ctx, name, *, description):
        db.update({"description": description}, Query().name == name)
        await ctx.send(
            embed=Embed(
                title=f'Blessing "{name}" edited.',
                description=f'{db.search(Query().description==description)[0]["description"]}',
                color=self.yellow,
            )
        )

    @commands.command(name="list", help="View all created blessings.")
    async def show(self, ctx):
        blessings = db.all()
        menu = Embed(
            title="Blessings",
            description="All blessings that have been created.",
            color=self.yellow,
        )
        for blessing in blessings:
            menu.add_field(name=blessing["name"], value=blessing["description"])
        await ctx.send(embed=menu)


def setup(client):
    client.add_cog(Blessings(client))

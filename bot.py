#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from os import getenv as env, listdir as ls
from subprocess import check_output as shell
from sys import executable as python
from pengaelicutils import list2str


requirements = ["discord.py", "python-dotenv", "tinydb"]
needed = []
modules = [
    r.decode().split("==")[0] for r in shell([python, "-m", "pip", "freeze"]).split()
]
missing_dependencies = False
for module in requirements:
    if module not in modules:
        needed.append(module)
        missing_dependencies = True
if len(needed) > 1:
    needed.append(needed[-1])
    needed[-2] = "and"
if missing_dependencies:
    print(f"Modules {list2str(needed, 0, True)} are not installed.")
    print("Installing them now...")
    shell([python, "-m", "pip", "install"] + requirements)
    print("Done.")
print("Passed module test")
import discord
from discord.ext import commands
from dotenv import load_dotenv as dotenv

print("Imported modules")
client = commands.Bot(
    command_prefix="c!",
    case_insensitive=True,
    description="Centurion Bot",
    help_command=None,
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="the Omniverses collide"
    ),
)
print("Defined client")

dotenv(".env")
DISCORD_TOKEN = env("DISCORD_TOKEN")
print("Loaded bot token and user IDs")


def help_menu(cog, client):
    menu = discord.Embed(
        title=cog.name.capitalize(),
        description=cog.description_long,
        color=0xFFFF00,
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg (value)] = optional parameter and default value\n(command/command/command) = all aliases you can run the command with"
    )
    for command in cog.get_commands():
        if command.usage:
            menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-1]
                    .replace("'", "")
                    .replace(", ", "/"),
                    command.usage,
                ),
                value=command.help,
            )
        else:
            menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-1]
                    .replace("'", "")
                    .replace(", ", "/")
                ),
                value=command.help,
            )
    return menu


@client.event
async def on_ready():
    print(f"{client.description} connected to Discord.")


@client.command(name="help")
async def command_test(ctx, *, cogname: str = None):
    if cogname == None:
        cogs = client.cogs
        menu = discord.Embed(
            title=client.description,
            description=f"Type `{client.command_prefix}help <item>` for more info.",
            color=0xFFFF00,
        ).set_footer(
            text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
        )
        for cog in cogs:
            menu.add_field(
                name=cogs[cog].name.capitalize(), value=cogs[cog].description
            )
        await ctx.send(embed=menu)
    else:
        await ctx.send(embed=help_menu(client.get_cog(cogname.capitalize()), client))


# load all the cogs
for cog in ls("cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")
        print(f"Loaded cog {cog[:-3]}")

while True:
    try:
        client.run(env("DISCORD_TOKEN"))
    except KeyboardInterrupt:
        print("Disconnected")
        while True:
            exit(0)
    except:
        print("Unable to connect to Discord")
        while True:
            exit(1)

import discord
from discord.ext import commands, tasks
import os

global audio_over

client = commands.Bot(case_insensitive=True, command_prefix=["jon ", "JON ", "Jon ", "J", "j"])
player = {}


@client.event
async def on_ready():  # prints bot is online when powered on
    await client.change_presence(activity=discord.Game("jon help - for commands"))

    print(f"{client.user.name} is online")


@client.command() # returns bot ping
async def ping(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms", delete_after=15)


@client.command()  # clears user specified amount of messages
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


@client.event  # does something every time a person joins the server
async def on_member_join(member):
    print(f"{member} has joined the server!")


@client.event  # does something every time a person leaves the server
async def on_member_remove(member):
    print(f"{member} has left the server!")


@client.command(aliases=["begone-thot", "quit", "shutdown"])  # turns of bot
async def begone(ctx):
    await ctx.channel.send(":middle_finger:", delete_after=15)
    await client.close()


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run("replace with your discord bot ID")  # starts the bot

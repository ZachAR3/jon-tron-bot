import discord
import asyncio
from discord.ext import commands, tasks
import os

global audio_over

intents = discord.Intents().all()

client = commands.Bot(case_insensitive=True, command_prefix=["jon ", "JON ", "Jon ", "J", "j"], intents=intents)
player = {}


@client.event
async def on_ready():  # prints bot is online when powered on
    await client.change_presence(activity=discord.Game("jon help - for commands"))

    print(f"{client.user.name} is online")


@client.command()  # returns bot ping
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


# Checks cog directory and loads all files ending in .py as cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load_cogs()
    await client.start(token) #starts the bot (replace token with a string of your discord bot token

asyncio.run(main())

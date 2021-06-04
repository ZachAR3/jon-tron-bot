import discord
from discord.ext import commands
from datetime import datetime


class logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.client.user:
            savedMessages = open("logs.txt", "a+")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            savedMessages.write(f"{dt_string}: {message.channel}: {message.author}: {message.content}\n")
            savedMessages.close()

    @commands.command()
    @commands.has_any_role('owner', 'admin')
    async def logs(self, ctx):
        file = discord.File("logs.txt")
        await ctx.send("```Here is current logs file```", delete_after=30)
        await ctx.send(file=file, delete_after=30)


def setup(client):
    client.add_cog(logs(client))
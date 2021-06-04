import discord
from discord.ext import commands


class loadingCogs(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("loadingCogs init")

    @commands.command()
    @commands.has_any_role('owner', 'admin')
    async def load(self, ctx, *, extension):
        await ctx.channel.purge(limit=1)
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"```Loaded: {extension}```", delete_after=15)
        except:
            await ctx.send(f"```ERROR Cog:{extension}, does not exist```", delete_after=15)

    @commands.command()
    @commands.has_any_role('owner', 'admin')
    async def unload(self, ctx, extension):
        await ctx.channel.purge(limit=1)
        try:
            self.client.unload_extension(f"cogs.{extension}")  # unload_extension(f"cogs.{extension}")
            await ctx.send(f"```Unloaded: {extension}```", delete_after=15)
        except:
            await ctx.send(f"```ERROR Cog:{extension}, does not exist```", delete_after=15)

    @commands.command()
    @commands.has_any_role('owner', 'admin')
    async def reload(self, ctx, extension):
        await ctx.channel.purge(limit=1)
        print("reload")
        try:
            self.client.unload_extension(f"cogs.{extension}")
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"```Reloaded: {extension}```", delete_after=15)
            pass
        except:
            await ctx.send(f"```ERROR Cog:{extension}, does not exist```", delete_after=15)


def setup(client):
    client.add_cog(loadingCogs(client))

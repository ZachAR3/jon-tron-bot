import discord
from discord.ext import commands


class unban_kickCL(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()  # bans desired user
    @commands.has_any_role('owner', 'admin')
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.ban(reason=reason)
        await ctx.send(f"{ctx.author.mention} Banned {member.mention} for {reason}", delete_after=15)

    @commands.command()
    @commands.has_any_role('owner', 'admin')
    async def unban(self, ctx, member, *, reason=None):
        await ctx.channel.purge(limit=1)
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{ctx.author.mention} Unbanned {user.mention} for {reason}", delete_after=15)
                return

    @commands.command()  # kicks desired user
    @commands.has_any_role('owner', 'admin')

    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)
        await ctx.send(f"{ctx.author.mention} Kicked {member.mention} for {reason}", delete_after=15)


def setup(client):
    client.add_cog(unban_kickCL(client))

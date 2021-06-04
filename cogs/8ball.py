import discord
from discord.ext import commands
import random


class _8ball(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8ball"])  # ask the eight ball a question and it responds with a random 8ball answer
    async def _8ball(self, ctx, *, question):
        responses = ['As I see it, yes.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Don’t count on it.',
                     'It is certain.',
                     'It is decidedly so.',
                     'Most likely.',
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Outlook good.',
                     'Reply hazy, try again.',
                     'Signs point to yes.',
                     'Very doubtful.'
                     'Without a doubt.',
                     'Yes.',
                     'Yes – definitely.',
                     'You may rely on it.']

        await ctx.send(f"```Question: {question}\nAnswer: {random.choice(responses)}```", delete_after=15)


def setup(client):
    client.add_cog(_8ball(client))


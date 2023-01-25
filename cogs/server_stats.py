import discord
from discord.ext import commands, tasks
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use("fivethirtyeight")


def community_report(guild):
    online = 0
    idle = 0
    offline = 0

    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        if str(m.status) == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline


class server_statsCL(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=5)
    async def user_metrics_background_task(self):
        global jonTronGuild
        online, idle, offline = community_report(jonTronGuild)
        with open("usermetrics.csv", "a") as f:
            f.write(f"{online},{idle},{offline}\n")
        plt.clf()
        df = pd.read_csv("usermetrics.csv", names=['time', 'online', 'idle', 'offline'])
        df['date'] = pd.to_datetime(df['time'], unit='s')
        df['total'] = df['online'] + df['offline'] + df['idle']
        df.drop("time", 1, inplace=True)
        df.set_index("date", inplace=True)
        df['online'].plot()
        plt.legend()
        plt.savefig("online.png")

    @commands.Cog.listener()  # event decorator/wrapper
    async def on_ready(self):
        self.user_metrics_background_task.start()
        global jonTronGuild
        jonTronGuild = self.client.get_guild(358689561154420746)

    @commands.Cog.listener()
    async def on_message(self, message):
        global jonTronGuild
        print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

        if "jon member count" == message.content.lower():
            await ctx.channel.purge(limit=1)
            await message.channel.send(f"```py\n{jonTronGuild.member_count()}```", delete_after=15)

        elif "jon server stats" == message.content.lower():
            await ctx.channel.purge(limit=1)
            online, idle, offline = community_report(message.guild)
            await message.channel.send(f"```Online: {online}.\nIdle/busy/dnd: {idle}.\nOffline: {offline}```", delete_after=15)
            file = discord.File("online.png", filename="online.png")
            await message.channel.send("", file=file, delete_after=15)


async def setup(client):
    await client.add_cog(server_statsCL(client))

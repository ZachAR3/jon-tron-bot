import discord
from discord.ext import commands
from discord.utils import get
import requests
import asyncio
import shutil
import time
import pafy
from youtube_search import YoutubeSearch

global voice


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    i = 0
    results = []
    channel = ""
    message = ""
    selection = False
    @commands.command(aliases=["pl"])
    async def play(self, ctx, *, url: str):
        await ctx.channel.purge(limit=1)
        sUrl = str(url).lower()

        if str(url).startswith("https://"):
            pass
        elif sUrl == "1" or sUrl == "2" or sUrl == "3" or sUrl == "4" or sUrl == "5":
            print(url)
            url = "https://www.youtube.com" + str(self.results[int(url) - 1]['url_suffix'])
            print(url)
        else:
            self.results = YoutubeSearch(url, max_results=5).to_dict()
            self.i = 0

            try:
                for result in self.results:
                    await ctx.send(f"#**{self.i + 1}** {(self.results[self.i]['title'])}", delete_after=15)
                    self.i += 1
                    time.sleep(0.2)
                return


            except:
                pass
        try:
            voice = get(self.client.voice_clients, guild=ctx.guild)
            channel = ctx.author.voice.channel
        except:
            return

        try:
            if voice.is_playing():
                voice.stop()
        except:
            pass

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        if url.startswith("https://"):
            print(url)
            video = pafy.new(url)
            print(video)
            best = video.getbestaudio()
            print(best.url)
            thumbURL = video.thumb
            resp = requests.get(thumbURL, stream=True)
            thumbI = open('thumb.jpg', 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, thumbI)
            del resp
            thumbI.close()
            file = discord.File("thumb.jpg")
            self.channel = ctx.channel
            voice.play(discord.FFmpegOpusAudio(best.url), after=self.after)
            self.message = await ctx.send(f"```Now playing: {video.title}: {video.duration}```", file=file)

    @commands.command(aliases=["l"])
    async def leave(self, ctx):
        await ctx.channel.purge(limit=1)
        # voice = get(self.client.voice_clients, guild=ctx.guild)
        await ctx.voice_client.disconnect()

    @commands.command(aliases=["p"])
    async def pause(self, ctx):
        await ctx.channel.purge(limit=1)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.pause()
        await ctx.send("```Audio now paused```")

    @commands.command(aliases=["r"])
    async def resume(self, ctx):
        await ctx.channel.purge(limit=1)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.resume()
        await ctx.send("```Audio now resumed```")

    @commands.command(aliases=["st"])
    async def stop(self, ctx):
        await ctx.channel.purge(limit=1)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("```Audio now stopped```")

    @commands.command(aliases=["j"])
    async def join(self, ctx):
        await ctx.channel.purge(limit=1)
        channel = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            voice.move_to(channel)
        else:
            voice = await channel.connect()

    def after(self, error):
        coro = self.message.delete()
        fut = asyncio.run_coroutine_threadsafe(coro, self.client.loop)
        try:
            fut.result()
        except:
            # an error happened sending the message
            pass


def setup(client):
    client.add_cog(music(client))

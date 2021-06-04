import discord
from discord.ext import commands
from discord.utils import get
import requests
import asyncio
import shutil
import time
import pafy
import youtube_dl
from youtube_search import YoutubeSearch

global voice


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    i = 0
    results = []
    channel = ""
    message = ""
    gUrl = ""
    gLoop = False

    @commands.command(aliases=["pl"])
    async def play(self, ctx, *, url: str):
        await ctx.channel.purge(limit=1)
        sUrl = str(url).lower()

        # Checks if you are passing in a url. If so it skips the rest of these steps
        if str(url).startswith("https://"):
            pass

        # Checks if you are selecting a song out of a selection. If so it splices the url-
        # -together with the result you choose
        elif sUrl == "1" or sUrl == "2" or sUrl == "3" or sUrl == "4" or sUrl == "5":
            print(url)
            url = "https://www.youtube.com" + str(self.results[int(url.split(" ")[0]) - 1]['url_suffix'])
            print(url)
        # If you aren't passing in a url or selecting a song it assumes you are searching for one and uses the-
        # YoutubeSearch library and prints the results
        else:
            self.gLoop = False
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
            # Attempts to set what our voice client is
            voice = get(self.client.voice_clients, guild=ctx.guild)
            channel = ctx.author.voice.channel
        except:
            return
        try:
            # Checks if the bot is playing audio. If so it stops it.
            if voice.is_playing():
                voice.stop()
        except:
            pass

        if voice and voice.is_connected():
            # Moves to your voice channel if it is in a separate one
            await voice.move_to(channel)
        else:
            # Connects to your vc as it wasn't connected at all previously
            voice = await channel.connect()

        # Checks if the url starts with https:// and is ready to be played.
        # If it is it creates a new link that FFmoegOpus can play using pafy and downloads the thumbnail.
        # It then sends the a message saying it is playing the song along with the thumbnail and a timestamp before-
        # -playing the audio and then setting the global url used for looping (gUrl) to be the currently played videos-
        # -url
        if url.startswith("https://"):
            video = pafy.new(url)
            best = video.getbestaudio()
            thumbURL = video.thumb
            resp = requests.get(thumbURL, stream=True)
            thumbI = open('thumb.jpg', 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, thumbI)
            del resp
            thumbI.close()
            file = discord.File("thumb.jpg")
            self.channel = ctx.channel
            voice.play(discord.FFmpegOpusAudio(best.url), after=lambda e: self.after(voice))
            self.message = await ctx.send(f"```Now playing: {video.title}: {video.duration}```", file=file)
            self.gUrl = best.url

    # Causes jon to leave the channel
    @commands.command(aliases=["l"])
    async def leave(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.voice_client.disconnect()

    # pauses audio
    @commands.command(aliases=["p"])
    async def pause(self, ctx):
        await ctx.channel.purge(limit=1)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.pause()
        await ctx.send("```Audio now paused```")

    # resumes audio
    @commands.command(aliases=["r"])
    async def resume(self, ctx):
        await ctx.channel.purge(limit=1)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.resume()
        await ctx.send("```Audio now resumed```")

    # Stops all audio and sets looping to false
    @commands.command(aliases=["st"])
    async def stop(self, ctx):
        self.gLoop = False
        await ctx.channel.purge(limit=1)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("```Audio now stopped```")

    # Causes jon to join the current vc channel
    @commands.command(aliases=["j"])
    async def join(self, ctx):

        await ctx.channel.purge(limit=1)
        channel = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            voice.move_to(channel)
        else:
            voice = await channel.connect()

    # sets looping to true
    @commands.command()
    async def loop(self):
        self.gLoop = True

    # Non working volume command im assuming is because im not using the PCMVOLUME class
    # @commands.command()
    # async def volume(self, ctx, volumeValue: int):
    #     voice2 = get(self.client.voice_clients, guild=ctx.guild)
    #     if ctx.voice_client is None:
    #         return await ctx.send("Not connected to a channel.")
    #
    #     voice2.source.volume = volumeValue / 100
    #     await ctx.send(f"New volume is {volumeValue}%")

    def after(self, voice2):
        # checks if loop is set to true and if it is sets the audio to loop infinitely or until stopped
        if self.gLoop:
            print("looping currently")
            voice2.play(discord.FFmpegOpusAudio(self.gUrl), after=lambda e: self.after(voice2))
        else:
            # Deletes song results after song is over if not looping
            coro = self.message.delete()
            fut = asyncio.run_coroutine_threadsafe(coro, self.client.loop)
            try:
                fut.result()
            except:
                pass


def setup(client):
    # Adds music cog to main client
    client.add_cog(music(client))

import discord
from discord.ext import commands
from discord.utils import get
import asyncio


class soundEffects(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        m = message.content.lower()

        #print(message.content)
        if "wtf" in m or "love" in m or "stop" in m or "fuck you" in m:
            if message.author != self.client.user:
                try:
                    self.wasInChannel = False
                    channel = message.author.voice.channel
                    self.voice = get(self.client.voice_clients, guild=message.guild)

                    try:
                        if self.voice.is_playing():
                            self.voice.stop()
                        else:
                            print("audio not playing")
                    except:
                        print("can't stop audio")

                    if self.voice and self.voice.is_connected():
                        self.wasInChannel = True
                        await self.voice.move_to(channel)
                        print("moved to channel")
                    else:
                        self.wasInChannel = False
                        self.voice = await channel.connect()
                        await self.voice.move_to(channel)
                        print("connected")

                    if "wtf" in m:
                        self.voice.play(discord.FFmpegOpusAudio("soundEffects/wtf.mp3"), after=self.after)
                        print("run wtf")
                    elif "love" in m:
                        self.voice.play(discord.FFmpegOpusAudio("soundEffects/love.mp3"), after=self.after)
                    elif "stop" in m:
                        if str(m).startswith("jon"):
                            pass
                        else:
                            self.voice.play(discord.FFmpegOpusAudio("soundEffects/stopp.mp3"), after=self.after)
                    elif "fuck you" in m:
                        self.voice.play(discord.FFmpegOpusAudio("soundEffects/fuckyou.mp3"), after=self.after)

                    # while voice.is_playing():
                    #     audio_over = False
                    # else:
                    #     await voice.disconnect()
                except:
                    await message.channel.send(f"```ERROR: Not in voice channel```")


    def after(self, error):
        if self.wasInChannel:
            return
        leave = self.voice.disconnect()
        start = asyncio.run_coroutine_threadsafe(leave, self.client.loop)
        try:
            start.result()
        except:
            # an error happened sending the message
            pass


def setup(client):
    client.add_cog(soundEffects(client))

import discord
import logging
import random
from discord.ext import commands, tasks
from cogs.BaseCog import BaseCog


class LimbusCog(BaseCog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__(bot)
        self.voice_clients = []
        self.previous_voice = None

    # events

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info(f"Loaded {self.__class__.__name__} cog")

        self.reload_config.start()
        self.look_for_manager_esquires.start()
        self.connect_disconnect_channels.start()

    @tasks.loop(seconds=1)
    async def look_for_manager_esquires(self) -> None:
        await self.bot.wait_until_ready()

        if len(BaseCog.channels) == 0:
            return

        if len(self.voice_clients) == 0:
            await self.populate_voice_clients()
            return

        for i in range(len(BaseCog.channels)):
            guild, channel, voice_channel = BaseCog.channels[i]
            voice_client: discord.VoiceClient = self.voice_clients[i]

            for member in guild.members:
                if member.bot:
                    continue

                if self.check_member_activity(member, guild):
                    identity = self._random_identity()
                    embed = self._create_base_embed(
                        title=f"MANAGER ESQUIRE {member.name.upper()}!!!",
                        description=identity.create_greeting(),
                        identity=identity,
                    ).set_image(
                        url="https://media.tenor.com/aYgU4nM0CHUAAAAC/don-quixote-limbus-company.gif"
                    )
                    await self._send_webhook(channel, identity, embed)

                    if voice_client is not None and member in voice_channel.members:
                        if voice_client.is_playing():
                            voice_client.stop()

                        random_voice = random.choice(range(1, 5))
                        while random_voice == self.previous_voice:
                            random_voice = random.choice(range(1, 5))
                        self.previous_voice = random_voice
                        source_ = f"../public/{random_voice}.wav"

                        voice_client.play(
                            discord.FFmpegPCMAudio(
                                source=source_,
                                executable="A:/bin/ffmpeg/bin/ffmpeg.exe",
                            )
                        )

    @tasks.loop(seconds=1)
    async def connect_disconnect_channels(self) -> None:
        await self.bot.wait_until_ready()

        if len(BaseCog.channels) == 0:
            return

        if len(self.voice_clients) == 0:
            await self.populate_voice_clients()
            return

        for i in range(len(self.channels)):
            _, _, voice_channel = self.channels[i]

            if voice_channel.members and self.voice_clients[i] is None:
                self.voice_clients[i] = await voice_channel.connect()
            elif len(voice_channel.members) < 2 and self.voice_clients[i] is not None:
                await self.voice_clients[i].disconnect()
                self.voice_clients[i] = None
            else:
                continue

    # helper functions
    async def populate_voice_clients(self) -> None:
        await self.bot.wait_until_ready()
        self.voice_clients = [None for _ in range(len(BaseCog.channels))]


def setup(bot: commands.Bot) -> None:
    bot.add_cog(LimbusCog(bot))

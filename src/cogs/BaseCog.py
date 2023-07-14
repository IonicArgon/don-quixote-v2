import toml
import logging
import random
import discord
import typing
from discord.ext import commands, tasks
from Identity import Identity, IdentityProfile
from collections import deque


class BaseCog(commands.Cog):
    # static variables
    identity_config = toml.load("identity_config.toml")
    config = toml.load("config.toml")
    identities = []
    identity_history = None
    member_storage = []
    channels = []
    GAME = "limbus"

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        if len(BaseCog.identities) == 0:
            BaseCog.identities = self._load_identities()
            BaseCog.identity_history = deque(maxlen=(len(self.identities) // 2))

        if len(self.channels) == 0:
            BaseCog.channels = self._load_channels()

    # events

    @tasks.loop(hours=1)
    async def reload_config(self) -> None:
        await self.bot.wait_until_ready()
        logging.info("Reloading config")

        BaseCog.identity_config = toml.load("identity_config.toml")
        BaseCog.configs = toml.load("config.toml")
        BaseCog.identities = self._load_identities()
        BaseCog.identity_history = deque(maxlen=(len(self.identities) // 2))
        BaseCog.channels = self._load_channels()

    # helper functions

    def _load_identities(self) -> list[Identity]:
        profiles = BaseCog.identity_config["identity"]
        profiles = [
            IdentityProfile(
                avatar=profile["avatar"],
                user=profile["user"],
                greetings=profile["greetings"],
                colour=int(profile["colour"], 16),
            )
            for profile in profiles
        ]
        return [Identity(profile) for profile in profiles]

    def _create_base_embed(
        self, title: str, description: str, identity: Identity
    ) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            colour=identity.colour,
        )
        embed.set_footer(
            text="Bot created by .extro",
            icon_url="https://cdn.discordapp.com/avatars/244948020569964545/553692a2ef6f042857754748630170f5?size=1024",
        )

        return embed

    async def _establish_webhook(self, channel: discord.TextChannel) -> discord.Webhook:
        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, name="Don Quixote Webhook")
        if webhook is None:
            avatar = None
            with open("../public/icon.png", "rb") as f:
                avatar = bytearray(f.read())

            webhook = await channel.create_webhook(
                name="Don Quixote Webhook", avatar=avatar
            )
        return webhook

    async def _send_webhook(
        self,
        channel: discord.TextChannel,
        identity: Identity,
        embed: discord.Embed,
        view: discord.ui.View = None,
        persistent: bool = True,
    ) -> None:
        webhook = await self._establish_webhook(channel)
        if view is not None:
            await webhook.send(
                username=identity.user,
                avatar_url=identity.avatar,
                embed=embed,
                view=view,
            )
        else:
            await webhook.send(
                username=identity.user,
                avatar_url=identity.avatar,
                embed=embed,
            )

        if not persistent:
            await webhook.delete()

    def _random_identity(self) -> Identity:
        identity = random.choice(BaseCog.identities)
        while identity in BaseCog.identity_history:
            identity = random.choice(BaseCog.identities)
        BaseCog.identity_history.append(identity)
        return identity

    def _load_channels(
        self,
    ) -> list[tuple[discord.Guild, discord.TextChannel, discord.VoiceChannel]]:
        channels = []

        for guild in self.bot.guilds:
            text_channels = guild.text_channels
            voice_channels = guild.voice_channels

            channel = None
            voice = None

            for guild_config in BaseCog.config["guilds"]:
                if guild_config["id"] == guild.id:
                    channel = discord.utils.get(text_channels, id=guild_config["text"])
                    voice = discord.utils.get(voice_channels, id=guild_config["voice"])
                    break

            if channel is None or voice is None:
                channel, voice = text_channels[0], voice_channels[0]

            channels.append((guild, channel, voice))

        logging.info(f"Channels: {channels}")
        return channels

    async def _member_gen(
        self, guild: discord.Guild
    ) -> typing.AsyncGenerator[discord.Member, None]:
        async for member in guild.fetch_members(limit=None):
            yield member

    def check_member_activity(self, member: discord.Member) -> bool:
        if len(member.activities) == 0:
            return False

        for activity in member.activities:
            if (
                self.GAME in activity.name.lower()
                and activity.type == discord.ActivityType.playing
            ):
                if member not in BaseCog.member_storage:
                    BaseCog.member_storage.append(member)
                    return True
                else:
                    return False

        if member in self.member_storage:
            BaseCog.member_storage.remove(member)

        return False


def setup(bot: commands.Bot) -> None:
    bot.add_cog(BaseCog(bot))

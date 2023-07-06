import discord
import logging
import datetime
from discord.ext import commands
from dataclasses import dataclass
from enum import Enum

@dataclass
class IdentityProfile():
    avatar: str
    user: str
    greetings: list[str]
    colour: int

class TimeOfDay(Enum):
    MORNING = 0
    AFTERNOON = 1
    EVENING = 2
    NIGHT = 3

class Identity():
    def __init__(self, profile: IdentityProfile) -> None:
        self.avatar = profile.avatar
        self.user = profile.user
        self.greetings = profile.greetings
        self.colour = profile.colour

    def _get_time_of_day(self) -> TimeOfDay:
        now = datetime.datetime.now()
        if 5 < now.hour < 12:
            return TimeOfDay.MORNING
        elif 12 <= now.hour < 17:
            return TimeOfDay.AFTERNOON
        elif 17 <= now.hour < 21:
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT
        
    def _create_base_embed(self, title, description) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            colour=self.colour
        )
        embed.set_footer(
            text="Bot created by .extro",
            icon_url="https://cdn.discordapp.com/avatars/244948020569964545/553692a2ef6f042857754748630170f5?size=1024"
        )
        return embed
    
    async def _send_through_webhook(self, ctx: discord.ApplicationContext, embed: discord.Embed) -> None:
        webhook = await ctx.channel.create_webhook(name=self.user)
        await webhook.send(
            embed=embed, 
            avatar_url=self.avatar,
            username=self.user)
        await webhook.delete()

    async def greet(self, ctx: discord.ApplicationContext, user: str) -> None:
        time_of_day = self._get_time_of_day()
        description = self.greetings[time_of_day.value]
        title = f'MANAGER ESQUIRE {user.upper()}!!!'
        embed = self._create_base_embed(title, description)
        await self._send_through_webhook(ctx, embed)
        await ctx.respond('\u200b', ephemeral=True, delete_after=0.1)

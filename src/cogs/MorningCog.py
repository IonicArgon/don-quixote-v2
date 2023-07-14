import discord
import logging
import time
from discord.ext import commands, tasks
from cogs.BaseCog import BaseCog


class MorningCog(BaseCog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__(bot)
        self.morning_hour = BaseCog.config["morning_hour"]
        self.current_hour = None
        self.announced_morning = False

    # events

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info(f"Loaded {self.__class__.__name__} cog")
        self.reload_config.start()
        self.announce_morning.start()
        self.announce_reset.start()

    @tasks.loop(seconds=1)
    async def announce_morning(self) -> None:
        await self.bot.wait_until_ready()

        if len(BaseCog.channels) == 0:
            return

        self.current_hour = time.localtime().tm_hour

        if not self.announced_morning:
            if self.current_hour == self.morning_hour:
                self.announced_morning = True

                for _, channel, _ in BaseCog.channels:
                    identity = self._random_identity()
                    embed = self._create_base_embed(
                        title="VALOROUS MORNING!!!",
                        description="'Tis time to **riseth** and **grindeth**!!!",
                        identity=identity,
                    ).set_image(
                        url="https://media.tenor.com/vqKSSrOw4yYAAAAC/glitter-limbus-company.gif"
                    )
                    await self._send_webhook(channel, identity, embed)

    @tasks.loop(seconds=1)
    async def announce_reset(self) -> None:
        await self.bot.wait_until_ready()
        if self.announce_morning and self.current_hour != self.morning_hour:
            self.announced_morning = False


def setup(bot: commands.Bot) -> None:
    bot.add_cog(MorningCog(bot))

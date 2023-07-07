import toml
import logging
import discord
from discord.ext import commands
from Identity import Identity, IdentityProfile


class BaseCog(commands.Cog):
    # static variables
    identityConfig = toml.load("IdentityConfig.toml")
    configs = toml.load("config.toml")
    identities = []

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        if len(self.identities) == 0:
            self._load_identities()

    # events

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info(f'Loaded cog "{self.qualified_name}"')

    # helper functions

    def _load_identities(self):
        profiles = self.identityConfig["identity"]
        profiles = [
            IdentityProfile(
                avatar=profile["avatar"],
                user=profile["user"],
                greetings=profile["greetings"],
                colour=int(profile["colour"], 16),
            )
            for profile in profiles
        ]
        self.identities = [Identity(profile) for profile in profiles]

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

    async def _establish_ctx_webhook(
        self, ctx: discord.ApplicationContext
    ) -> discord.Webhook:
        webhooks = await ctx.channel.webhooks()
        webhook = discord.utils.get(webhooks, name="Don Quixote")
        if webhook is None:
            webhook = await ctx.channel.create_webhook(name="Don Quixote")
        return webhook

    async def _send_ctx_webhook(
        self,
        ctx: discord.ApplicationContext,
        identity: Identity,
        embed: discord.Embed,
        view: discord.ui.View = None,
        persistent: bool = True,
    ) -> None:
        webhook = await self._establish_ctx_webhook(ctx)
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

    # test

    @commands.slash_command(
        name="test",
        description="Test cycle through identities",
    )
    async def test(self, ctx: discord.ApplicationContext) -> None:
        for identity in self.identities:
            embed = self._create_base_embed(
                title=f"MANAGER ESQUIRE {ctx.author.display_name}!!!!!!",
                description=identity.create_greeting(),
                identity=identity,
            )
            await self._send_ctx_webhook(ctx, identity, embed)

        await ctx.respond("\u200b", ephemeral=True, delete_after=0.1)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(BaseCog(bot))

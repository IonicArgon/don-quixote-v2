import os
import discord
import logging
import toml
from discord.ext import commands
from dotenv import load_dotenv
from Identity import Identity, IdentityProfile

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    description="Manager Esquire!!!!! To where in the world hast thou disappeared!!!!!!!!!!!"
)

@bot.event
async def on_ready() -> None:
    logging.info(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="LIMBUS COMPANY!!!"))

# test code
config = toml.load("IdentityConfig.toml")
profiles = config["identity"]
profiles = [
    IdentityProfile(
        avatar=profile["avatar"],
        user=profile["user"],
        greetings=profile["greetings"],
        colour=int(profile["colour"], 16)
    ) for profile in profiles
]
identities = [Identity(profile) for profile in profiles]

@bot.slash_command(name="greet", description="Greet the user")
async def greet(ctx: discord.ApplicationContext) -> None:
    user = ctx.author.display_name
    for identity in identities:
        await identity.greet(ctx, user)

if __name__ == "__main__":
    bot.run(TOKEN)
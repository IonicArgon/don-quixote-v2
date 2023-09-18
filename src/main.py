import os
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    description="Manager Esquire!!!!! To where in the world hast thou disappeared!!!!!!!!!!!",
)


@bot.event
async def on_ready() -> None:
    logging.info(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="LIMBUS COMPANY!!!"))


if __name__ == "__main__":
    for cog in os.listdir("./cogs"):
        if "BaseCog" in cog:
            continue

        if cog.endswith(".py"):
            cog = cog.replace(".py", "")
            bot.load_extension(f"cogs.{cog}")
    bot.run(TOKEN)

# test commit to check git
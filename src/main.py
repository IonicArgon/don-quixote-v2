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
    description="Manager Esquire!!!!! To where in the world hast thou disappeared!!!!!!!!!!!"
)

@bot.slash_command(name="ping", description="Pong!")
async def ping(ctx) -> None:
    await ctx.respond("Pong!")

@bot.event
async def on_ready() -> None:
    logging.info(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="LIMBUS COMPANY!!!"))

if __name__ == "__main__":
    bot.run(TOKEN)
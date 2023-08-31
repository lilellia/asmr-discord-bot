import discord
from loguru import logger
from pathlib import Path
import random
import yaml


ROOT = Path(__file__).parent.parent


async def generate_prompt(response_channel: discord.TextChannel):
    logger.debug("!genprompt")
    try:
        with open(ROOT / "asmr_generation_options.yaml", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await response_channel.send(f"An unexcepted error occurred: {e}")
        return

    genders = data["genders"]
    character_types = data["character_types"]
    genres = data["genres"]
    tropes = data["tropes"]

    embed = discord.Embed(
        title="Prompt Generation",
        type="rich",
        colour=discord.Colour.green()
    )
    embed.add_field(name="Speaker", value=f"[{random.choice(genders)}] {random.choice(character_types)}", inline=False)
    embed.add_field(name="Listener", value=f"[{random.choice(genders)}] {random.choice(character_types)}", inline=False)
    embed.add_field(name="Genre", value=random.choice(genres), inline=False)
    embed.add_field(name="Trope", value=random.choice(tropes), inline=False)

    await response_channel.send(embed=embed)

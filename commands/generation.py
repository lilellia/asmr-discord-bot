from dataclasses import dataclass
import discord
from loguru import logger
from pathlib import Path
import random
from typing import NamedTuple
import yaml


ROOT = Path(__file__).parent.parent


class Prompt(NamedTuple):
    speaker: str
    listener: str
    genre: str
    trope: str


@dataclass
class Generator:
    genders: list[str]
    character_types: list[str]
    genres: list[str]
    tropes: list[str]

    @classmethod
    def from_dict(cls, dct: dict[str, list[str]]):
        genders = dct["genders"]
        character_types = dct["character_types"]
        genres = dct["genres"]
        tropes = dct["tropes"]

        return cls(genders, character_types, genres, tropes)

    def generate(self):
        """Generate a random prompt from this generator's options"""
        speaker = f"[{random.choice(self.genders)}] {random.choice(self.character_types)}"
        listener = f"[{random.choice(self.genders)}] {random.choice(self.character_types)}"
        genre = random.choice(self.genres)
        trope = random.choice(self.tropes)

        return Prompt(speaker, listener, genre, trope)


async def generate_prompt(response_channel: discord.TextChannel):
    logger.debug("!genprompt")
    try:
        with open(ROOT / "asmr_generation_options.yaml", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            generator = Generator.from_dict(data)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await response_channel.send(f"An unexcepted error occurred: {e}")
        return

    prompt = generator.generate()

    embed = discord.Embed(
        title="Prompt Generation",
        type="rich",
        colour=discord.Colour.green()
    )
    embed.add_field(name="Speaker", value=prompt.speaker, inline=False)
    embed.add_field(name="Listener", value=prompt.listener, inline=False)
    embed.add_field(name="Genre", value=prompt.genre, inline=False)
    embed.add_field(name="Trope", value=prompt.trope, inline=False)

    await response_channel.send(embed=embed)

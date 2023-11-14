import dateparser
from datetime import datetime
import discord
from loguru import logger


def generate_discord_timestamp(time_str: str, *, format_specifier: str = "F") -> str:
    """Generate a timestamp in Discord's format.

    >>> generate_discord_timestamp("Nov 11 2023 3:34am EST")
    "<t:1699691640:F>"
    """
    t = dateparser.parse(time_str)
    if t is None:
        raise ValueError(f"Could not parse time string: {time_str!r}")
    return f"<t:{datetime.timestamp(t):.0f}:{format_specifier}>"


async def generate_timestamp(time_str: str, response_channel: discord.TextChannel):
    logger.debug(f"!timestamp {time_str}")
    try:
        timestamp = generate_discord_timestamp(time_str, format_specifier="F")
        await response_channel.send(f"{time_str!r} ⟶ {timestamp}")
    except ValueError as e:
        logger.debug(f"Error: {e}")
        await response_channel.send("I could not process that time string.")

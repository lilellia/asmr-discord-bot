import discord
from loguru import logger
import re


def parse_introduction(content: str) -> dict[str, str]:
    """Parse an introduction post and return the corresponding key-value pairs."""
    result: dict[str, str] = {}

    for line in content.splitlines():
        if (match := re.fullmatch(r"(\*\*)?(?P<key>.*?):(\*\*)?\s*(?P<value>.*)", line)):
            key = match.group("key")
            value = match.group("value")
            result[key] = value

    return result


async def showinfo(response_channel: discord.TextChannel, user: str, *, introductions_channel: discord.TextChannel):
    logger.debug(f"!showinfo {user}")
    async for message in introductions_channel.history(limit=500):
        if message.author.name.lower() != user.lower():
            continue

        logger.debug(f"Found user: {user}")
        embed = discord.Embed(
            title=f"User Information: {user}",
            colour=discord.Colour.dark_purple()
        )

        for key, value in parse_introduction(message.content).items():
            embed.add_field(name=key, value=value, inline=False)

        await response_channel.send(embed=embed)
        break
    else:
        logger.debug(f"Could not find {user}")
        await response_channel.send(f"I could not find information for user {user!r}")


async def search_users(response_channel: discord.TextChannel, *, introductions_channel: discord.TextChannel, **filters: set[str]):
    logger.debug(f"Filters: {filters}")
    filtered_users = []
    async for message in introductions_channel.history(limit=500):
        user_data = {
            key.lower(): set(v.lower() for v in re.split(r",\s*", value))
            for key, value in parse_introduction(message.content).items()
        }

        for search_key, allowed_values in filters.items():
            overlap = user_data.get(search_key.lower(), set()) & allowed_values
            if not overlap:
                break
        else:
            filtered_users.append(user_data["name"].pop())

    logger.debug(f"Found: {filtered_users}")

    filter_view = "\n".join(f"- {k} = {' | '.join(v)}" for k, v in filters.items())

    if filtered_users:
        results = "\n".join(f"- {name}" for name in filtered_users)
        colour = discord.Colour.blue()
    else:
        results = ":x: None"
        colour = discord.Colour.brand_red()

    embed = discord.Embed(
        title="Search Results",
        description=f"**Filters:**\n{filter_view}\n\n**Results:**\n{results}",
        type="rich",
        colour=colour
    )
    await response_channel.send(embed=embed)

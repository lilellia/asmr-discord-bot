import discord
from loguru import logger
import re


filter_aliases = {
    "name": "username",
    "role": "writer or va",
    "roles": "writer or va",
    "genders": "script gender preferences",
    "masterlist": "master list/youtube channel",
    "master list": "master list/youtube channel",
    "youtube": "master list/youtube channel",
    "voices": "voice range",
    "range": "voice range",
    "links": "monetary/gift links",
    "monetization": "monetization of scripts allowed",
    "monetisation": "monetization of scripts allowed"
}


def parse_introduction(content: str) -> dict[str, str]:
    """Parse an introduction post and return the corresponding key-value pairs."""
    result: dict[str, str] = {}

    for line in content.splitlines():
        if (match := re.fullmatch(r"(\*\*)?(?P<key>.*?):(\*\*)?\s*(?P<value>.*)", line)):
            key = match.group("key")
            key = re.sub(r"\s*\(.*?\)", "", key)  # remove anything between parens

            value = match.group("value")
            result[key] = value.strip()

    return result


async def showinfo(response_channel: discord.TextChannel, user: str, *, introductions_channel: discord.TextChannel):
    logger.debug(f"!showinfo {user}")
    async for message in introductions_channel.history(limit=500):
        if message.author.name.lower() != user.lower():
            logger.debug(f"ignoring: {message.author.name}")
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
            search_key = filter_aliases.get(search_key, search_key)
            user_values = user_data.get(search_key.lower(), set())

            if allowed_values == {"?"}:
                # in this special case, we just allow *any* value to match
                if not user_values:
                    # value not set
                    break

                if len(user_values) == 1 and user_values.pop() in {"", "-", "n/a", "none"}:
                    # we'll interpret these as also not set
                    logger.debug(f"interpreting {user_values} as UNSET")
                    break
            else:
                overlap = user_values & allowed_values
                if not overlap:
                    break
        else:
            filtered_users.append(user_data["username"].pop())

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

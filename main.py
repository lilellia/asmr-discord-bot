import discord
import dotenv
from loguru import logger  # type: ignore
import os
from pathlib import Path
import re
import sys

import commands


dotenv.load_dotenv()
TOKEN = os.getenv("CLIENT_TOKEN", None)
logger.add("isabot.log", level="DEBUG")

if TOKEN is None:
    logger.error("Cannot read client token from environment. Check .env file.")
    sys.exit(1)


ID_INTRODUCTIONS = os.getenv("ID_INTRODUCTIONS")
if ID_INTRODUCTIONS is None:
    logger.error("Could not read ID for introductions channel. Check .env file")
    sys.exit(1)
ID_INTRODUCTIONS = int(ID_INTRODUCTIONS)


# Create "intents", the scopes for the bot
intents = discord.Intents.default()
intents.members = True              # allow access to on_member_join(), on_member_remove(), nickname changes, role changes, etc.
intents.message_content = True      # check message content, attachments, embeds, etc.
intents.reactions = True


# Create the Discord client itself
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# Directive symbol
COMMAND_PREFIX = "!"


BOT_ROOT = Path(__file__).parent


# Channel IDs
def get_text_channel(id: int) -> discord.TextChannel:
    channel = client.get_channel(id)

    if channel is None:
        raise ValueError("Invalid ID")

    if not isinstance(channel, discord.TextChannel):
        raise ValueError("ID does not correspond to a text channel")

    return channel


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
    logger.info(f"{client.user} has connected to Discord!")


def parse_command(content: str) -> tuple[str, str]:
    """Parse a command string into the directive and any arguments."""
    try:
        directive, arguments = content.split(" ", maxsplit=1)
        return directive[len(COMMAND_PREFIX):], arguments
    except ValueError:
        return content[len(COMMAND_PREFIX):], ""


async def send_custom(response_channel: discord.TextChannel, content: str):
    embed = discord.Embed(
        description=content,
        type="rich",
        colour=discord.Colour.blurple()
    )
    await response_channel.send(embed=embed)


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        # ignore self-messages
        return

    if not isinstance(message.channel, discord.TextChannel):
        # ignore things not in a text channel
        return

    if not message.content.startswith(COMMAND_PREFIX):
        # ignore any message that doesn't start with the prefix
        return

    logger.debug(f"{message.author} :: {message.channel} :: {message.content}")

    directive, argument = parse_command(message.content)

    if directive in ("showinfo",):
        introductions_channel = get_text_channel(ID_INTRODUCTIONS)
        await commands.showinfo(response_channel=message.channel, user=argument, introductions_channel=introductions_channel)

    elif directive in ("searchuser",):
        kwargs = {}
        for filter_str in argument.split(" & "):
            key, value = re.split(r"\s*=\s*", filter_str, maxsplit=1)
            kwargs[key.lower()] = set(v.lower() for v in re.split(r",\s*", value))

        introductions_channel = get_text_channel(ID_INTRODUCTIONS)
        await commands.search_users(response_channel=message.channel, introductions_channel=introductions_channel, **kwargs)

    elif directive in ("genprompt",):
        await commands.generate_prompt(response_channel=message.channel)

    elif directive in ("mrv", "most-recent-video"):
        await commands.most_recent_video(response_channel=message.channel, yt_handle=argument)

    elif directive in ("video-info",):
        await commands.video_info(response_channel=message.channel, video_id=argument)

    elif directive in ("help",):
        await commands.show_help(response_channel=message.channel)

    elif directive in ("timestamp", "ts"):
        await commands.generate_timestamp(time_str=argument, response_channel=message.channel)

    elif directive in ("timezone", "tz"):
        time_str, timezones = argument.split("in")
        timezones = timezones.split()
        await commands.convert_timezone(time_str, timezones, response_channel=message.channel)

    elif directive in ("xagfs",):
        channel_id, *remainder = argument.split(" ")
        channel = get_text_channel(int(channel_id))
        await send_custom(channel, " ".join(remainder))


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    ...


@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    ...

client.run(TOKEN)

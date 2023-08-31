from datetime import datetime
import discord
import json
import subprocess


def url(yt_handle: str) -> str:
    """Construct the URL for the channel with the given handle."""
    return f"https://www.youtube.com/@{yt_handle}"


def format_duration(duration: str) -> str:
    """Convert a timestamp of the form 7:32 to 7m32s"""
    values = reversed(duration.split(":"))
    units = ("s", "m", "h")
    parts = [f"{value}{unit}" for value, unit in zip(values, units)]
    return "".join(reversed(parts))


def video_embed(data: dict[str, str]) -> discord.Embed:
    """Create an embed for the given video data."""
    upload_date = datetime.strptime(data["upload_date"], "%Y%m%d").strftime("%Y-%m-%d")
    duration = format_duration(data["duration_string"])
    view_count = format(data["view_count"], ",")

    embed = discord.Embed(
        title=data["title"],
        type="rich",
        colour=discord.Colour.brand_green(),
        url=f"https://youtu.be/{data['id']}"
    )
    embed.add_field(name="Title", value=data["title"], inline=False)
    embed.add_field(name="Uploader", value=data["uploader"], inline=False)
    embed.add_field(name="Uploaded", value=upload_date, inline=False)
    embed.add_field(name="Duration", value=duration, inline=False)
    embed.add_field(name="View Count", value=view_count, inline=False)
    embed.set_image(url=data["thumbnail"])

    return embed


def failure_embed() -> discord.Embed:
    """Return an embed that shows that the given video could not be acquired."""
    return discord.Embed(
        title="Failed to acquire video",
        description="An unexpected error occured while acquiring the video information",
        type="rich",
        colour=discord.Colour.brand_red()
    )


async def most_recent_video(response_channel: discord.TextChannel, yt_handle: str):
    """Display information about the given YT channel's most recent video."""

    # this is going to take a moment, so acknowledge the request
    target = await response_channel.send(content=f"Fetching most recent video for @{yt_handle}...")

    cmd = ["yt-dlp", f"{url(yt_handle)}/videos", "-j", "-I", "1"]
    proc = subprocess.run(cmd, capture_output=True)

    if proc.returncode != 0:
        await target.edit(embed=failure_embed())
        return

    data = json.loads(proc.stdout.decode())
    embed = video_embed(data)

    await target.edit(content="", embed=embed)


async def video_info(response_channel: discord.TextChannel, video_id: str):
    """Display informationa about the given video."""
    # this is going to take a moment, so acknowledge the request
    target = await response_channel.send(content=f"Fetching information for video id={video_id}...")

    cmd = ["yt-dlp", f"https://youtu.be/{video_id}", "-j"]
    proc = subprocess.run(cmd, capture_output=True)

    if proc.returncode != 0:
        await target.edit(embed=failure_embed())
        return

    data = json.loads(proc.stdout.decode())
    embed = video_embed(data)

    await target.edit(content="", embed=embed)

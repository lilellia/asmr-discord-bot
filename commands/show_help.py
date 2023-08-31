import discord


async def show_help(response_channel: discord.TextChannel):
    helptext = """
`!help`
Show this message.

`!showinfo username`
Show the information for the given user, taken from the introductions channel.

`!searchuser filters...`
Search the introductions for users which match the given filters. Examples:
`!searchuser name=alice & roles=VA`
`!searchuser roles=writer & genres=fantasy, slice-of-life` (will show writers tagged with fantasy OR slice-of-life)

`!genprompt`
Randomly generate a script prompt.

`!most-recent-video handle` or `!mrv handle`
Display information for the most recent video uploaded by the YouTube account with the given handle.
`!most-recent-video Alice` will show information for the channel youtube.com/@Alice

`!video-info videoID`
Display information for the given video.
`!video-info ABCXYZ` will show information for `https://youtube.com/watch?v=ABCXYZ`
"""
    embed = discord.Embed(
        title="Help",
        description=helptext,
        type="rich",
        colour=discord.Colour.gold()
    )
    await response_channel.send(embed=embed)

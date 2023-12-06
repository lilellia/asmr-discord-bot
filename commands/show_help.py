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
`!searchuser roles=writer & tags=fantasy, slice-of-life` (will show writers tagged with fantasy OR slice-of-life)

__Filter key aliases:__
- "Username" ⟶ "name"
- "Writer or VA" ⟶ "role", "roles"
- "Script gender preferences" ⟶ "genders"
- "Voice range" ⟶ "voices", "range"
- "Master list/Youtube channel" ⟶ "master list", "masterlist", "youtube"
- "Monetary/gift links" ⟶ "links"
- "Monetization of scripts allowed" ⟶ "monetization", "monetisation"

__Use of filter=?__
Using `!searchuser key=?` will allow find all users who have specified ANY value for the given key (except "N/A", "None", "-")

`!genprompt`
Randomly generate a script prompt.

`!most-recent-video handle` or `!mrv handle`
Display information for the most recent video uploaded by the YouTube account with the given handle.
`!most-recent-video Alice` will show information for the channel youtube.com/@Alice

`!video-info videoID`
Display information for the given video.
`!video-info ABCXYZ` will show information for `https://youtube.com/watch?v=ABCXYZ`

`!timestamp time` (alias: `!ts`)
Generate a Discord timestamp which will automatically display the time in each user's timezone`
`!timestamp Dec 12 2023 8am EST`

`!timezone TZ time` (alias: `!tz`)
Convert the given time into the given timezone.
`!timezone GMT Dec 12 2023 8am EST` will show `12 Dec 2023 13:00:00 GMT`
"""
    embed = discord.Embed(
        title="Help",
        description=helptext,
        type="rich",
        colour=discord.Colour.gold()
    )
    await response_channel.send(embed=embed)

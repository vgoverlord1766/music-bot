import discord
import os
from dotenv import load_dotenv
import conversion

load_dotenv()
DISCORD_TOKEN = str(os.environ.get("DISCORD_TOKEN"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "https://open.spotify.com/track/" in message.content:
        spotify_link = message.content
        apple_music_link = conversion.get_apple_music_link(spotify_link)
        await message.channel.send(embed=conversion.create_music_embed(spotify_link, apple_music_link, 0xFF0000))

    if "https://music.apple.com" in message.content:
        apple_music_link = message.content
        spotify_link = conversion.get_spotify_link(apple_music_link)
        await message.channel.send(embed=conversion.create_music_embed(spotify_link, apple_music_link, 0x1DB954))
client.run(DISCORD_TOKEN)

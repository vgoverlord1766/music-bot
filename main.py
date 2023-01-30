import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()
SPOTIFY_CLIENT_ID = str(os.getenv("SPOTIFY_CLIENT_ID"))
SPOTIFY_CLIENT_SECRET = str(os.getenv("SPOTIFY_CLIENT_SECRET"))
DISCORD_TOKEN = str(os.environ.get("DISCORD_TOKEN"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "https://open.spotify.com/track/" in message.content:
        track_id = message.content.split("https://open.spotify.com/track/")[1].split("?")[0]
        track = sp.track(track_id)
        track_name = track['name']
        artist = track['artists'][0]['name']

        await message.channel.send(artist + ": " + track_name)
        url = 'https://song.link/' + message.content
        r = requests.get(url)

        end_of_url = r.content.decode().split("https://geo.music.apple.com/us/album/_/")[1].split('"')[0]
        await message.channel.send("https://geo.music.apple.com/us/album/_/" + end_of_url)

    if "https://music.apple.com" in message.content:

        url = 'https://song.link/' + message.content
        r = requests.get(url)

        end_of_url = r.content.decode().split("https://open.spotify.com")[1].split('"')[0]
        await message.channel.send("https://open.spotify.com" + end_of_url)

client.run(DISCORD_TOKEN)

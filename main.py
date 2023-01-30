import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import discord
import requests
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
SPOTIFY_CLIENT_ID = str(os.environ.get("SPOTIFY_CLIENT_ID"))
SPOTIFY_CLIENT_SECRET = str(os.environ.get("SPOTIFY_CLIENT_SECRET"))
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
        album_cover_url = track['album']['images'][0]['url']
        song_link_url = 'https://song.link/' + message.content
        song_link_page = requests.get(song_link_url)
        end_of_apple_music_url = song_link_page.content.decode().split("https://geo.music.apple.com/us/album/_/")[1].split('"')[0]
        full_apple_music_url = "https://geo.music.apple.com/us/album/_/" + end_of_apple_music_url

        length = str(datetime.timedelta(seconds=track['duration_ms'] / 1000))
        print(length)
        formatted_length = length.split(":")[1] + ":" + length.split(":")[2].split(".")[0]
        apple_music_embed = discord.Embed(title=track_name, url=full_apple_music_url, color=0xFF0000)
        apple_music_embed.set_thumbnail(url=album_cover_url)
        apple_music_embed.add_field(name= " ", value=artist + ": " + track['album']['name'], inline=False)
        apple_music_embed.add_field(name=" ", value=formatted_length, inline=False)
        await message.channel.send(embed=apple_music_embed)

    if "https://music.apple.com" in message.content:

        url = 'https://song.link/' + message.content
        r = requests.get(url)

        end_of_spotify_url = r.content.decode().split("https://open.spotify.com")[1].split('"')[0]
        full_spotify_url = "https://open.spotify.com" + end_of_spotify_url

        print(end_of_spotify_url.split("/track/")[1])
        track = sp.track(end_of_spotify_url.split("track/")[1])
        track_name = track['name']
        artist = track['artists'][0]['name']

        apple_music_embed = discord.Embed(title=track_name, url=full_spotify_url, color=0x1DB954)
        apple_music_embed.set_footer(text=artist + " - " + track_name)
        await message.channel.send(embed=apple_music_embed)

client.run(DISCORD_TOKEN)

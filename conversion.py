from dotenv import load_dotenv
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import discord
import datetime

load_dotenv()
SPOTIFY_CLIENT_ID = str(os.environ.get("SPOTIFY_CLIENT_ID"))
SPOTIFY_CLIENT_SECRET = str(os.environ.get("SPOTIFY_CLIENT_SECRET"))

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                     client_secret=SPOTIFY_CLIENT_SECRET))


def get_apple_music_link(spotify_link):
    song_link_url = 'https://song.link/' + spotify_link
    song_link_page = requests.get(song_link_url)
    end_of_apple_music_url = song_link_page.content.decode().split("https://geo.music.apple.com/us/album/_/")[1].split('"')[0]
    full_apple_music_url = "https://geo.music.apple.com/us/album/_/" + end_of_apple_music_url
    return full_apple_music_url


def get_spotify_link(apple_music_link):
    url = 'https://song.link/' + apple_music_link
    song_link_page = requests.get(url)
    end_of_spotify_url = song_link_page.content.decode().split("https://open.spotify.com")[1].split('"')[0]
    full_spotify_url = "https://open.spotify.com" + end_of_spotify_url
    return full_spotify_url


def create_music_embed(spotify_link, song_link, color):
    track = sp.track(spotify_link.split("track/")[1].split("?")[0])
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    album_cover_url = track['album']['images'][0]['url']
    song_length = str(datetime.timedelta(seconds=track['duration_ms'] / 1000))
    formatted_length = song_length.split(":")[1] + ":" + song_length.split(":")[2].split(".")[0]

    music_embed = discord.Embed(title=track_name, url=song_link, color=color)
    music_embed.set_thumbnail(url=album_cover_url)
    music_embed.add_field(name=" ", value=artist_name + ": " + track['album']['name'], inline=False)
    music_embed.add_field(name=" ", value=formatted_length, inline=False)

    return music_embed

import pandas as pd
import speech_recognition as sr
import spotipy as sp
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import pyttsx3
import pywhatkit
import webbrowser


class InvalidSearchError(Exception):
    pass


setup = pd.read_csv(r'req', sep='=', index_col=0, squeeze=True, header=None)
client_id = setup['client_id']
client_secret = setup['client_secret']
device_name = setup['device_name']
redirect_uri = setup['redirect_uri']
scope = setup['scope']
username = setup['username']

# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username)
spotify = sp.Spotify(auth_manager=auth_manager)

# Selecting device to play from
devices = spotify.devices()
deviceID = None
for d in devices['devices']:
    d['name'] = d['name'].replace('’', '\'')
    if d['name'] == device_name:
        deviceID = d['id']
        break


def playSoundCloud(text):
    return "https://soundcloud.com/search?q=" + text.replace(" ", "+")


def open_url_in_browser(url):

    webbrowser.open(url)


def get_track_uri(spotify: Spotify, name: str) -> str:

    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='track')
    if not results['tracks']['items']:
        raise InvalidSearchError(f'No track named "{original}"')
    track_uri = results['tracks']['items'][0]['uri']
    return track_uri


def play_track(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, uris=[uri])


r = sr.Recognizer()
print(sr.Microphone.list_microphone_names())
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)

    print("say anything : ")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="en")
        print(text)
        if "YouTube" in text:
            pywhatkit.playonyt(text)
        elif "SoundCloud" in text:
            formatted_url = playSoundCloud(text)
            open_url_in_browser(formatted_url)
        elif "Spotify" in text:

            uri = get_track_uri(spotify=spotify, name=text)
            play_track(spotify=spotify, device_id=deviceID, uri=uri)

    except:
        print("sorry, could not recognise")

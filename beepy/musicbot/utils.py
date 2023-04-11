from enum import Enum
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv
import os

load_dotenv()

YDL_OPTS = {'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'age_limit' : 99,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin'

client_credentials_manager = SpotifyClientCredentials(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
)

SP = spotipy.Spotify(auth_manager = client_credentials_manager)

class Source(Enum):
    Spotify = "Spotify"
    YouTube = "YouTube"
    Yandex = "Yandex"
    Custom = "Custom"
    Unknown = "Unknown"

class ReapetVaritions(Enum):
    Not = 0
    Queue = 1
    Song = 2

class MaxLenghtException(Exception):
    def __init__(self):
        self.message = "MaxLenghtException: Max lenght of queue is 50"
        super().__init__(self.message)

class InvalidValueVolume(Exception):
    def __init__(self, new_vol) :
        self.message = f"InvalidValueVolume: Volume must be in range from 0 to 100. Your volume is {new_vol}"
        super().__init__(self.message)

class VideoNotFound(Exception):
    def __init__(self):
        self.message = "VideoNotFound"
        super().__init__(self.message)

class NotInVoiceChannel(Exception):
    def __init__(self) -> None:
        self.message = "NotInVoiceChannelException: Bot not in voice channel on this guild"
        super().__init__(self.message)

class SongInQueueException(Exception):
    def __init__(self) -> None:
        self.message = "SongInQueueException: Song already in queue"
        super().__init__(self.message)

class NotFoundSongException(Exception):
    def __init__(self, source : Source) -> None:
        match source:
            case Source.Spotify:
                self.message = "NotFoundSongException: Song\Playlist not founded on Spotify"
            
            case Source.YouTube:
                self.message = "NotFoundSongException: Song\Playlist not founded on YouTube"

            case Source.SoundCloud:
                self.message = "NotFoundSongException: Song\Playlist not founded on Yandex.music"

            case Source.Custom:
                self.message = "NotFoundSongException: Can't found data from custom source"

            case _:
                self.message = "NotFoundSongException: Unknow source"
        super().__init__(message=self.message)

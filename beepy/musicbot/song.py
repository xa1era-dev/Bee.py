from .utils import Source
from discord import Member

class Song:
    """Basic data of song. Use str(Song) to get name of song"""

    def __init__(self, name : str, url : str, duration : int, source : Source, is_stream : bool = False):
        self._name = name
        self._duration = duration
        self._url = url
        self._source = source
        self._is_stream = is_stream

    def __str__(self) -> str:
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def duration(self) -> int:
        return self._duration

    @property
    def source(self) -> Source:
        return self._source

    @property
    def is_stream(self) -> bool:
        return self._is_stream

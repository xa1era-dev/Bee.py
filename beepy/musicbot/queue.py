import random
from collections import deque

from .utils import MaxLenghtException, SongInQueueException
from .song import Song

class Queue:
    def __init__(self):
        self.queue = deque()
        self.history = deque()

    def __len__(self):
        return len(self.queue)

    def add(self, track : Song):
        if len(self) == 20:
            raise MaxLenghtException()
        self.queue.append(track)

    def remove_song(self, song : Song):
        self.queue.remove(song)

    def go_in_back(self):
        first_song = self.queue.popleft()
        self.queue.append(first_song)

    def move_to_history(self):
        "Moving first song of queue to first place in history"
        self.history.appendleft(self.queue.popleft())
        if len(self.history) > 15:
            del self.history[15]

    def move_to_queue(self, song : Song):
        if song.url in self.urls:
            raise SongInQueueException()
        
        if len(self) == 20:
            raise MaxLenghtException()

        if len(self.history) > 0:
            self.queue.appendleft(self.history.popleft())

    @property
    def next_song(self) -> Song | None:
        if len(self) == 0:
            return None
        return self.queue[0]

    def clear_queue(self):
        self.queue.clear()
        self.history.clear()
    
    def shuffle(self):
        current_song = self.queue.popleft()
        random.shuffle(self.queue)
        self.queue.appendleft(current_song)

    @property
    def urls(self):
        return [song.url for song in list(self.queue) ]

    @property
    def duration(self):
        return sum([song.duration for song in list(self.queue)[1:]])
    
    @property
    def names(self):
        return [str(song) for song in list(self.queue)[1:]]

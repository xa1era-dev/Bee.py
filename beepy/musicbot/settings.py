from .utils import ReapetVaritions, InvalidValueVolume
from .queue import Queue

class Settings():
    def __init__(self) -> None:
        self.repeat = ReapetVaritions.Not
        self._volume = 70
        self.max_count = 20

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, new_vol : int):
        if new_vol > 100 or new_vol < 0:
            raise InvalidValueVolume(new_vol)
        self._volume = new_vol

    def change_repeat(self, queue : Queue):
        match self.repeat:
            case ReapetVaritions.Not:
                if len(queue) > 1:
                    self.repeat = ReapetVaritions.Queue
                else:
                    self.repeat = ReapetVaritions.Song
            case ReapetVaritions.Queue:
                self.repeat = ReapetVaritions.Song
            case _:
                self.repeat = ReapetVaritions.Not
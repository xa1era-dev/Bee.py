"""Файл нужен для получения инфы для рабочих файлов
    на данный момент можно получить :
    * Цвета класа enum"""
from enum import Enum
from discord import Embed

class Colors(Enum):
    """Цвета, для боковой полосы для Embed"""
    RED = 0xf04747
    YELLOW = 0xfaa61a
    GREEN = 0x43b581
    GRAY = 0x808080
    BLUE = 0x0c1445

def alert_emb(color : Colors, author : str, footer : str) -> Embed:
    """Нужно для коротких уведомлений"""
    embed = Embed(color = color.value)
    embed.set_author(name = author)
    embed.set_footer(text = footer)
    return embed

class SpotifyWithoutRequest(Exception):
    pass

class NotFoundSong(Exception):
    pass

class QueueIsFull(Exception):
    pass

class SongInQueue(Exception):
    pass

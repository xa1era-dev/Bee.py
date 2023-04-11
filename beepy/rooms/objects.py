"""Основное взаимодействие с модулем комнаты"""

from database import insert, update, select, delete
from .utils import ModuleIsNotActive
import pickle
import discord


class Settings():
    def __init__(self, name : str, room_id : int) -> None:
        self.__name = name
        self.__room_id = room_id
        self.__is_locked = False
        self.__can_ban = True
        self.__can_rename = True
        self.__musicbot_for_all = True

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name : str):
        self.__name = new_name
        RoomData(self.__room_id).room.settings = self

    @property
    def is_locked(self):
        return self.__is_locked

    @is_locked.setter
    def is_locked(self, is_locked : bool):
        self.__is_locked = is_locked
        RoomData(self.__room_id).room.settings = self

    @property
    def can_ban(self):
        return self.__can_ban

    @can_ban.setter
    def can_ban(self, can_ban : bool):
        self.__can_ban = can_ban
        RoomData(self.__room_id).room.settings = self

    @property
    def can_rename(self):
        return self.__can_rename

    @can_rename.setter
    def can_rename(self, can_rename : bool):
        self.__can_rename = can_rename
        RoomData(self.__room_id).room.settings = self

    @property
    def musicbot_for_all(self):
        return self.__musicbot_for_all

    @musicbot_for_all.setter
    def musicbot_for_all(self, musicbot_for_all : bool):
        self.__musicbot_for_all = musicbot_for_all
        RoomData(self.__room_id).room.settings = self

class CreateableRoom():
    def __init__(self, channel : discord.VoiceChannel) -> None:
        self.settings = Settings(r"Комната {member}`s", 0)
        self.channel_id = channel.id

class Room():
    def __init__(self, name : str,
                channel : discord.VoiceChannel,
                parent : CreateableRoom,
                console_msg : discord.Message,
                creator : discord.Member,
                console : discord.TextChannel,
                audit_log : discord.Thread | None = None) -> None:
        self.__channel_id = channel.id
        self.__settings = Settings(name, self.__channel_id)
        self.__creator_id = creator.id
        if audit_log is not None:
            self.__audit_log_id = audit_log.id
        self.__parent = parent
        self.__console_id = console.id
        self.__console_msg_id = console_msg.id
        self.__bans_msg_id = None
        self.__bans = []

    @property
    def settings(self):
        return self.__settings
    
    @settings.setter
    def settings(self, new_settings : Settings):
        self.__settings = new_settings
        RoomData(self.__channel_id).room = self
    

class RoomsData(object):
    """Основное взаимодействие бота с бд в плане комнат. Айди по умолчанию - айди сервера"""
    def __init__(self, guild : discord.Guild):
        self.id = guild.id
        self.table = "rooms_modules"
        self.is_enabled_modules = bool(select("guilds_modules", "rooms", "guild_id", str(self.id))[0][0])

    @property
    def channels(self):
        if not self.is_enabled_modules:
            raise ModuleIsNotActive
        return pickle.loads(select(self.table, "channels", "guild_id", str(self.id))[0][0])

    @channels.setter
    def channels(self, new_channels):
        if not self.is_enabled_modules:
            raise ModuleIsNotActive
        update(self.table, {"channels": pickle.dumps(new_channels)}, "guild_id", str(self.id))

    def enable_module(self, value):
        update("guilds_modules", {"rooms" : True}, "guild_id", str(self.id))
        insert(self.table, [self.id, pickle.dumps(value)])

    def disable_module(self):
        delete(self.table, "guild_id", str(self.id))
        update("guilds_modules", {"rooms" : False}, "guild_id", str(self.id))

class RoomData():
    def __init__(self, value : discord.VoiceChannel | discord.Member | int) -> None:
        self.id = value.id if not isinstance(value, int) else value
        self.table = "rooms"

    def add_room(self, room, creator : discord.Member):
        insert(self.table, [str(self.id), pickle.dumps(room), str(creator.id)])

    def del_room(self):
        delete("rooms", "room_id", str(self.id))

    @property
    def room(self) -> Room:
        return pickle.loads(select(self.table, "rooms", "room_id", str(self.id))[0][0])

    @room.setter
    def room(self, value):
        update(self.table, {"rooms" : pickle.dumps(value)}, "room_id", str(self.id))

    def get_room_id_by_creator(self):
        id = int(select("rooms", "room_id", "creator_id", str(self.id))[0][0])
        return id

    def is_room(self) -> bool:
        """Проверка являтся ли канал комнатой. Требует айди комнаты"""
        info = select("rooms", "rooms", "room_id", str(self.id))
        return info != []
    
    def is_creator(self):
        info = select("rooms", "room_id", "creator_id", str(self.id))
        return info != []

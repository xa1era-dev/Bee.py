import json
import discord
from database import *
from .queue import Queue
from .settings import Settings
import pickle

class MusicBotData(object):
    def __init__(self, guild : discord.Guild):
        self.id = str(guild.id)
        self.table = "musicbot"
        self.where = "guild_id"

    def enable_module(self,
                      now_msg_id : int,
                      queue_msg_id : int,
                      guide_msg_id : int,
                      channel_id : int,
                      log_channel : int):
        update("guilds_modules", {"musicbot" : True}, "guild_id", self.id)
        insert(self.table, [self.id,
                            pickle.dumps(Settings()),
                            pickle.dumps(Queue()),
                            str(now_msg_id),
                            str(queue_msg_id),
                            str(guide_msg_id), 
                            str(channel_id),
                            str(log_channel)])

    def disable_module(self):
        update("guilds_modules", {"musicbot" : False}, "guild_id", self.id)
        delete(self.table, self.where, self.id)

    def is_enabled_module(self):
        return bool(select("guilds_modules", "musicbot", "guild_id", self.id)[0][0])

    @property
    def channel_id(self) -> int:
        return int(select(self.table, "channel", self.where, self.id)[0][0])
    
    @channel_id.setter
    def channel_id(self, new_id : int):
        update(self.table, {"channel" : new_id}, self.where, self.id)



    @property
    def now_msg_id(self) -> int:
        return int(select(self.table, "now_msg_id", self.where, self.id)[0][0])
    
    @now_msg_id.setter
    def now_msg_id(self, new_id : int):
        update(self.table, {"now_msg_id" : new_id}, self.where, self.id)
    


    @property
    def queue_msg_id(self) -> int:
        return int(select(self.table, "queue_msg_id", self.where, self.id)[0][0])
    
    @queue_msg_id.setter
    def queue_msg_id(self, new_id : int):
        update(self.table, {"queue_msg_id" : new_id}, self.where, self.id)



    @property
    def guide_msg_id(self) -> int:
        return int(select(self.table, "guide_msg_id", self.where, self.id)[0][0])

    @guide_msg_id.setter
    def guide_msg_id(self, new_id : int):
        update(self.table, {"guide_msg_id" : new_id}, self.where, self.id)



    @property
    def log_channel_id(self) -> int:
        return int(select(self.table, "log_channel", self.where, self.id)[0][0])
    
    @log_channel_id.setter
    def log_channel_id(self, new_id : int):
        update(self.table, {"log_channel" : new_id}, self.where, self.id)



    @property
    def settings(self) -> Settings:
        return pickle.loads(bytes(select(self.table, "settings", self.where, self.id)[0][0]))
    
    @settings.setter
    def settings(self, new_settings : Settings):
        update(self.table, {"settings" : pickle.dumps(new_settings)}, self.where, self.id)



    @property
    def queue(self) -> Queue:
        try:
            return pickle.loads(bytes(select(self.table, "queue", self.where, self.id)[0][0]))
        except IndexError:
            return Queue() # type: ignore

    @queue.setter
    def queue(self, queue : Queue):
        update(self.table, {"queue" : pickle.dumps(queue)}, self.where, self.id)



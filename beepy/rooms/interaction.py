import discord
from modules import Colors
from musicbot import MusicBotData
from client import Bot as bot
import asyncio

class RoomLockButton(discord.ui.Button):
    def __init__(self, is_mafia : bool = False, is_locked : bool = False) -> None:
        super().__init__(disabled = is_mafia, custom_id="lock")
        self.style = discord.ButtonStyle.green
        self.label='🔓'
        if is_locked:
            self.style = discord.ButtonStyle.red
            self.label='🔒'

class RoomMusicBotButton(discord.ui.Button):
    def __init__(self, is_mafia : bool = False, mus_bot_for_all : bool = True):
        super().__init__(label='🎵', disabled=is_mafia, custom_id='musbot_change_access')
        self.style = discord.ButtonStyle.red
        if mus_bot_for_all:
            self.style = discord.ButtonStyle.green

class RoomBanButton(discord.ui.Button):
    def __init__(self, is_disabled : bool):
        super().__init__(style = discord.ButtonStyle.secondary,
            label = 'Кого забанить',
            custom_id = 'banroom',
            disabled = is_disabled)

class RoomEditButton(discord.ui.Button):
    def __init__(self, is_mafia : bool):
        super().__init__(style=discord.ButtonStyle.blurple,
            label = '✏️',
            custom_id = 'editroomname',
            disabled = is_mafia)

"""class RoomsStartGame(discord.ui.Button):
    def __init__(self, cnt : int, is_mafia : bool):
        super().__init__(style=discord.ButtonStyle.blurple,
            label = '🕵️‍♂️',
            custom_id='start_game',
            disabled = is_mafia)
        #if cnt < 5:
        #    self.disabled = True"""

class RoomsControl(discord.ui.View):
    def __init__(self, room, guild : discord.Guild):
        super().__init__(timeout = None)
        self.room = room
        #self.is_mafia = Modules(self.id).rooms.is_mafia
        self.is_mafia = False
        self.add_item(RoomLockButton(self.is_mafia, self.room.settings.is_locked))
        if MusicBotData(guild).is_enabled_module:
            self.add_item(RoomMusicBotButton(self.is_mafia, self.room.settings.musicbot_for_all))
        self.add_item(RoomBanButton(self.is_mafia))
        self.add_item(RoomEditButton(self.is_mafia))

import discord
import discord.utils
from .queue import Queue
from .settings import Settings
from .messages import Messages
from .music_bot_db import MusicBotData
from .utils import ReapetVaritions, FFMPEG_OPTIONS, YDL_OPTS, VideoNotFound, NotInVoiceChannel
import yt_dlp

def get_voice(guild : discord.Guild, bot : discord.Bot) -> discord.VoiceClient | None:
    return discord.utils.get(bot.voice_clients, guild=guild) # type: ignore

def get_queue(guild : discord.Guild) -> Queue:
    return MusicBotData(guild).queue

def get_settings(guild : discord.Guild) -> Settings:
    return MusicBotData(guild).settings

async def next_song(guild : discord.Guild, bot : discord.Bot):
    if get_voice(guild, bot) is not None and not get_voice(guild, bot).is_playing(): # type: ignore
        queue : Queue = get_queue(guild)
        settings : Settings = get_settings(guild)
        if settings.repeat == ReapetVaritions.Queue:
            queue.go_in_back()

        elif settings.repeat == ReapetVaritions.Not:
            queue.move_to_history()

        MusicBotData(guild).queue = queue

        if len(queue) == 0:
            await stop_session(guild, bot)
            return

        await play_song(guild, bot)
        await Messages(guild).edit_queue()

async def play_song(guild : discord.Guild, bot : discord.Bot):
    vc1=guild.voice_client
    vc = get_voice(guild, bot)
    print(vc1.is_connected(), vc.is_connected())
    queue : Queue = get_queue(guild)
    if not vc:
        raise NotInVoiceChannel()
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        infourl = ydl.extract_info(queue.next_song.url, download = False)
        if infourl == None:
            raise VideoNotFound()
        URL = infourl['url']
        guild.voice_client.play(discord.FFmpegPCMAudio(URL, before_options = FFMPEG_OPTIONS),
            after = lambda e : bot.loop.create_task(next_song(guild, bot)))
    await Messages(guild).edit_now()

async def pause(guild : discord.Guild, bot : discord.Bot):
    vc = get_voice(guild, bot)
    if vc is None:
        raise NotInVoiceChannel()
    if vc.is_playing():
        vc.pause()
    else:
        vc.resume()
    await Messages(guild).edit_now()

async def stop_session(guild : discord.Guild, bot : discord.Bot):
    vc = get_voice(guild, bot)
    vc.stop()
    queue = get_queue(guild)
    queue.clear_queue()
    MusicBotData(guild).queue = queue
    settings = get_settings(guild)
    settings.repeat = ReapetVaritions.Not
    MusicBotData(guild).settings = settings
    bot.loop.create_task(vc.disconnect()) # type: ignore
    #bot.loop.create_task(change_acsecc())
    bot.loop.create_task(Messages(guild).edit_now())
    bot.loop.create_task(Messages(guild).edit_queue())

"""async def change_acsecc(self):
    create_room_id = Rooms(self.guild.id).info['channles'][0]
    create_room = self.guild.get_channel(create_room_id)
    category = create_room.category.channels.remove(create_room)
    for room in category:
        chan_sets = Rooms(room.id).settings
        for mem in room.members:
            if chan_sets["MusBotToAll"]:
                await self.channel.set_permissions(target = mem, view_channel = True, send_messages = True)
            else:
                await self.channel.set_permissions(target = mem, view_channel = False, send_messages = False)"""

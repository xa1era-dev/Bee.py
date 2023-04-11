import discord
from modules import Colors
import datetime
from .music_bot_db import MusicBotData
from .queue import Queue
from .voice import play_song, stop_session, get_voice
from .messages import Messages, MusicHistory
from .song import Song
from .utils import Source, SongInQueueException


async def clearq(guild : discord.Guild, bot : discord.Bot):
    MusicBotData(guild).queue = Queue()
    await stop_session(guild, bot)
    
async def add_to_queue(guild : discord.Guild, song : Song, member : discord.Member, bot : discord.Bot):
    queue = MusicBotData(guild).queue
    if song.url in queue.urls:
        raise SongInQueueException()
    queue.add(song)
    MusicBotData(guild).queue = queue
    is_connected = get_voice(guild, bot)

    if is_connected == None:
        await member.voice.channel.connect()
        await play_song(guild, bot)

    await Messages(guild).edit_queue()
    mus_channel = guild.get_channel(MusicBotData(guild).channel_id)
    mus_log_id = MusicBotData(guild).log_channel_id
    mus_log = mus_channel.get_thread(mus_log_id)

    if mus_log == None:
        def predicate(thread : discord.Thread):
            return thread.id == MusicBotData(guild).log_channel_id
        raw_auditmus = await mus_channel.archived_threads().find(predicate)
        mus_log = await raw_auditmus.unarchive()

    embed = discord.Embed(color = Colors.YELLOW.value)
    embed.timestamp = discord.utils.utcnow()
    embed.set_author(name = f'Музыка добавлена в очередь ({song.source.value})', icon_url='')

    if song.is_stream:
        embed.add_field(name = 'Название стрима:',value = f'[{str(song)}]({song.url})')

    else:
        embed.add_field(name = 'Название трека:',value = f'[{str(song)}]({song.url})')
        embed.add_field(name = 'Длительность трека:', value = str(datetime.timedelta(seconds=song.duration)), inline=False)

    embed.add_field(name = 'Кто поставил:', value = f'{member.mention} | `{member.name}#{member.discriminator}`', inline=False)
    await mus_log.send(embed = embed, view=MusicHistory(song))

async def enable_module(guild : discord.Guild):
    from rooms import RoomsData
    info = RoomsData(guild).channels
    cat = guild.get_channel(info.channel_id).category
    music_text_channel = await cat.create_text_channel(
        name='Music🎵',
        overwrites={guild.default_role:discord.PermissionOverwrite(
            read_messages = True,
            read_message_history = True,
            send_messages = False,),},)
    """auditlog = guild.get_channel(Modules(guild.id).auditlog.chan)
    if not auditlog:
        auditlog=await guild.create_text_channel(
            name='журнал-аудита',
            overwrites={
                guild.default_role:discord.PermissionOverwrite(
                    view_channel=False,
                    read_messages=False,
                    send_messages=False,)},)
        Modules(guild.id).auditlog.chan=auditlog.id
    muslog=await auditlog.create_thread(
        name='журнал-музыки',
        type=discord.ChannelType.public_thread,)
    admins=[]
    for role in list(reversed(guild.roles)):
        if role.permissions.administrator==True:
            admins.append(role.mention)
        else:
            pass
    await muslog.send(content=', '.join(admins))"""
    guide_emb=discord.Embed(color=Colors.GRAY.value)
    guide_emb.set_footer(text='guide_msg')
    queue_emb=discord.Embed(color=Colors.GRAY.value)
    queue_emb.set_footer(text='queue_msg')
    now_emb=discord.Embed(
        color=Colors.GRAY.value,
        title='Для старта бота, создайте комнату и введите любую песню в данный канал',)
    now_emb.set_footer(text='now_msg')
    guide_msg=await music_text_channel.send(embed=guide_emb)
    queue_msg=await music_text_channel.send(embed=queue_emb)
    now_msg=await music_text_channel.send(embed=now_emb)
    await music_text_channel.set_permissions(target=guild.default_role,view_channel=False)
    log = await music_text_channel.create_thread(name="История музыки", type=discord.ChannelType.public_thread)
    if music_text_channel.last_message.is_system():
        await music_text_channel.last_message.delete()
    MusicBotData(guild).enable_module(now_msg.id, queue_msg.id, guide_msg.id, music_text_channel.id, log.id) 

async def disable_module(guild : discord.Guild):
    channel = guild.get_channel(MusicBotData(guild).channel_id)
    await channel.delete()
    MusicBotData(guild).disable_module()

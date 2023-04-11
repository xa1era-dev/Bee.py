import discord
from modules import Colors
from musicbot import MusicBotData
from .objects import RoomsData, RoomData
import asyncio
from .interaction import RoomsControl

async def create_room(create_channel : CreateableRoom, mem : discord.Member, bot : discord.Bot):
    mem_name = mem.name if mem.nick is None else mem.nick
    room_data = RoomData(mem)
    if room_data.is_creator():
        try:
            await mem.move_to(None)# type: ignore   
        except:
            pass
        user = await bot.fetch_user(mem.id)# type: ignore
        embed = discord.Embed(color = Colors.GRAY.value, title = 'У вас уже имеется комната')
        await user.send(embed = embed)
    else:
        name = create_channel.settings.name.replace("{member}", mem_name)
        cre_channel = bot.get_channel(create_channel.channel_id)
        newroom = await cre_channel.clone(name = name)#type: ignore
        try:
            await mem.move_to(newroom)#type: ignore
        except:
            pass
        if MusicBotData(mem.guild).is_enabled_module:
            music = mem.guild.get_channel(MusicBotData(mem.guild).channel_id)
            if not mem.guild.voice_client:
                await music.set_permissions(target=mem, view_channel = True, send_messages = True)# type: ignore
        console = await create_console(newroom, mem)#type: ignore
        room = Room(name, newroom, create_channel, console[1], mem, console[0])#type: ignore
        RoomData(newroom).add_room(room, mem)#type: ignore
        await edit_console(room, bot)
        await asyncio.sleep(3)
        if newroom.members == []:#type: ignore
            await delete_room(room, bot)

async def create_console(new_room : discord.VoiceChannel, mem : discord.Member):
    mem_name = mem.name if mem.nick is None else mem.nick
    overwrites = {
        mem.guild.default_role:discord.PermissionOverwrite(view_channel = False, 
            send_messages = False, add_reactions = False),
        mem : discord.PermissionOverwrite(view_channel = True, send_messages = True,
            read_message_history = True)
    }
    console = await new_room.category.create_text_channel(name = f"Консоль {mem_name}", #type: ignore
        overwrites = overwrites)
    """chan_log_id = None
    if Modules(af.guild.id).auditlog.chan:
        chan_log = await textroom.create_thread(name = 'журнал-комнаты', type = discord.ChannelType.public_thread)
        chan_log_id = chan_log.id
        embed = discord.Embed(color = Colors.Yellow.value, title = 'Вы создали комнату')
        await chan_log.send(embed = embed)"""
    await console.set_permissions(target = mem, manage_channels = True)
    console_emb = discord.Embed(color = Colors.GRAY.value, title = 'Консоль комнаты')
    console_msg = await console.send(embed = console_emb)
    return console, console_msg

async def edit_console(room : Room, bot : discord.Bot):
    consoleemb = discord.Embed(color = Colors.GRAY.value, title='Консоль комнаты')
    console = bot.get_channel(room.console_id)#type: ignore
    console_msg = await console.fetch_message(room.console_msg_id)#type: ignore
    voice_channel = bot.get_channel(room.channel_id)#type: ignore
    options = []
    if not room.settings.is_locked:
        options.append(str('`🟢` | `🔓` -  комната `разблокирована`'))
        await voice_channel.set_permissions(target = voice_channel.guild.default_role, overwrite = None)#type: ignore
    else:
        options.append(str('`🔴` | `🔒` -  комната `заблокирована`'))
        await voice_channel.set_permissions(target =voice_channel.guild.default_role, connect = False)#type: ignore
    if MusicBotData(voice_channel.guild).is_enabled_module:#type: ignore
        if room.settings.musicbot_for_all:
            options.append('`🟢` | `🎵` - музыкальным ботом могут управлять `все члены комнаты`')
        else:
            options.append('`🔴` |  `🎵` - музыкальным ботом могут управлять `только создатель комнаты`')
    options.append('`✏️` -  изменить название комнаты')
    #options.append('`🕵️‍♂️` - начать мафию (Work In Progress)')
    consoleemb.add_field(name = "Параметры:", value = '\n'.join(options), inline=False)
    if room.bans:
        consoleemb.add_field(name = "Забаненные пользователи:",
            value = ', '.join([member.mention for member in room.bans]))
        banemb = discord.Embed(color = Colors.GRAY.value)
        banemb.set_author(name = 'Выберете из выпающего списка, кого вы хотите разбанить')
        if room.bans_msg_id is not None:
            await console.fetch_message(room.bans_msg_id.edit(embed = banemb))#type: ignore
        else:
            room.bans_msg_id = (await room.console_id.send(embed = banemb)).id# type: ignore
    await console_msg.edit(embed = consoleemb, view = RoomsControl(room, voice_channel.guild))# type: ignore


async def delete_room(room : Room, bot : discord.Bot):
    RoomData(bot.get_channel(room.channel_id)).del_room()#type: ignore
    await bot.get_channel(room.channel_id).delete()#type: ignore
    await bot.get_channel(room.console_id).delete()#type: ignore

async def change_access_musbot(room : Room, bot : discord.Bot):
    settings = room.settings
    voice_channel = bot.get_channel(room.channel_id)
    muschan = voice_channel.guild.get_channel(MusicBotData(room.guild).channel_id)

    if settings.musicbot_for_all:
        for mem in voice_channel.members:
            if mem.id != bot.user.id and mem.id != room.creator_id:
                muschan.set_permissions(mem, overwrite=None)
    else:
        musbot_prems = discord.PermissionOverwrite(
        view_channel=True,
        send_messages=True,
        read_message_history=True,)
        
        for mem in voice_channel.members:
            if mem.id != bot.user.id and mem.id != room.creator_id:
                muschan.set_permissions(mem, overwrite=musbot_prems)
    
    room.settings.musicbot_for_all = not (room.settings.musicbot_for_all)
    RoomData(room).room = room
    await edit_console(room, bot)

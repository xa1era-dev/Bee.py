# -*- coding: utf-8 -*-
import discord
from discord.commands import SlashCommandGroup
import discord.utils
from rooms import Room, CreateableRoom, Settings, delete_room, create_room, edit_console, change_access_musbot
from musicbot import (MusicBotData,
                      define_source, 
                      NotFoundSongException, 
                      pause, 
                      get_settings,
                      Messages,
                      get_queue,
                      stop_session,
                      SongInQueueException,
                      MaxLenghtException,
                      ReapetVaritions)
import musicbot
import asyncio
from modules import Colors
from rooms import RoomsData, RoomData


#https://discord.com/api/oauth2/authorize?client_id=713831247285190726&permissions=8&scope=bot%20applications.commands


async def voice_state_update(
        mem : discord.Member,
        bot : discord.Bot,
        be : discord.VoiceChannel | None = None,
        af : discord.VoiceChannel | None = None
    ):

    perms_after_connect_room = discord.PermissionOverwrite(
        view_channel = True,
        send_messages = True,
        read_message_history = True)
    

    if af is not None and af.id == RoomsData(mem.guild).channels.channel_id: #create room
        await create_room(RoomsData(mem.guild).channels, mem, bot)

    if be and RoomData(be).is_room() and (len(be.members) == 0 or (be.members[0].id == bot.user.id)): #type: ignore #delete room
        await delete_room(RoomData(be).room, bot)

    if af and RoomData(af).is_room(): #connect to room
        if mem.id != bot.user.id and not RoomData(mem).is_creator(): #type: ignore
            await bot.get_channel(RoomData(af).room.__console_id).set_permissions(target = mem, overwrite = perms_after_connect_room)
            if MusicBotData(mem.guild).is_enabled_module() and RoomData(af).is_room() and RoomData(af).room.settings["MusBotToAll"]:
               await mem.guild.get_channel(MusicBot(mem.guild.id).info['channel']).set_permissions(target = mem, overwrite = perms_after_connect_room)

    if be and RoomData(be).is_room(): #disconnect from room
        #if MusicBot(mem.guild.id).info != {}:
        #    await mem.guild.get_channel(MusicBot(mem.guild.id).info['channel']).set_permissions(target = mem, overwrite = None)
        #if len(be.members) == 1 and be.members[0].id == bot.user.id:
        #    await MusicBotProcesses(mem.guild).clearq()
        #    await RoomProcesses(mem.guild, be.id).deleteroom(mem,be)
        if mem.id != bot.user.id and not RoomData(mem).is_creator(): #type: ignore
            if RoomData(be).room.settings.is_locked == False:
                await bot.get_channel(RoomData(be).room.__console_id).set_permissions(target = mem, overwrite = None)#type: ignore

async def message(msg : discord.Message, bot : discord.Bot):
    if msg.author.id != bot.user.id:
        await define_source(msg, bot)

        """except NotFoundSongException as err:
            print(err)

        except SongInQueueException:
            err_emb = discord.Embed(color=Colors.RED.value, title="Песня уже в очереди")
            err_emb.set_footer(text="Автоматическое удаление через 5 секунд")
            await msg.reply(embed=err_emb, delete_after=5.0)
            await asyncio.sleep(5.0)

        except MaxLenghtException:
            err_emb = discord.Embed(color=Colors.RED.value, title="Очередь достигла максимума")
            err_emb.set_footer(text="Автоматическое удаление через 5 секунд")
            await msg.reply(embed=err_emb, delete_after=5.0)
            await asyncio.sleep(5.0)"""

        await msg.delete()

async def rooms_slash(ctx : discord.ApplicationContext,
    option : discord.Option(str, choices=['enable','disable']), 
    bot : discord.Bot):# type: ignore
    loadembed = discord.Embed(
        color = Colors.GRAY.value,
        title = 'Обработка данных')
    msg = await ctx.response.send_message(embed = loadembed, ephemeral = True)
    is_enabled_rooms=RoomsData(ctx.guild).is_enabled_module()#type: ignore
    redembed=discord.Embed(color=Colors.RED.value)
    greenembed=discord.Embed(color=Colors.GREEN.value)
    if option in ['enable','disable']:
        if ctx.author.guild_permissions.administrator:#type: ignore
            if is_enabled_rooms:
                if option=='enable':
                    redembed.set_author(name='Ошибка')
                    redembed.add_field(
                        name='Причина ошибки:',
                        value='Модуль `комнаты` уже включен')
                elif option=='disable':
                    crechan=RoomsData(ctx.guild).channels.channel_id#type: ignore
                    await (bot.get_channel(crechan)).delete()
                    RoomsData(ctx.guild).disable_module()#type: ignore
                    greenembed.set_author(
                        name='Модуль отключен')
                    greenembed.add_field(
                        name='Отключенный модуль:',
                        value='Комнаты',
                        inline=False)
                    greenembed.add_field(
                        name='Допольнительная информация:',
                        value='Созданные комнаты будут рабоать в обычном режиме',
                        inline=False)
            else:
                if option=='enable':
                    categ=await ctx.guild.create_category('Комнаты')#type: ignore
                    cre=await categ.create_voice_channel('Создать комнату')
                    creatable_room=CreateableRoom(cre)
                    greenembed.set_author(
                        name='Модуль включен')
                    greenembed.add_field(
                        name='Подключенный модуль:',
                        value='Комнаты',
                        inline=False)
                    greenembed.add_field(
                        name='Канал для создания комант:',
                        value=cre.mention,
                        inline=False)
                    RoomsData(ctx.guild).enable_module(creatable_room)#type: ignore
                if option=='disable':
                    redembed.set_author(name='Ошибка')
                    redembed.add_field(name='Причина ошибки:',value='Модуль комнаты отключен')
    redembed.timestamp=discord.utils.utcnow()
    greenembed.timestamp=discord.utils.utcnow()
    if redembed.author:
        await msg.edit_original_response(embed=redembed)#type: ignore
    if greenembed.author:
        await msg.edit_original_response(embed=greenembed)#type: ignore



async def musicbot_slash(ctx : discord.ApplicationContext,
                         state : discord.Option(
                            str,'Состояние музыкального бота',
                            choices=['enable', 'disable', 'info']),
                         bot : discord.Bot):    
    loadembed=discord.Embed(color=Colors.GRAY.value, title='Обработка данных')
    msg=await ctx.response.send_message(embed=loadembed,ephemeral=True)
    redembed=discord.Embed(color=Colors.RED.value)
    greenembed=discord.Embed(color=Colors.GREEN.value)

    if state=='enable' or state=='disable':
        if ctx.author.guild_permissions.administrator==True:
            if state=='enable':
                if RoomsData(ctx.guild).is_enabled_module() and not MusicBotData(ctx.guild).is_enabled_module():
                    await musicbot.enable_module(ctx.guild)
                    greenembed.set_author(name='Модуль включен')
                    greenembed.add_field(
                        name='Подключенный модуль:',
                        value='`Музыкальный бот`')
                    
                elif not RoomsData(ctx.guild).is_enabled_module() and not MusicBotData(ctx.guild).is_enabled_module():
                    redembed.set_author(name='Ошибка')
                    redembed.add_field(
                        name='Причина ошибки:',
                        value='Модуль `комнаты` не включен')
                    
                elif RoomsData(ctx.guild).is_enabled_module() and MusicBotData(ctx.guild).is_enabled_module():
                    redembed.set_author(name='Ошибка')
                    redembed.add_field(
                        name='Причина ошибки:',
                        value='Модуль `музыкальный бот` уже включен')
                    


            elif state=='disable':
                if not MusicBotData(ctx.guild).is_enabled_module():
                    redembed.set_author(name='Ошибка')
                    redembed.add_field(
                        name='Причина ошибки:',
                        value='Модуль `музыкальный бот` уже выключен')
                else:
                    if not ctx.guild.voice_client:
                        await musicbot.disable_module(ctx.guild)
                        greenembed.set_author(name='Модуль выключен')
                        greenembed.add_field(
                            name='Отключенный модуль:',
                            value='`Музыкальный бот`')
                    else:
                        redembed.set_author(name='Ошибка')
                        redembed.add_field(
                            name='Причина ошибки:',
                            value='Бот занят')

        else:
            redembed.set_author(name='Ошибка')
            redembed.add_field(name='Причина ошибки:',value='У вас нет прав администратора')

    """if state=='info':
        if Modules(ctx.guild.id).musicbot.info:
            musinfo=Modules(ctx.guild.id).musicbot.get_info
            muschan=ctx.guild.get_channel(musinfo['channel'])
            greenembed.set_author(name='Успех')
            greenembed.add_field(name='Канал:',value=f'{muschan.name} | {muschan.mention}')
            greenembed.add_field(name='Активировано:',value=f'{discord.utils.format_dt(muschan.created_at)}',inline=False)
        else:
            redembed.set_author(name='Ошибка')
            redembed.add_field(name='Причина ошибки:',value='Модуль музыкальный бот не активирован')"""
    redembed.timestamp=discord.utils.utcnow()
    greenembed.timestamp=discord.utils.utcnow()
    if redembed.author:
        await msg.edit_original_response(embed=redembed)
    else:
        await msg.edit_original_response(embed=greenembed)

async def post_inter(inter : discord.Interaction, bot : discord.Bot):
    await bot.process_application_commands(interaction = inter)
    if inter.custom_id not in ['editroomname', 'editnickname', "back_to_queue", "clear_queue"] and inter.type != discord.InteractionType.application_command:
        await inter.response.defer()
    room = None
    if RoomData(inter.user).is_creator():
        room = inter.guild.get_channel(RoomData(inter.user).get_room_id_by_creator())
    
    match inter.custom_id:

        case 'lock':
            if room is not None:
                room_obj = RoomData(room).room
                room_obj.settings.is_locked = not room_obj.settings.is_locked
                RoomData(room).room = room_obj
                await edit_console(room_obj, bot)
        
        case 'musbot_change_access':
            if room is not None:
                await change_access_musbot(RoomData(room).room. bot)
        
        case  "prev_song":
            vc = discord.utils.get(bot.voice_clients, guild=inter.guild)
            queue = get_queue(inter.guild)
            queue.move_to_queue()
            MusicBotData(inter.guild).queue = queue
            vc.stop()
        
        case  'pause':
            await pause(inter.guild, bot)

        case  'next_song':
            vc = discord.utils.get(bot.voice_clients, guild=inter.guild)
            vc.stop()
    
        case  "clear_queue":
            await stop_session(inter.guild, bot)
        
        case  'repeat':
            queue = get_queue(inter.guild)
            settings = get_settings(inter.guild)
            settings.change_repeat(queue)
            MusicBotData(inter.guild).settings = settings
            await Messages(inter.guild).edit_now()
        
    """if inter.custom_id == 'volumeup':
        volume = Modules(inter.guild.id).musicbot.get_info['volume']
        if volume < 100:
            for server in queues:
                if server["guildid"]==[inter.guild_id]:
                    volume += 10
                    server['settings'][0]=1
                    Modules(inter.guild_id).musicbot.volume=volume
                    await editnow(inter.guild_id)
    if inter.custom_id == 'volumedown':
        volume = Modules(inter.guild.id).musicbot.get_info['volume']
        if volume > 0:
            for server in queues:
                if server["guildid"] == [inter.guild_id]:
                    volume -= 10
                    server['settings'][0] = 1
                    Modules(inter.guild_id).musicbot.volume = volume
                    await editnow(inter.guild_id)"""
    """
    if inter.custom_id == 'start_game':
        if roomid is not None:
            await mafia.StartGame().create_lobby(inter.guild, roomid)
            await editconsole(inter.user)"""

    """if inter.custom_id == 'banroom':
            if room is not None:
                bans = Rooms(room).room_bans
                banemb = discord.Embed(color = Colors.GRAY.value)
                banemb.set_author(name = 'Введите @человек, чтобы забанить его в вашей комнате `(макс. 10 человек)`')
                banemb.add_field(name = 'Нельзя забанить:', value = '*Себя и бота\n*Администраторов\n*Людей не в вашей комнате')
                banemb.set_footer(text = 'Обнаружение @человек дейтсвует 20 секунд')
                await inter.followup.send(embed = banemb, ephemeral = True)
                def check(message):
                    return message.raw_mentions != []
                try:
                    event = await bot.wait_for('message', check = check, timeout = 20.0)
                except asyncio.TimeoutError:
                    pass
                else:
                    target = inter.guild.get_member(event.raw_mentions[0])
                    room = inter.guild.get_channel(room)
                    if (target.id != inter.user.id) and target.id != bot.user.id and target.guild_permissions.administrator != True and target.voice.channel and target.voice.channel == room and len(bans) <= 10:
                        bans.append(event.raw_mentions[0])
                        Rooms(room).room_bans=bans
                        await room.set_permissions(target = target, connect = False)
                        await target.move_to(None)
                        await RoomProcesses(inter.guild, room).editconsole()
                    await event.delete()
        if inter.custom_id == 'editroomname':
            if room is not None:
                modal = discord.ui.Modal(title = 'Изменить название комнаты')
                modal.add_item(discord.ui.InputText(
                    label = 'Введите новое название комнаты',
                    placeholder = 'Назване комнаты',required=True))
                async def recive_modal(interaction : discord.Interaction):
                    await interaction.response.defer(ephemeral = True)
                    room = interaction.guild.get_channel(room)
                    await room.edit(name = modal.children[0].value)
                    embed = discord.Embed(color = Colors.YELLOW.value)
                    embed.set_author(name = 'Успех')
                    embed.add_field(name = 'Новое название:', value = modal.children[0].value)
                    await interaction.followup.send(embed = embed, ephemeral = True)
                modal.callback = recive_modal
                await inter.response.send_modal(modal)"""
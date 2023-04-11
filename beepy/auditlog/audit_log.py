import discord
import datetime
from modules import *
from client import Bot as bot


class AuditLogging(object):
    def __init__(self, guild : discord.Guild):
        self.guild = guild
        self.channel = self.guild.get_channel(AuditLog(self.guild.id).chan)

    async def change_mute_deaf(self, mem : discord.Member, be : discord.VoiceState, af : discord.VoiceState):
        embed = None
        if mem.guild.owner == mem:
            selftarget, target = 'Создатель сервера', 'Создателю сервера'
        elif mem.guild_permissions.administrator:
            selftarget, target = 'Администратор', 'Администратору'
        else:
            selftarget, target='Пользователь', 'Пользователю'
        if Rooms(be.channel.id).is_room:
            chan_type , chan_type2 = 'комнате', "Комната"
        else:
            chan_type, chan_type2 = 'голосовом канале',"Голосовой канал"
        if be.self_mute != af.self_mute:
            if be.self_mute:
                embed = discord.Embed(color = Colors.YELLOW.value)
                embed.set_author(name=f'{selftarget} включил микрофон в {chan_type}',icon_url='https://i.ibb.co/Bq5ckTC/picked-up-mute.png')
            else:
                embed = discord.Embed(color = Colors.RED.value)
                embed.set_author(name=f'{selftarget} отключил микрофон в {chan_type}',icon_url='https://i.ibb.co/KFGkScK/give-mute.png')
        if be.mute != af.mute:
            if be.mute:
                embed = discord.Embed(color=Colors.YELLOW.value)
                embed.set_author(name=f'{target} включили микрофон в {chan_type}',icon_url='https://i.ibb.co/Bq5ckTC/picked-up-mute.png')
            else:
                embed = discord.Embed(color=Colors.RED.value)
                embed.set_author(name=f'{target} отключили микрофон в {chan_type}',icon_url='https://i.ibb.co/KFGkScK/give-mute.png')
        if be.self_deaf!=af.self_deaf:
            if be.self_deaf:
                embed = discord.Embed(color=Colors.YELLOW.value)
                embed.set_author(name=f'{selftarget} включил звук в {chan_type}',icon_url='https://i.ibb.co/7CFkmZs/undeaf.png')
            else:
                embed = discord.Embed(color=Colors.RED.value)
                embed.set_author(name=f'{selftarget} отключил звук в {chan_type}',icon_url='https://i.ibb.co/NrV4RNp/deaf.png')
        if be.deaf != af.deaf:
            if be.deaf:
                embed = discord.Embed(color=Colors.YELLOW.value)
                embed.set_author(name=f'{target} включили звук в {chan_type}',icon_url='https://i.ibb.co/7CFkmZs/undeaf.png')
            else:
                embed=discord.Embed(color=Colors.RED.value)
                embed.set_author(name=f'{target} отключили звук в {chan_type}',icon_url='https://i.ibb.co/NrV4RNp/deaf.png')
        if embed is not None:
            embed.add_field(name = f'{selftarget}:', value = f'{mem.mention} | `{mem.name}#{mem.discriminator}`', inline=False)
            embed.add_field(name = f'{chan_type2}:', value = f'{be.channel.name} | {be.channel.mention}', inline=False)
            if mem.avatar:
                embed.set_thumbnail(url = mem.avatar.url)
            if Rooms(af.channel.id).is_room:
                creator = af.channel.guild.get_member(Rooms(af.channel).creator)
                embed.add_field(name = 'Создатель комнаты:', value = f'{creator.mention} | `{creator.name}#{creator.discriminator}`', inline=False)
            if be.deaf != af.deaf or be.mute != af.mute:
                auditlist = list(await mem.guild.audit_logs(limit = 1,
                    action = discord.AuditLogAction.member_update).flatten())
                if auditlist != []:
                    audits = auditlist[0]
                    if audits.target == mem:
                        embed.add_field(name = 'Модератор:',
                            value = f'{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`',inline=False)
                        if audits.user.avatar:
                            embed.set_thumbnail(url=audits.user.avatar.url)
            embed.timestamp=discord.utils.utcnow()
            await self.channel.send(embed=embed)

    async def audit_createroom(self, mem : discord.Member, be : discord.VoiceChannel):
        embed = discord.Embed(color = Colors.GREEN.value)
        if be:
            if Rooms(be.id).is_room:
                fromchan, chan_type='из-под комнаты', 'Комната'
            else:
                fromchan, chan_type='из-под голосового канала', 'Голосовой канал'
        else:
            fromchan = ''
        if mem.guild.owner == mem:
            target='Создатель сервера'
        elif mem.guild_permissions.administrator:
            target = 'Администратор'
        else:
            target = 'Пользователь'
        embed.set_author(name=f'{target} создал комнату {fromchan}',icon_url='https://i.ibb.co/J3Tc4Ky/room-create.png')
        embed.add_field(name=f'{target}:',value=f'{mem.mention} | `{mem.name}#{mem.discriminator}`',inline=False)
        if mem.avatar:
            embed.set_thumbnail(url=mem.avatar.url)
        if be:
            auditlist = list(await mem.guild.audit_logs(action = discord.AuditLogAction.member_move, limit=1).flatten())
            if auditlist:
                audits = auditlist[0]
            embed.add_field(name = f'{chan_type}:', value = f'{be.name} | {be.mention}', inline=False)
            if audits:
                embed.add_field(name = 'Модератор:', value = f'{audits.user.mention} | {audits.user.name}#{audits.user.discriminator}', inline=False)
                if audits.user.avatar:
                    embed.set_thumbnail(url=audits.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await self.channel.send(embed=embed)

    async def otherroom(self, mem : discord.Member, be : discord.VoiceChannel, af : discord.VoiceChannel):
        embed = discord.Embed(color = Colors.YELLOW.value)
        if mem.guild.owner == mem:
            target = 'Создатель сервера'
        elif mem.guild_permissions.administrator:
            target = 'Администратор'
        else:
            target = 'Пользователь'
        embed.set_author(name = f'{target} был перемещен в другую комнату', icon_url='https://i.ibb.co/QYFwz8g/connecting-between-rooms.png')
        embed.add_field(name = f'{target}:', value=f'{mem.mention} | `{mem.name}#{mem.discriminator}`', inline=False)
        if mem.avatar:
            embed.set_thumbnail(url = mem.avatar.url)
        embed.add_field(name = 'Изменение комнаты:', value = f'`🟥` {be.name} ➞ `🟩` {af.name}', inline=False)
        embed.add_field(name = 'Создатели комнат:',
            value = f'`🟥` {mem.guild.get_member(Rooms(be.id).creator).mention} | `🟩` {mem.guild.get_member(Rooms(af.id).creator).mention}',
            inline=False)
        auditlist = list(await mem.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_move).flatten())
        if auditlist:
            audits = auditlist[0]
            embed.add_field(name = 'Модератор:', value=f'{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`', inline=False)
            if audits.user.avatar:
                embed.set_thumbnail(url=audits.user.avatar.url)
        embed.timestamp=discord.utils.utcnow()
        await self.channel.send(embed=embed)

    async def change_voice(self, mem:discord.Member,be:discord.VoiceChannel,af:discord.VoiceChannel):
        #for member in channel.members: муз бот
        #    if (member.voice and member.voice.channel != guild.voice_client.channel) or not member.voice:
        #        await channel.set_permissions(target = member, overwrite = None)
        embed = discord.Embed(color = Colors.GREEN.value)
        if mem.guild.owner == mem:
            target='Создатель сервера'
        elif mem.guild_permissions.administrator:
            target='Администратор'
        else:
            target='Пользователь'
        if Rooms(af.id).is_room:
            afcreator = self.guild.get_member(Rooms(af.id).creator)
            embed.set_author(name = f'{target} был перемещен из гол. канала в комнату', icon_url = 'https://i.ibb.co/QYFwz8g/connecting-between-rooms.png')
        else:
            embed.set_author(name = f'{target} был перемещен из комнаты в гол. канал', icon_url = 'https://i.ibb.co/QYFwz8g/connecting-between-rooms.png')
            becreator = af.guild.get_member(Rooms(be.id).creator)
        embed.add_field(name = f'{target}:', value = f'{mem.mention} | `{mem.name}#{mem.discriminator}`',inline=False)
        if mem.avatar:
            embed.set_thumbnail(url=mem.avatar.url)
        embed.add_field(name='Изменение гол. статуса:', value=f'{be.name} ➞ {af.name}',inline=False)
        if Rooms(af.id).is_room:
            embed.add_field(name = f'Создатель комнаты {af.name}:', value = f'{afcreator.mention} | `{afcreator.name}#{afcreator.discriminator}`', inline = False)
        else:
            embed.add_field(name = f'Создатель комнаты {be.name}:', value = f'{becreator.mention} | `{becreator.name}#{becreator.discriminator}`', inline = False)
        auditlist = list(await mem.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_move).flatten())
        if auditlist:
            audits = auditlist[0]
            embed.add_field(name = 'Модератор:', value = f'{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`', inline=False)
            if audits.user.avatar:
                embed.set_thumbnail(url = audits.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await self.channel.send(embed = embed)

    async def disconnect_from_voice(self, mem:discord.Member, be:discord.VoiceChannel):
        embed=discord.Embed(color=Colors.RED.value)
        if self.guild.owner == mem:
            target = 'Создатель сервера'
        elif mem.guild_permissions.administrator:
            target = 'Администратор'
        else:
            target = 'Пользователь'
        auditlist = list(await self.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_disconnect).flatten())
        audits = None
        if auditlist != []:
            audits = auditlist[0]
        if Rooms(be.id).is_room:
            chan, chanf = 'комнаты', 'Комната'
            creat = self.guild.get_member(Rooms(be.id).creator)
        else:
            chan, chanf = 'голосового канала', 'Головой канал'
        if mem.avatar:
            embed.set_thumbnail(url = mem.avatar.url)
        embed.set_author(name = f'{target} вышел из {chan}', icon_url = 'https://i.ibb.co/hFR1xpF/disconnect-from-room.png')
        embed.add_field(name = f'{target}:', value = f'{mem.mention} | `{mem.name}#{mem.discriminator}`', inline = False)
        embed.add_field(name = f'{chanf}:', value = f'{be.name} | {be.mention}', inline = False)
        embed.timestamp = discord.utils.utcnow()
        if Rooms(be.id).is_room:
            embed.add_field(name = 'Создатель комнаты:', value = f'{creat.mention} | `{creat.name}#{creat.discriminator}`', inline = False)
            chan_log = self.guild.get_channel_or_thread(Rooms(be.id).room_log)
            if chan_log:
                await chan_log.send(embed = embed)
        if audits is not None:
            if audits.target == mem:
                embed.set_author(name = f'{target} был кикнут из {chan}', icon_url = 'https://i.ibb.co/hFR1xpF/disconnect-from-room.png')
            embed.add_field(name = 'Модератор:', value = f'{audits.user.mention} | {audits.user.name}#{audits.user.discriminator}', inline = False)
            if audits.user.avatar:
                embed.set_thumbnail(url = audits.user.avatar.url)
        await self.channel.send(embed=embed)

    async def connect_to_voice(self, mem:discord.Member, af:discord.VoiceChannel):
        embed = discord.Embed(color = Colors.GREEN.value)
        if self.guild.owner == mem:
            target = 'Создатель сервера'
        elif mem.guild_permissions.administrator:
            target = 'Администратор'
        else:
            target = 'Пользователь'
        if Rooms(af.id).is_room:
            chan, chanf = 'комнате', 'Комната'
            creat = self.guild.get_member(Rooms(af.id).creator)
        else:
            chan, chanf = 'голосовому каналу', 'Головой канал'
        embed.set_author(name = f'{target} присоединился к {chan}', icon_url = 'https://i.ibb.co/XtPGGD3/connect-to-room.png')
        embed.timestamp = discord.utils.utcnow()
        embed.add_field(name = f'{target}:', value = f'{mem.mention} | `{mem.name}#{mem.discriminator}`', inline = False)
        embed.add_field(name = f'{chanf}:', value = f'{af.name} | {af.mention}', inline = False)
        if mem.avatar:
            embed.set_thumbnail(url = mem.avatar.url)
        if Rooms(af.id).is_room:
            embed.add_field(name = 'Создатель комнаты:', value = f'{creat.mention} | `{creat.name}#{creat.discriminator}`', inline = False)
            chan_log =self.guild.get_channel_or_thread(Rooms(af.id).room_log)
            if chan_log:
                await chan_log.send(embed = embed)
        await self.channel.send(embed=embed)

    async def audit_deleteroom(self, mem : discord.Member, be : discord.VoiceChannel):
        embed = discord.Embed(color=Colors.RED.value)
        auditlist = list(await self.guild.audit_logs(limit=1,action=discord.AuditLogAction.member_disconnect).flatten())
        if auditlist != []:
            audits = auditlist[0]
        if mem.guild.owner == mem:
            target = 'Создатель сервера'
        elif mem.guild_permissions.administrator:
            target = 'Администратор'
        else:
            target = 'Пользователь'
        embed.set_author(name = f'Комната была удалена ({target} вышел)', icon_url = 'https://i.ibb.co/y6YjNJM/room-delete.png')
        creator = be.guild.get_member(Rooms(be.id).creator)
        embed.add_field(name = f'{target}:', value = f'{mem.mention} | `{mem.name}#{mem.discriminator}`', inline = False)
        if mem.avatar:
            embed.set_thumbnail(url = mem.avatar.url)
        embed.add_field(name = 'Комната:', value = f'{be.name}', inline = False)
        embed.add_field(name = 'Создатель комнаты:', value = f'{creator.mention} | `{creator.name}#{creator.discriminator}`', inline = False)
        if auditlist != []:
            if audits.target == mem:
                embed.set_author(name = f'Комната была удалена ({target} был кикнут)', icon_url = 'https://i.ibb.co/y6YjNJM/room-delete.png')
            embed.add_field(name = 'Модератор:', value = f'{audits.user.mention} | {audits.user.name}#{audits.user.discriminator}', inline = False)
            if audits.user.avatar:
                embed.set_thumbnail(url = audits.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await self.channel.send(embed=embed)

    async def edit_emoji(self, raw_emoji : discord.RawReactionActionEvent):
        if self.guild.owner==raw_emoji.member:
            target = 'Создатель сервера'
        elif raw_emoji.member.guild_permissions.administrator:
            target = 'Администратор'
        else:
            target = 'Пользователь'
        if raw_emoji.event_type == "REACTION_ADD":
            embed = discord.Embed(color=Colors.GREEN.value)
            embed.set_author(name = f'{target} поставил реакцию', icon_url = 'https://i.ibb.co/Fsk4K5H/add-react.png')
            changed_role = 'Выданная роль'
        else:
            embed = discord.Embed(color=Colors.RED.value)
            embed.set_author(name = f'{target} убрал реакцию', icon_url = 'https://i.ibb.co/wy9P1wJ/remove-react.png')
            changed_role = 'Убранная роль'
        member = raw_emoji.member
        embed.add_field(name = f'{target}:', value = f'{member.mention} | `{member.name}#{member.discriminator}`')
        if member.avatar:
            embed.set_thumbnail(url = member.avatar.url)
        channel = guild.get_channel(raw_emoji.channel_id)
        message = await channel.fetch_message(raw_emoji.message_id)
        embed.add_field(name = 'Сообщение:', value = f'> [Гиперссылка]({message.jump_url})', inline=False)
        embed.add_field(name = 'Реакция:', value = f'{raw_emoji.emoji}')
        """if roleid:
            role = guild.get_role(int(roleid))
            embed.add_field(name=f'{changed_role}:',value=f'{role.mention}')"""
        await self.channel.send(embed=embed)

    async def new_member(self, mem : discord.Member):
        roleid = Guild(self.guild.id).welcome_role
        role = self.guild.get_role(roleid)
        embed = discord.Embed(color = Colors.GREEN.value)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name = 'Новый пользователь на сервере')
        embed.add_field(name = 'Пользователь:', value = f'{mem.mention} | `{mem.name}#{mem.discriminator}`')
        if roleid:
            embed.add_field(name = 'Выданная роль:', value = f'{role.mention}')
        if mem.avatar:
            embed.set_thumbnail(url = mem.avatar.url)
        await self.channel.send(embed = embed)

    async def member_update(self, beforemem : discord.Member, aftermem : discord.Member):
        if beforemem == beforemem.guild.owner:
            target, target2 = 'cоздателя сервера', 'Создатель сервера'
        elif beforemem.guild_permissions.administrator:
            target, target2 = 'администратора', 'Администратор'
        else:
            target, target2 = 'пользователя', 'Пользователь'
        if aftermem.nick is None:
            aftername = aftermem.name
        else:
            aftername = aftermem.nick
        if beforemem.nick is None:
            beforename = beforemem.name
        else:
            beforename = beforemem.nick
        embed = discord.Embed(color = Colors.YELLOW.value)
        embed.add_field(name = f'{target2}:', value = f'{beforemem.mention} | `{beforemem.name}#{beforemem.discriminator}`', inline = False)
        if aftername != beforename:
            embed.set_author(name = f'У {target} изменили имя на сервере')
            embed.add_field(name = 'Старое имя:', value = f'{beforename}')
            embed.add_field(name = 'Новое имя:', value = f'{aftername}')
            auditlist = list(await self.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_update).flatten())
            if auditlist:
                audits = auditlist[0]
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`", inline = False)
                if audits.user.avatar:
                    embed.set_thumbnail(url=audits.user.avatar.url)
        elif len(beforemem.roles) > len(aftermem.roles):
            embed.set_author(name=f'У {target} изменили роли')
            old_role = next(role for role in beforemem.roles if role not in aftermem.roles)
            auditlist=list(await beforemem.guild.audit_logs(limit=1,action=discord.AuditLogAction.member_role_update).flatten())
            if auditlist:
                audits=auditlist[0]
                embed.add_field(name = 'Убранная роль:', value = old_role.mention)
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`", inline = False)
                if audits.user.avatar:
                    embed.set_thumbnail(url=audits.user.avatar.url)
        elif len(beforemem.roles) < len(aftermem.roles):
            embed.set_author(name=f'У {target} изменили роли')
            new_role = next(role for role in aftermem.roles if role not in beforemem.roles)
            auditlist = list(await self.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_role_update).flatten())
            if auditlist:
                audits = auditlist[0]
                embed.add_field(name = 'Добавленная роль:', value = new_role.mention)
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`", inline = False)
                if audits.user.avatar:
                    embed.set_thumbnail(url = audits.user.avatar.url)
        elif beforemem.timed_out != aftermem.timed_out:
            if beforemem.timed_out:
                embed.set_author(name = f'Для {target} был снят тайм-аут')
            else:
                embed.set_author(name = f'Для {target} был установлен тайм-аут')
                embed.add_field(name = 'Истечет:', value = f'{discord.utils.format_dt(aftermem.communication_disabled_until)}')
        await self.channel.send(embed = embed)

    async def member_leave(self, mem : discord.Member):
        embed = discord.Embed(color = Colors.RED.value)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name = 'Пользователь вышел с сервера', icon_url = 'https://i.ibb.co/vhgg0C8/disconnect-from-server.png')
        embed.add_field(name='Пользователь:', value = f"{mem.mention} | `{mem.name}#{mem.discriminator}`", inline = False)
        if mem.avatar:
            embed.set_thumbnail(url = mem.avatar.url)
        await self.channel.send(embed = embed)

    async def member_ban(self, user : discord.User):
        embed = discord.Embed(color = Colors.RED.value)
        embed.set_author(name = 'Пользователь забанен', icon_url = 'https://i.ibb.co/vhgg0C8/disconnect-from-server.png')
        embed.add_field(name = 'Пользователь:', value = f"{user.mention} | `{user.name}#{user.discriminator}`", inline = False)
        async for audits in self.guild.audit_logs(limit = 1, action = discord.AuditLogAction.ban):
            embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`", inline = False)
            if audits.user.avatar:
                embed.set_thumbnail(url = audits.user.avatar.url)
        await self.channel.send(embed = embed)

    async def member_unban(self, user : discord.User):
        embed = discord.Embed(color = Colors.GREEN.value)
        embed.set_author(name = 'Пользователь разбанен', icon_url = 'https://i.ibb.co/cg9hwSf/connect-to-server.png')
        embed.add_field(name = 'Пользователь:', value = f"{user.mention} | `{user.name}#{user.discriminator}`")
        async for audits in self.guild.audit_logs(action = discord.AuditLogAction.ban):
            if audits.target == user:
                embed.add_field(name = 'Кто забанил:', value = f"f{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`", inline = False)
                break
        async for audits in self.guild.audit_logs(limit = 1, action = discord.AuditLogAction.unban):
            embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`", inline = False)
            if audits.user.avatar:
                embed.set_thumbnail(url = audits.user.avatar.url)
            await self.channel.send(embed = embed)

    async def message_delete(self, message : discord.Message):
        embed = discord.Embed(color = Colors.RED.value)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name = 'Сообщение удалено', icon_url = 'https://i.ibb.co/2Zkb5JD/delete-msg.png')
        embed.add_field(name = 'Канал:', value = message.channel.mention)
        embed.add_field(name = 'Автор:', value = f"{message.author.mention} | `{message.author.name}#{message.author.discriminator}`")
        if message.embeds == []:
            embed.add_field(name = 'Сообщение:', value = f'> {message.content}', inline = False)
        else:
            embed.add_field(name = 'Сообщение:', value = 'Сообщение со вставкой', inline = False)
        async for audits in message.guild.audit_logs(limit = 1, action = discord.AuditLogAction.message_delete):
            if audits.user != bot and message.author != bot:
                if audits.user != message.author:
                    embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`", inline = False)
                elif audits.user == message.author:
                    embed.set_author(name='Сообщение удалено автором', icon_url = 'https://i.ibb.co/2Zkb5JD/delete-msg.png')
                if audits.user.avatar:
                    embed.set_thumbnail(url = audits.user.avatar.url)
                await self.channel.send(embed = embed)

    async def guild_update(self, be_guild : discord.Guild, af_guild : discord.Guild):
        embed = discord.Embed(color = Colors.YELLOW.value)
        embed.timestamp = discord.utils.utcnow()
        if be_guild.name != af_guild.name:
            embed.set_author(name = 'Название сервера изменено', icon_url = 'https://i.ibb.co/KzfhVzp/server-edit.png')
            embed.add_field(name = 'Старое название:', value = be_guild.name)
            embed.add_field(name = 'Новое название:', value = af_guild.name)
            async for audits in be_guild.audit_logs(limit = 1, action = discord.AuditLogAction.guild_update):
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`")
                if audits.user.avatar:
                    embed.set_thumbnail(url = audits.user.avatar.url)
        elif be_guild.icon != af_guild.icon:
            embed.set_author(name = 'Значок сервера изменен', icon_url = 'https://i.ibb.co/KzfhVzp/server-edit.png')
            embed.add_field(name = 'Старый значок:', value = be_guild.icon.url)
            embed.add_field(name = 'Новый значок:', value = af_guild.icon.url)
            async for audits in be_guild.audit_logs(limit = 1, action = discord.AuditLogAction.guild_update):
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`")
                if audits.user.avatar:
                    embed.set_thumbnail(url = audits.user.avatar.url)
        elif be_guild.afk_timeout != af_guild.afk_timeout:
            embed.set_author(name = 'Значение афк сервера изменено(в минутах)', icon_url = 'https://i.ibb.co/KzfhVzp/server-edit.png')
            embed.add_field(name = 'Старое значение:', value = int(be_guild.afk_timeout/60))
            embed.add_field(name = 'Новое значение:', value = int(af_guild.afk_timeout/60))
            async for audits in be_guild.audit_logs(limit=1,action=discord.AuditLogAction.guild_update):
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`")
                if audits.user.avatar:
                    embed.set_thumbnail(url = audits.user.avatar.url)
        elif be_guild.afk_channel != af_guild.afk_channel:
            embed.set_author(name = 'Афк канал сервера изменен', icon_url = 'https://i.ibb.co/KzfhVzp/server-edit.png')
            embed.add_field(name = 'Старый канал:', value = f"{be_guild.afk_channel.name} | {be_guild.afk_channel.mention}")
            embed.add_field(name = 'Новый канал:', value = f"{af_guild.afk_channel.name} | {af_guild.afk_channel.mention}")
            async for audits in be_guild.audit_logs(limit=1,action=discord.AuditLogAction.guild_update):
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`")
                if audits.user.avatar:
                    embed.set_thumbnail(url = audits.user.avatar.url)
        elif be_guild.owner_id != af_guild.owner_id:
            embed.set_author(name = 'Права на сервер перданы', icon_url = 'https://i.ibb.co/KzfhVzp/server-edit.png')
            embed.add_field(name = 'Старый создатель:', value = f"{be_guild.owner.mention} | `{be_guild.owner.name}#{be_guild.owner.discriminator}`")
            embed.add_field(name = 'Новый создатель:', value = f"{af_guild.owner.mention} | `{af_guild.owner.name}#{af_guild.owner.discriminator}`")
            if be_guild.owner.avatar:
                embed.set_thumbnail(url = be_guild.owner.avatar.url)
        await self.channel.send(embed=embed)

    def get_role_perms(self, role_perms : discord.Permissions) -> list:
        if role_perms.administrator:
            return ['`администратор`']
        perms = []
        if role_perms.create_instant_invite:
            perms.append('`создавать приглашения`')
        if role_perms.kick_members:
            perms.append('`кикать`')
        if role_perms.ban_members:
            perms.append('`банить`')
        if role_perms.manage_channels:
            perms.append('`управление каналами`')
        if role_perms.manage_guild:
            perms.append('`управление сервером`')
        if role_perms.add_reactions:
            perms.append('`добавление реакций`')
        if role_perms.view_audit_log:
            perms.append('`просмотр журнала аудита`')
        if role_perms.priority_speaker:
            perms.append('`приорететный режим`')
        if role_perms.stream:
            perms.append('`стримить`')
        if role_perms.read_messages:
            perms.append('`видеть каналы`')
        if role_perms.read_message_history:
            perms.append('`смотреть историю сообщений`')
        if role_perms.send_messages:
            perms.append('`отправлять сообщения`')
        if role_perms.send_tts_messages:
            perms.append('`отправлять голосовые сообщения`')
        if role_perms.manage_messages:
            perms.append('`управлять сообщениями`')
        if role_perms.embed_links:
            perms.append('`встраивать ссылки`')
        if role_perms.attach_files:
            perms.append('`приклеплять файлы`')
        if role_perms.mention_everyone:
            perms.append('`упоминать @everyone и @here`')
        if role_perms.external_emojis:
            perms.append('`использовать внешние эмодзи`')
        if role_perms.connect:
            perms.append('`подключаться`')
        if role_perms.speak:
            perms.append('`говорить`')
        if role_perms.mute_members:
            perms.append('`мутить`')
        if role_perms.deafen_members:
            perms.append('`отключать звук`')
        if role_perms.move_members:
            perms.append('`перемещать участников`')
        if role_perms.use_voice_activation:
            perms.append('`использование режима активации по голосу`')
        if role_perms.change_nickname:
            perms.append('`изменять никнейм`')
        if role_perms.manage_nicknames:
            perms.append('`управлять никнеймами`')
        if role_perms.manage_roles:
            perms.append('`управлять ролями`')
        if role_perms.manage_webhooks:
            perms.append('`управлять вебхуками`')
        if role_perms.manage_emojis:
            perms.append('`управлять эмодзи`')
        return perms

    async def guild_role_create(self, role : discord.Role):
        embed = discord.Embed(color = Colors.GREEN.value)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name = 'Роль создана', icon_url = 'https://i.ibb.co/7NxHh2g/create-role.png')
        async for audits in role.guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_create):
            if audits.user != bot:
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`")
                if audits.user.avatar:
                    embed.set_thumbnail(url = audits.user.avatar.url)
        await self.channel.send(embed=embed)

    async def guild_role_delete(self, role : discord.Role):
        embed = discord.Embed(color = Colors.RED.value)
        embed.set_author(name = 'Роль удалена', icon_url = 'https://i.ibb.co/nBnkLvF/remove-role.png')
        embed.add_field(name = 'Роль:', value = f'@{role.name}')
        embed.add_field(name = 'Цвет:', value = f"[Перейти](https://www.color-hex.com/color/{str(role.color)[1:7]})")
        embed.add_field(name = 'Список прав', value = ', '.join(self.get_role_perms(role)), inline = False)
        async for audits in role.guild.audit_logs(limit=1,action=discord.AuditLogAction.role_delete):
            if audits.user != bot:
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`")
                if audits.user.avatar:
                    embed.set_thumbnail(url=audits.user.avatar.url)
        await self.channel.send(embed=embed)

    async def guild_role_update(self, be_role : discord.Role, af_role : discord.Role):
        embed = discord.Embed(color = Colors.YELLOW.value)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name = 'Роль изменена', icon_url = 'https://i.ibb.co/0Fm76j2/edit-role.png')
        if be_role.name != af_role.name:
            embed.add_field(name = 'Роль',value = af_role.mention)
            embed.add_field(name = 'Старое имя:',value = be_role.name)
            embed.add_field(name = 'Новое имя:', value = af_role.name)
        if be_role.color != af_role.color:
            embed.add_field(name = 'Роль', value = af_role.mention)
            embed.add_field(name = 'Старый цвет:', value = '[Перейти](https://www.color-hex.com/color/'+str(be_role.color)[1:7]+')')
            embed.add_field(name = 'Новый цвет:', value = '[Перейти](https://www.color-hex.com/color/'+str(af_role.color)[1:7]+')')
        if be_role.hoist != af_role.hoist:
            embed.add_field(name = 'Роль', value = af_role.mention)
            if af_role.hoist:
                embed.add_field(name = 'Статус:', value = 'Теперь учатники с этой ролью показываются отдельно')
            else:
                embed.add_field(name = 'Статус:', value = 'Теперь учатники с этой ролью `не` показываются отдельно')
        if be_role.mentionable != af_role.mentionable:
            embed.add_field(name ='Роль', value = af_role.mention)
            if af_role.mentionable:
                embed.add_field(name = 'Статус:', value = 'Теперь учатники с этой ролью могут упоминать @everyone и @here и др. роли')
            else:
                embed.add_field(name = 'Статус:', value = 'Теперь учатники с этой ролью `не` могут упоминать @everyone и @here и др. роли')
        if be_role.permissions != af_role.permissions:
            addperms = list(set(self.get_role_perms(af_role.permissions)) - set(self.get_role_perms(be_role.permissions)))
            remperms = list(set(self.get_role_perms(be_role.permissions)) - set(self.get_role_perms(af_role.permissions)))
            if addperms != []:
                embed.add_field(name = 'Добавленные права:', value = ', '.join(addperms))
            if remperms != []:
                embed.add_field(name = 'Убранные права:', value = ', '.join(remperms))
            embed.add_field(name = 'Список прав:',value=', '.join(self.get_role_perms(af_role.permissions)), inline = False)
        async for audits in be_role.guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_update):
            if audits.user != bot:
                embed.add_field(name = 'Модератор:', value = f"{audits.user.mention} | `{audits.user.name}#{audits.user.discriminator}`", inline = False)
                if audits.user.avatar:
                    embed.set_thumbnail(url = audits.user.avatar.url)
                await self.channel.send(embed = embed)

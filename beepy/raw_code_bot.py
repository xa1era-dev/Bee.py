






""""""

async def emojirole_add_slash(ctx,emoji,msg,role):
    await ctx.response.defer()
    if not Guild(msg.id).emojirole.get_role(emoji.id):
        await msg.add_reaction(await ctx.guild.fetch_emoji(emoji.id))
        Modules(ctx.guild.id).emojirole.add_role(msg.id,emoji.id,role.id)

async def raw_reac_edit(pay:discord.RawReactionActionEvent):
    roleid = Modules(pay.message_id).emojirole.get_role(pay.emoji.id)
    guild=bot.get_guild(pay.guild_id)
    if roleid:
        role=guild.get_role(int(roleid))
        if pay.event_type=="REACTION_ADD":
            member=pay.member
            await member.add_roles(role)
        else:
            member=guild.get_member(pay.user_id)
            await member.remove_roles(role)

async def welcome_role(ctx:discord.ApplicationContext,option,role):
    loadembed=discord.Embed(color=Colors.Gray.value,title='Обработка данных')
    msg=await ctx.response.send_message(embed=loadembed,ephemeral=True)
    if ctx.author.guild_permissions.administrator==True:
        if option=='set':
            embed=discord.Embed(color=Colors.Yellow.value,description='Роль выставлена')
            embed.set_author(name='Успех')
            embed.add_field(name='Роль будет выдаваться при заходе на сервер:',value=f'{role.mention}')
            beroleid=Modules(ctx.guild.id).welcome_role
            if beroleid:
                befrole=ctx.guild.get_role(int(beroleid))
                embed.add_field(name='Старая роль:',value=f'{befrole.mention}',inline=False)
            await msg.edit_original_message(embed=embed)
            Modules(ctx.guild.id).welcome_role=role.id
        else:
            embed=discord.Embed(color=Colors.Yellow.value,description='Роль выставлена')
            embed.set_author(name='Успех')
            beroleid=Modules(ctx.guild.id).welcome_role
            if beroleid:
                befrole=ctx.guild.get_role(int(beroleid))
                embed.add_field(name='Старая роль:',value=f'{befrole.mention}',inline=False)
            await msg.edit_original_message(embed=embed)
            del Modules(ctx.guild.id).welcome_role

async def member_join(mem:discord.Member):
    welrolid = Guild(mem.guild.id).welcome_role
    if welrolid:
        role = mem.guild.get_role(welrolid)
        await mem.add_roles(role)





async def member_update(beforemem:discord.Member, aftermem:discord.Member):
    pass

async def check_ping():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = f'Ping: {round(bot.latency * 1000)} ms'))
    await asyncio.sleep(60)
    await check_ping()



""""""

"""@bot.slash_command(name = 'test')
async def test(ctx : discord.ApplicationContext):
    testemb = discord.Embed(color = Colors.Gray.value, title = 'Test')
    selected_dict = {}
    class TestS(discord.ui.Select):
        def __init__(self):
            super().__init__(placeholder = 'Test', min_values = 1, max_values = 1, options = [discord.SelectOption(label="Red", description="Your favourite colour is red", emoji="🟥",  value = 'red1'),
        discord.SelectOption(label="Green", description="Your favourite colour is green", emoji="🟩", value = 'green1'),
        discord.SelectOption(label="Blue", description="Your favourite colour is blue", emoji="🟦",  value = 'blue1'),], row = 1)
        async def callback (self, inter : discord.Interaction):
            selected_dict[f'{inter.user.id}'] = inter.data['values']
            print(selected_dict)
    class Test(discord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
            self.add_item(TestS())
        @discord.ui.button(label = '✅', style = discord.ButtonStyle.green, row = 2)
        async def callback(self, button, inter):
            print(selected_dict)
    await ctx.respond(embed=testemb, view = Test())"""


@bot.slash_command(
    name='welcomerole',
    description='Выдача ролей при заход на сервер')
async def welcomerole(
    ctx:discord.ApplicationContext,
    option:discord.Option(
        str,
        'Состояние функции',
        choices=['set','remove']),
    role:discord.Role):
    await welcome_role(ctx,option,role)

emojirole=SlashCommandGroup('emojirole','Позволяет управлять эмодзи для выдачи родей')

@emojirole.command(
    name='add',
    description='Установка эмоджи для выдачи ролей')
async def add(
        ctx: discord.ApplicationContext,
        emoji:discord.Emoji,
        msgid:discord.Message,
        role:discord.Role):
    await emojirole_add_slash(ctx,emoji,msgid,role)

@emojirole.command(
    name='editwip',
    description='Изменять эмодзи для выдачи ролей')
async def edit(
        ctx:discord.ApplicationContext):
    print(ctx)

@emojirole.command(
    name='removewip',
    description='Изменять эмодзи для выдачи ролей')
async def remove(
        ctx:discord.ApplicationContext):
    print(ctx)

bot.add_application_command(emojirole)

"""
@bot.command(pass_context=True)
async def embed(ctx, *args):
    print(args)
    reason=[]
    for arg in args:
        reason.append(str(arg))
    em=' '.join(reason)
    text=re.search('text:(.*?):text', em)[0]
    color=re.search('color:(.*?) ', em)[0]
    title=re.search('title:(.*?) ', em)[0]
    emtext=text[5:len(text)-5]
    emcolor=discord.Colour(int(color[len(color)-7:len(color)-1],16))
    emtitle=title[6:len(title)-1]
    embed=discord.Embed(color=emcolor,description=emtext,title=emtitle)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def guild(ctx, *args):
    await ctx.message.delete()
    bot=bot.get_user(713831247285190726)
    cursor.execute("SELECT prefix FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
    info=cursor.fetchall()[0]
    prefix=str(info)[2:len(str(info))-3]
    if args is None:
        guildhelp=discord.Embed(color=0x808080,title='Введите `'+prefix+'guild help` для просмотра команд для сервера(WIP)')
        guildhelp.set_footer(text='Автоматическое удаление через 5 секунд')
        guildhelp.timestamp = discord.utils.utcnow()
        msg=await ctx.send(embed=guildhelp)
        await asyncio.sleep(5)
        if msg:
            await msg.delete()
    else:
        if args[0]=='role':
            if ctx.message.author.guild_permissions.administrator==True:
                if args[1]!='none':
                    role=discord.utils.get(ctx.guild.roles,id=int(''.join(filter(str.isdigit,args[1]))))
                    if role:
                        cursor.execute("SELECT welcomerole FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                        info=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
                        rol=discord.utils.get(ctx.guild.roles,id=info)
                        if rol:
                            rolech=discord.Embed(color=0x808080,title='Роль захода на сервер изменена')
                            rolech.add_field(name='Старая роль:',value=rol.mention)
                            rolech.add_field(name='Новая роль:',value=role.mention)
                            rolech.timestamp = discord.utils.utcnow()
                            cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                            if len(cursor.fetchall())>7:
                                info=int(str(cursor.fetchall()[0])[3:len(str(cursor.fetchall()[0]))-4])
                                if info:
                                    auditlog=discord.utils.get(ctx.guild.text_channels,id=info)
                                await auditlog.send(embed=rolech)
                            else:
                                await ctx.send(embed=rolech)
                            cursor.execute("UPDATE guildsinfo SET welcomerole=%s WHERE guildid='%s'",(role.id,ctx.guild.id))
                            conn.commit()
                        else:
                            rolech=discord.Embed(color=0x808080,title='Роль захода на сервер поставлена')
                            rolech.add_field(name='Роль:',value=role.mention)
                            rolech.timestamp = discord.utils.utcnow()
                            cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                            info=int(str(cursor.fetchall()[0])[3:len(str(cursor.fetchall()[0]))-4])
                            if info:
                                auditlog=discord.utils.get(ctx.guild.text_channels,id=info)
                                await auditlog.send(embed=rolech)
                            cursor.execute("UPDATE guildsinfo SET welcomerole=%s WHERE guildid='%s'",(role.id,ctx.guild.id))
                            conn.commit()
                elif args[1]=='none':
                    cursor.execute("SELECT welcomerole FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                    info=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
                    rol=discord.utils.get(ctx.guild.roles,id=info)
                    rolech=discord.Embed(color=0x808080,title='Роль захода на сервер удалена')
                    rolech.add_field(name='Роль:',value=rol.mention)
                    rolech.timestamp = discord.utils.utcnow()
                    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                    if len(cursor.fetchall()[0])>7:
                        info=int(str(cursor.fetchall()[0])[3:len(str(cursor.fetchall()[0]))-4])
                        if info:
                            auditlog=discord.utils.get(ctx.guild.text_channels,id=info)
                            await auditlog.send(embed=rolech)
                    cursor.execute("UPDATE guildsinfo SET welcomerole=%s WHERE guildid='%s'",(0,ctx.guild.id))
                    conn.commit()
                else:
                    enable=discord.Embed(color=0x808080,title='Вы не выделили роль')
                    enable.timestamp = discord.utils.utcnow()
                    enable.set_footer(text='Автоматическое удаление через 3 секунд')
                    msg=await ctx.send(embed=enable)
                    await asyncio.sleep(3)
                    if msg:
                        await msg.delete()
            else:
                enable=discord.Embed(color=0x808080,title='У вас нет прав администратора',icon_url='https://i.ibb.co/k4PhcqB/not-perms.png')
                enable.timestamp = discord.utils.utcnow()
                enable.set_footer(text='Автоматическое удаление через 3 секунд')
                msg=await ctx.send(embed=enable)
                await asyncio.sleep(3)
                if msg:
                    await msg.delete()
        elif args[0]=='info':
            enable=discord.Embed(color=0x808080,title='Информация о сервере '+ctx.guild.name)
            enable.set_thumbnail(url=ctx.guild.icon_url)
            enable.add_field(name='Количество пользователей:',value=len(ctx.guild.members))
            enable.add_field(name='Дата создания:',value=ctx.guild.created_at.replace(microsecond=0),inline=False)
            enable.add_field(name='Создатель сервера:',value=ctx.guild.owner.mention+' | '+'`'+ctx.guild.owner.name+'#'+ctx.guild.owner.discriminator+'`',inline=False)
            online=0
            for mem in ctx.guild.members:
                if mem.status is not discord.Status.offline:
                    online+=1
            enable.add_field(name='Пользователи онлайн:',value=online)
            enable.timestamp = discord.utils.utcnow()
            enable.set_footer(text='Автоматическое удаление через 30 секунд')
            msg=await ctx.send(embed=enable)
            await asyncio.sleep(30)
            if msg:
                await msg.delete()
        elif args[0]=='prefix':
            if ctx.message.author.guild_permissions.administrator==True:
                if args[1]:
                    cursor.execute("SELECT prefix FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                    info=cursor.fetchall()[0]
                    pref=str(info)[2:len(str(info))-3]
                    enable=discord.Embed(color=0x808080,title='Префикс перед командами был изменен')
                    enable.add_field(name='Старый префикс:',value=pref)
                    enable.add_field(name='Новый префикс:',value=args[1])
                    enable.timestamp = discord.utils.utcnow()
                    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                    if len(cursor.fetchall())>7:
                        info=int(str(cursor.fetchall()[0])[3:len(str(cursor.fetchall()[0]))-4])
                        if info:
                            auditlog=discord.utils.get(ctx.guild.text_channels,id=info)
                        await auditlog.send(embed=enable)
                    else:
                        await ctx.send(embed=enable)
                    cursor.execute("UPDATE guildsinfo SET prefix=%s WHERE guildid='%s'",[args[1],ctx.guild.id])
                    conn.commit()
                else:
                    enable=discord.Embed(color=0x808080,title='Вы не выбрали префикс')
                    enable.timestamp = discord.utils.utcnow()
                    enable.set_footer(text='Автоматическое удаление через 3 секунд')
                    msg=await ctx.send(embed=enable)
                    await asyncio.sleep(3)
                    if msg:
                        await msg.delete()
            else:
                enable=discord.Embed(color=0x808080,title='У вас нет прав администратора',icon_url='https://i.ibb.co/k4PhcqB/not-perms.png')
                enable.timestamp = discord.utils.utcnow()
                enable.set_footer(text='Автоматическое удаление через 3 секунд')
                msg=await ctx.send(embed=enable)
                await asyncio.sleep(3)
                if msg:
                    await msg.delete()
        elif args[0]=='emoterole':
            if ctx.message.author.guild_permissions.administrator==True:
                if args[1]:
                    if args[2]:
                        if args[3]:
                            msg=await ctx.message.channel.fetch_message(int(args[1]))
                            if msg:
                                emoji= await ctx.guild.fetch_emoji(int(''.join(filter(str.isdigit,args[2]))))
                                if emoji:
                                    if args[3]!='none':
                                        role=discord.utils.get(ctx.guild.roles,id=int(''.join(filter(str.isdigit,args[3]))))
                                        if role:
                                            cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                                            info=cursor.fetchall()
                                            cursor.execute("INSERT INTO emojirole VALUES (%s, %s, %s, %s)",(ctx.guild.id,msg.id,emoji.id,role.id))
                                            conn.commit()
                                            await msg.add_reaction(emoji)
                                            embed=discord.Embed(color=0x43b581)
                                            embed.timestamp=discord.utils.utcnow()
                                            embed.set_author(name='Роль при постановлении реакции установлена')
                                            embed.add_field(name='Сообщение:',value='> '+msg.content+'|[Перейти]('+msg.jump_url+')',inline=False)
                                            embed.add_field(name='Эмоция:',value=emoji,inline=False)
                                            embed.add_field(name='Роль:',value=role.mention,inline=False)
                                            embed.add_field(name='Оставшиеся места:',value='У вас безлимит',inline=False)
                                            if info:
                                                auditlogid=int(''.join(filter(str.isdigit,info.pop(0))))
                                                auditlog=discord.utils.get(ctx.guild.text_channels,id=auditlogid)
                                                await auditlog.send(embed=embed)
                                            else:
                                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                                message=await ctx.send(embed=embed)
                                                await asyncio.sleep(30)
                                                if message:
                                                    await message.delete()
                                    else:
                                        cursor.execute("SELECT roleid FROM emojirole WHERE msgid='%s'",[msg.id])
                                        info=cursor.fetchall()
                                        roleid=int(''.join(filter(str.isdigit,info.pop(0))))
                                        role=discord.utils.get(ctx.guild.roles,id=roleid)
                                        cursor.execute("DELETE FROM emojirole WHERE msgid='%s'",[msg.id])
                                        conn.commit()
                                        await msg.remove_reaction(emoji,bot)
                                        cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                                        info=cursor.fetchall()
                                        embed=discord.Embed(color=0xf04747)
                                        embed.timestamp=discord.utils.utcnow()
                                        embed.set_author(name='Роль при постановлении реакции удалена')
                                        embed.add_field(name='Сообщение:',value='> '+msg.content+'|[Перейти]('+msg.jump_url+')',inline=False)
                                        embed.add_field(name='Эмоция:',value=emoji,inline=False)
                                        embed.add_field(name='Роль:',value=role.mention,inline=False)
                                        embed.add_field(name='Оставшиеся места:',value='У вас безлимит',inline=False)
                                        if info:
                                            auditlogid=int(''.join(filter(str.isdigit,info.pop(0))))
                                            auditlog=discord.utils.get(ctx.guild.text_channels,id=auditlogid)
                                            await auditlog.send(embed=embed)
                                        else:
                                            embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                            message=await ctx.send(embed=embed)
                                            await asyncio.sleep(30)
                                            if message:
                                                await message.delete()
        elif args[0]=='auditlog':
            if args[1]=='enable':
                cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                info=cursor.fetchall()
                if len(str(info))<10:
                    auditlogid=int(''.join(filter(str.isdigit,info.pop(0))))
                    auditlog=await ctx.guild.create_text_channel(name='журнал-аудита')
                    everyone=discord.utils.get(ctx.guild.roles,name='@everyone')
                    await auditlog.set_permissions(everyone,view_channel=False,send_messages=False)
                    roomhelp=discord.Embed(color=0x808080,title='Модуль `журнал аудита` был активирован. Этот канал будет журналом аудита')
                    roomhelp.timestamp = discord.utils.utcnow()
                    msg=await auditlog.send(embed=roomhelp)
                    cursor.execute("UPDATE guildsinfo SET auditlogid='%s' WHERE guildid='%s'",(auditlog.id,ctx.guild.id))
                    conn.commit()
                else:
                    roomhelp=discord.Embed(color=0x808080,title='Модуль `журнал аудита` уже активирован')
                    roomhelp.set_footer(text='Автоматическое удаление через 5 секунд')
                    roomhelp.timestamp = discord.utils.utcnow()
                    msg=await ctx.send(embed=roomhelp)
                    await asyncio.sleep(5)
                    if msg:
                        await msg.delete()
            elif args[1]=='disable':
                cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                info=cursor.fetchall()
                if info:
                    auditlogid=int(''.join(filter(str.isdigit,info.pop(0))))
                    auditlog=discord.utils.get(ctx.guild.text_channels,id=auditlogid)
                    await auditlog.delete()
                    roomhelp=discord.Embed(color=0x808080,title='Модуль `журнал аудита` был отключен.')
                    roomhelp.set_footer(text='Автоматическое удаление через 5 секунд')
                    roomhelp.timestamp = discord.utils.utcnow()
                    msg=await ctx.send(embed=roomhelp)
                    await asyncio.sleep(5)
                    if msg:
                        await msg.delete()
                else:
                    roomhelp=discord.Embed(color=0x808080,title='Модуль `журнал аудита` не активирован')
                    roomhelp.set_footer(text='Автоматическое удаление через 5 секунд')
                    roomhelp.timestamp = discord.utils.utcnow()
                    msg=await ctx.send(embed=roomhelp)
                    await asyncio.sleep(5)
                    if msg:
                        await msg.delete()
        elif args[0]=='moderate':
            if args[1]:
                cursor.execute("SELECT modrole FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                info=cursor.fetchall()
                modchan=await ctx.guild.create_text_channel(name='журнал модерации')
                everyone=discord.utils.get(ctx.guild.roles,name='@everyone')
                await modchan.set_permissions(target=everyone,view_channel=False,send_messages=False,add_reactions=False)
                moder=ctx.guild.get_role(int(''.join(filter(str.isdigit,args[1]))))
                cursor.execute("UPDATE guildsinfo SET modrole='%s' , modchan='%s' WHERE guildid='%s'",(moder.id,modchan.id,ctx.guild.id))
                conn.commit()
                embed=discord.Embed(color=0x808080)
                embed.set_author(name='Роль модераторов назначена')
                embed.add_field(name='Роль:',value=moder.mention)
                embed.add_field(name='Модератор:',value=ctx.message.author.mention+' | `'+ctx.message.author.name+'#'+ctx.message.author.discriminator+'`',inline=False)
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                embed.timestamp = discord.utils.utcnow()
                cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[ctx.message.guild.id])
                auditlogid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
                if auditlogid!=0:
                    channel = discord.utils.get(ctx.message.guild.channels, id=auditlogid)
                    await channel.send(embed=embed)
                else:
                    embed.set_footer(text='Автоматическое удаление через 5 секунд')
                    embed.timestamp = discord.utils.utcnow()
                    msg=await ctx.send(embed=embed)
                    await asyncio.sleep(5)
                    if msg:
                        await msg.delete()
        else:
            roomhelp=discord.Embed(color=0x808080,title='Введите `'+prefix+'guild help` для просмотра команд для сервера(WIP)')
            roomhelp.set_footer(text='Автоматическое удаление через 5 секунд')
            roomhelp.timestamp = discord.utils.utcnow()
            msg=await ctx.send(embed=roomhelp)
            await asyncio.sleep(5)
            if msg:
                await msg.delete()

@bot.command(pass_context=True)
async def webhook(ctx):
    await ctx.message.delete()
    cursor.execute("SELECT webhook FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
    info=cursor.fetchall()
    if len(str(info))<15: 
        bot=ctx.guild.get_member(713831247285190726)
        webhook=await ctx.message.channel.create_webhook(name='Обновления бота',avatar=await (bot.avatar_url_as(format='png',size=1024)).read())
        cursor.execute("UPDATE guildsinfo SET webhook='%s' WHERE guildid='%s'",(webhook.id,ctx.guild.id))
        conn.commit()
    else:
        enable=discord.Embed(color=0x808080,title='У вас уже имеется вебхук')
        enable.timestamp = discord.utils.utcnow()
        enable.set_footer(text='Автоматическое удаление через 3 секунд')
        msg=await ctx.send(embed=enable)
        await asyncio.sleep(3)
        if msg:
            await msg.delete()

@bot.command(pass_context=True)
async def webhooksend(ctx):
    await ctx.message.delete()
    channel=discord.utils.get(ctx.guild.text_channels,id=886262435177173002)
    async for msg in channel.history(limit=1):
        if msg.id!=ctx.message.id:
            for guild in bot.guilds:
                async with aiohttp.ClientSession() as session:
                    cursor.execute("SELECT webhook FROM guildsinfo WHERE guildid='%s'",[guild.id])
                    info=cursor.fetchall()
                    if len(str(info))>10:
                        webhook=await bot.fetch_webhook(int(''.join(filter(str.isdigit,info.pop(0)))))
                        if webhook:
                            await webhook.send(content=msg.content)
                    
@bot.command(pass_context=True)
async def teams(ctx, *args):
    await ctx.message.delete()
    cursor.execute("SELECT prefix FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
    info=cursor.fetchall()[0]
    prefix=str(info)[2:len(str(info))-3]
    cursor.execute("SELECT teams FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
    info=cursor.fetchall()
    if len(str(info))>15: 
        teamsid=int(''.join(filter(str.isdigit,info.pop(0))))
    if args is None:
        roomhelp=discord.Embed(color=0x808080,title='Введите `'+prefix+'teams help` для просмотра команд для сервера(WIP)')
        roomhelp.set_footer(text='Автоматическое удаление через 5 секунд')
        roomhelp.timestamp = discord.utils.utcnow()
        msg=await ctx.send(embed=roomhelp)
        await asyncio.sleep(5)
        if msg:
            await msg.delete()
    else:
        if ctx.message.author.guild_permissions.administrator==True:
            if args[0]=='enable':
                channel = await ctx.guild.create_text_channel('регистрация команд')
                embed=discord.Embed(color=0x808080)
                embed.add_field(name='Список команд:',value='`'+prefix+'team create название_команды(макс 20 символов)`-капитан создает команду'+'\n'+'`'+prefix+'team add othermembers @2-ой_участник @3-ий_участник @4-ый_участник @5-ый_участник`-добавить остальных 4 участников команды. Участников писать через `ПРОБЕЛ`'+'\n'+'`'+prefix+'team add coach @тренер`-добавить тренера команды'+'\n'+'`'+prefix+'team remove member @участник`-удалить участника команды'+'\n'+'`'+prefix+'team add member @участник`-добавить участника'+'\n'+'`'+prefix+'team remove coach`-удалить тренера'+'\n'+'`'+prefix+'team checkin`-подтвердить участние команды на турнире(Доступно в режиме check-in)'+'\n'+'`'+prefix+'team leave`-покинуть команду'+'\n'+'`'+prefix+'team disband`-удалить команду'+'\n`'+prefix+'team info название_команды или @любой_участник_команды` - узнать информацию о команде')
                await channel.send(embed=embed)
                cursor.execute("UPDATE guildsinfo SET teams='%s' WHERE guildid='%s'",(channel.id,ctx.guild.id))
                conn.commit()
            elif args[0]=='disable':
                channel=discord.utils.get(ctx.guild.text_channels,id=teamsid)
                if channel:
                    await channel.delete()
                cursor.execute("UPDATE guildsinfo SET teams='0' WHERE guildid='%s'",[ctx.guild.id])
                conn.commit()
            elif args[0]=='checkin':
                cursor.execute("SELECT checkin FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                info=cursor.fetchall()
                checkin=str(info)[3:len(str(info))-4]
                if checkin=='0':
                    cursor.execute("UPDATE guildsinfo SET checkin='1' WHERE guildid='%s'",[ctx.guild.id])
                    conn.commit()
                    embed=discord.Embed(color=0x43b581,title='Режим чек-ин был активирован')
                    embed.set_footer(text='Автоматическое удаление через 10 секунд')
                    captain=discord.utils.get(ctx.guild.roles,name='Капитан команды')
                    msg=await ctx.send(embed=embed,content=captain.mention)
                else:
                    cursor.execute("UPDATE guildsinfo SET checkin='0' WHERE guildid='%s'",[ctx.guild.id])
                    conn.commit()
                    cursor.execute("UPDATE teams SET cheackin='0'")
                    conn.commit()
                    embed=discord.Embed(color=0xf04747,title='Режим чек-ин был отключен')
                    embed.set_footer(text='Автоматическое удаление через 10 секунд')
                    msg=await ctx.send(embed=embed)
                    await asyncio.sleep(10)
                    if msg:
                        await msg.delete()
            elif args[0]=='info':
                numbers=[]
                teams=[]
                captains=[]
                checkins=[]
                cursor.execute("SELECT row_number() OVER() FROM teams")
                info=cursor.fetchall()
                for abc in info:
                    number=str(abc)[1:len(str(abc))-2]
                    numbers.append(number)
                cursor.execute("SELECT teamname FROM teams")
                info=cursor.fetchall()
                for abc in info:
                    teamname=str(abc)[2:len(str(abc))-3]
                    teams.append(teamname)
                cursor.execute("SELECT captainid FROM teams")
                info=cursor.fetchall()
                for abc in info:
                    captainid=str(abc)[2:len(str(abc))-3]
                    captain=await ctx.guild.fetch_member(captainid)
                    captains.append(captain.mention)
                cursor.execute("SELECT checkin FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                info=cursor.fetchall()
                checking=str(info)[3:len(str(info))-4]
                if checking=='1':
                    cursor.execute("SELECT cheackin FROM teams")
                    info=cursor.fetchall()
                    for abc in info:
                        checkin=str(abc)[1:len(str(abc))-2]
                        checkins.append(checkin)
                embed=discord.Embed(color=0x808080,title='Список команд('+str(len(numbers))+')')
                if len(numbers)>25:
                    embed2=discord.Embed(color=0x808080,title='Список команд('+str(len(numbers))+')')
                elif len(numbers)>50:
                    embed3=discord.Embed(color=0x808080,title='Список команд('+str(len(numbers))+')')
                elif len(numbers)>75:
                    embed4=discord.Embed(color=0x808080,title='Список команд('+str(len(numbers))+')')
                for checkin in checkins:
                    if checking=='1' and checkin=='1':
                        if len(numbers)>0:
                            embed.add_field(name='Команда №'+numbers[checkins.index(checkin)]+':',value='Название  -  '+teams[checkins.index(checkin)]+'\nКапитан  -  '+captains[checkins.index(checkin)],inline=False)
                        elif len(numbers)==0:
                            embed.add_field(name='Ошибка:',value='Команд пока нет')
                        elif len(numbers)>25:
                            embed2.add_field(name='Команда №'+numbers[checkins.index(checkin)]+':',value='Название  -  '+teams[checkins.index(checkin)]+'\nКапитан  -  '+captains[checkins.index(checkin)],inline=False)
                        elif len(numbers)>50:
                            embed3.add_field(name='Команда №'+numbers[checkins.index(checkin)]+':',value='Название  -  '+teams[checkins.index(checkin)]+'\nКапитан  -  '+captains[checkins.index(checkin)],inline=False)
                        elif len(numbers)>75:
                            embed4.add_field(name='Команда №'+numbers[checkins.index(checkin)]+':',value='Название  -  '+teams[checkins.index(checkin)]+'\nКапитан  -  '+captains[checkins.index(checkin)],inline=False)
                    elif checking=='0':
                        if len(numbers)>0:
                            embed.add_field(name='Команда №'+numbers[checkins.index(checkin)]+':',value='Название  -  '+teams[checkins.index(checkin)]+'\nКапитан  -  '+captains[checkins.index(checkin)],inline=False)
                        elif len(numbers)==0:
                            embed.add_field(name='Ошибка:',value='Команд пока нет')
                        elif len(numbers)>25:
                            embed2.add_field(name='Команда №'+numbers[checkins.index(checkin)]+':',value='Название  -  '+teams[checkins.index(checkin)]+'\nКапитан  -  '+captains[checkins.index(checkin)],inline=False)
                        elif len(numbers)>50:
                            embed3.add_field(name='Команда №'+numbers[checkins.index(checkin)]+':',value='Название  -  '+teams[checkins.index(checkin)]+'\nКапитан  -  '+captains[checkins.index(checkin)],inline=False)
                        elif len(numbers)>75:
                            embed4.add_field(name='Команда №'+numbers[checkins.index(checkin)]+':',value='Название  -  '+teams[checkins.index(checkin)]+'\nКапитан  -  '+captains[checkins.index(checkin)],inline=False)
                await ctx.send(embed=embed)
                if len(numbers)>25:
                    await ctx.send(embed=embed2)
                elif len(numbers)>50:
                    await ctx.send(embed=embed3)
                elif len(numbers)>75:
                    await ctx.send(embed=embed4)

@bot.command(pass_context=True)
async def team(context, *args):
    await context.message.delete()
    ctx=context
    cursor.execute("SELECT prefix FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
    info=cursor.fetchall()[0]
    prefix=str(info)[2:len(str(info))-3]
    cursor.execute("SELECT teams FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
    info=cursor.fetchall()
    if info: 
        teamsid=int(''.join(filter(str.isdigit,info.pop(0))))
    if teamsid:
        if args[0]=='create':
            if args[1]:
                if len(args[1])<=20:
                    cursor.execute("SELECT row_number() OVER() FROM teams WHERE teamname=%s",[args[1]])
                    info=cursor.fetchall()
                    if info!=[]:
                        name=str(info)[2:len(str(info))-3]
                    else:
                        name=None
                    cursor.execute("SELECT row_number() OVER() FROM teams WHERE captainid='%s'",[ctx.message.author.id])
                    info=cursor.fetchall()
                    if info!=[]:
                        captian=str(info)[2:len(str(info))-3]
                    else:
                        captian=None
                    cursor.execute("SELECT row_number() OVER() FROM teams WHERE coachid='%s'",[ctx.message.author.id])
                    info=cursor.fetchall()
                    if info!=[]:
                        coach=str(info)[2:len(str(info))-3]
                    else:
                        coach=None
                    cursor.execute("SELECT row_number() OVER() FROM teams WHERE members LIKE %s",['%'+str(ctx.message.author.id)+'%'])
                    info=cursor.fetchall()
                    if info!=[]:
                        member=str(info)[2:len(str(info))-3]
                    else:
                        member=None
                    if not captian and not name and not member and not coach:
                        cursor.execute("INSERT INTO teams(teamname, captainid, cheackin) VALUES (%s,'%s','0')",(str(args[1]),ctx.message.author.id))
                        conn.commit()
                        embed=discord.Embed(color=0x43b581,title='Команда успешно создана')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await asyncio.sleep(10)
                        if msg:
                            await msg.delete()
                    elif captian:
                        embed=discord.Embed(color=0xf04747,title='У вас уже есть команда')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await asyncio.sleep(10)
                        if msg:
                            await msg.delete()
                    elif member or coach:
                        embed=discord.Embed(color=0xf04747,title='Вы уже состоите в команде')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await asyncio.sleep(10)
                        if msg:
                            await msg.delete()
                    elif name:
                        embed=discord.Embed(color=0xf04747,title='Команда с таким названием уже существует')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await asyncio.sleep(10)
                        if msg:
                            await msg.delete()
        elif args[0]=='add':
            if args[1]:
                if args[1]=='othermembers':
                    if args[2] and args[3] and args[4] and args[5]:
                        team=[]
                        member2=discord.utils.get(ctx.guild.members,id=int(''.join(filter(str.isdigit,args[2]))))
                        if member2:
                            cursor.execute("SELECT teamname FROM teams WHERE members LIKE %s",['%'+str(member2.id)+'%'])
                            info=cursor.fetchall()
                            if info!=[]:
                                name2=str(info)[3:len(str(info))-4]
                            else:
                                name2=None
                            cursor.execute("SELECT teamname FROM teams WHERE captainid='%s'",[member2.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                captain2=str(info)[3:len(str(info))-4]
                            else:
                                captain2=None
                            cursor.execute("SELECT teamname FROM teams WHERE coachid='%s'",[member2.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                coach2=str(info)[3:len(str(info))-4]
                            else:
                                coach2=None
                            if name2==None and captain2==None and coach2==None:
                                team.append(member2.id)
                        member3=discord.utils.get(ctx.guild.members,id=int(''.join(filter(str.isdigit,args[3]))))
                        if member3:
                            cursor.execute("SELECT teamname FROM teams WHERE members LIKE %s",['%'+str(member3.id)+'%'])
                            if info!=[]:
                                name3=str(info)[3:len(str(info))-4]
                            else:
                                name3=None
                            cursor.execute("SELECT teamname FROM teams WHERE captainid='%s'",[member3.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                captain3=str(info)[3:len(str(info))-4]
                            else:
                                captain3=None
                            cursor.execute("SELECT teamname FROM teams WHERE coachid='%s'",[member3.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                coach3=str(info)[3:len(str(info))-4]
                            else:
                                coach3=None
                            if not name3 and not captain3 and not coach3:
                                team.append(member3.id)
                        member4=discord.utils.get(ctx.guild.members,id=int(''.join(filter(str.isdigit,args[4]))))
                        if member4:
                            cursor.execute("SELECT teamname FROM teams WHERE members LIKE %s",['%'+str(member4.id)+'%'])
                            info=cursor.fetchall()
                            if info!=[]:
                                name4=str(info)[3:len(str(info))-4]
                            else:
                                name4=None
                            cursor.execute("SELECT teamname FROM teams WHERE captainid='%s'",[member4.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                captain4=str(info)[3:len(str(info))-4]
                            else:
                                captain4=None
                            cursor.execute("SELECT teamname FROM teams WHERE coachid='%s'",[member4.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                coach4=str(info)[3:len(str(info))-4]
                            else:
                                coach4=None
                            if not name4 and not captain4 and not coach4:
                                team.append(member4.id)
                        member5=discord.utils.get(ctx.guild.members,id=int(''.join(filter(str.isdigit,args[5]))))
                        if member5:
                            cursor.execute("SELECT teamname FROM teams WHERE members LIKE %s",['%'+str(member5.id)+'%'])
                            info=cursor.fetchall()
                            if info!=[]:
                                name5=str(info)[3:len(str(info))-4]
                            else:
                                name5=None
                            cursor.execute("SELECT teamname FROM teams WHERE captainid='%s'",[member5.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                captain5=str(info)[3:len(str(info))-4]
                            else:
                                captain5=None
                            cursor.execute("SELECT teamname FROM teams WHERE coachid='%s'",[member5.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                coach5=str(info)[3:len(str(info))-4]
                            else:
                                coach5=None
                            if not name5 and not captain5 and not coach5:
                                team.append(member5.id)
                        if len(team)==4:
                            opt = [item for item in set(team) if team.count(item) > 1]
                            if opt==[]:
                                cursor.execute("UPDATE teams SET members=%s WHERE captainid='%s'",(str(team),ctx.message.author.id))
                                conn.commit()
                                embed=discord.Embed(color=0x43b581,title='Участники успешно добавлены в команду')
                                embed.add_field(name='Участники:',value=member2.mention+', '+member3.mention+', '+member4.mention+', '+member5.mention)
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msg=await ctx.send(embed=embed)
                                await asyncio.sleep(10)
                                if msg:
                                    await msg.delete()
                            else:
                                embed=discord.Embed(color=0xf04747,title='Найдены одинаковые пользователи')
                                for id in opt:
                                    member=discord.utils.get(ctx.guild.members,id=id)
                                    embed.add_field(name='Повторяющийся пользователь:',value=member.mention+' | `'+member.name+'#'+member.discriminator+'`')
                                embed.timestamp = discord.utils.utcnow()
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msg=await ctx.send(embed=embed)
                                await asyncio.sleep(10)
                                if msg:
                                    await msg.delete()
                        else:
                            embed=discord.Embed(color=0xf04747,title='Некоторые пользователи уже в команде')
                            if name2!=None:
                                embed.add_field(name='Пользователь:',value=member2.mention+' | `'+member2.name+'#'+member2.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=name2,inline=False)
                                embed.add_field(name='Роль в команде:',value='Участник команды')
                            elif captain2!=None:
                                embed.add_field(name='Пользователь:',value=member2.mention+' | `'+member2.name+'#'+member2.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=name2,inline=False)
                                embed.add_field(name='Роль в команде:',value='Капитан команды')
                            elif coach2!=None:
                                embed.add_field(name='Пользователь:',value=member2.mention+' | `'+member2.name+'#'+member2.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=name2,inline=False)
                                embed.add_field(name='Роль в команде:',value='Тренер команды')
                            elif name3!=None:
                                embed.add_field(name='Пользователь:',value=member3.mention+' | `'+member3.name+'#'+member3.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=name3,inline=False)
                                embed.add_field(name='Роль в команде:',value='Участник команды')
                            elif captain3!=None:
                                embed.add_field(name='Пользователь:',value=member3.mention+' | `'+member3.name+'#'+member3.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=captain3,inline=False)
                                embed.add_field(name='Роль в команде:',value='Капитан команды')
                            elif coach3!=None:
                                embed.add_field(name='Пользователь:',value=member3.mention+' | `'+member3.name+'#'+member3.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=coach3,inline=False)
                                embed.add_field(name='Роль в команде:',value='Тренер команды')
                            elif name4!=None:
                                embed.add_field(name='Пользователь:',value=member4.mention+' | `'+member4.name+'#'+member4.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=name4,inline=False)
                                embed.add_field(name='Роль в команде:',value='Участник команды')
                            elif captain4!=None:
                                embed.add_field(name='Пользователь:',value=member4.mention+' | `'+member4.name+'#'+member4.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=captain4,inline=False)
                                embed.add_field(name='Роль в команде:',value='Капитан команды')
                            elif coach4!=None:
                                embed.add_field(name='Пользователь:',value=member4.mention+' | `'+member4.name+'#'+member4.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=coach4,inline=False)
                                embed.add_field(name='Роль в команде:',value='Тренер команды')
                            elif name5!=None:
                                embed.add_field(name='Пользователь:',value=member5.mention+' | `'+member5.name+'#'+member5.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=name5,inline=False)
                                embed.add_field(name='Роль в команде:',value='Участник команды')
                            elif captain5!=None:
                                embed.add_field(name='Пользователь:',value=member5.mention+' | `'+member5.name+'#'+member5.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=captain5,inline=False)
                                embed.add_field(name='Роль в команде:',value='Капитан команды')
                            elif coach5!=None:
                                embed.add_field(name='Пользователь:',value=member5.mention+' | `'+member5.name+'#'+member5.discriminator+'`',inline=True)
                                embed.add_field(name='Команда:',value=coach5,inline=False)
                                embed.add_field(name='Роль в команде:',value='Тренер команды')
                            embed.timestamp = discord.utils.utcnow()
                            embed.set_footer(text='Автоматическое удаление через 15 секунд')
                            msg=await ctx.send(embed=embed)
                            await msg.delete(delay=15.0)
                    else:
                        embed=discord.Embed(color=0xf04747,title='Не все пользователи написаны')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await msg.delete(delay=10.0)
                elif args[1]=='member':
                    if args[2]:
                        member=discord.utils.get(ctx.guild.members,id=int(''.join(filter(str.isdigit,args[2]))))
                        if member:
                            cursor.execute("SELECT members FROM teams WHERE captainid='%s'",[ctx.message.author.id])
                            info=cursor.fetchall()[0]
                            if len(str(info))>7:
                                members=(str(info)[3:len(str(info))-4]).split(',')
                            else:
                                members=[]
                            for i in members:
                                members[members.index(i)]=int(members[members.index(i)])
                            cursor.execute("SELECT row_number() OVER() FROM teams WHERE members LIKE %s",['%'+str(member.id)+'%'])
                            info=cursor.fetchall()
                            if info!=[]:
                                mem=str(info)[2:len(str(info))-3]
                            else:
                                mem=None
                            cursor.execute("SELECT row_number() OVER() FROM teams WHERE captainid='%s'",[member.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                captian=str(info)[2:len(str(info))-3]
                            else:
                                captian=None
                            cursor.execute("SELECT row_number() OVER() FROM teams WHERE coachid='%s'",[member.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                coach=str(info)[2:len(str(info))-3]
                            else:
                                coach=None
                            if member.id not in members and len(members)!=4 and not mem and not captian and not coach:
                                members.append(member.id)
                                cursor.execute("UPDATE teams SET members=%s WHERE captainid='%s'",(str(members),ctx.message.author.id))
                                conn.commit()
                                embed=discord.Embed(color=0x43b581,title='Пользователь успешно добавлен в команду')
                                mem=[]
                                for id in members:
                                    member=discord.utils.get(ctx.guild.members,id=id)
                                    mem.append(member.mention)
                                embed.add_field(name='Список участников:',value=', '.join(mem),inline=False)
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msg=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                            elif member.id in members:
                                embed=discord.Embed(color=0xf04747,title='Пользователь уже состоит в вашей команде')
                                mem=[]
                                for id in members:
                                    member=discord.utils.get(ctx.guild.members,id=id)
                                    mem.append(member.mention)
                                embed.add_field(name='Список участников:',value=', '.join(mem),inline=False)
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msg=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                            elif captian:
                                embed=discord.Embed(color=0xf04747,title='У пользователя есть команда')
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msg=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                            elif mem or coach:
                                embed=discord.Embed(color=0xf04747,title='Пользователь уже состоит в команде')
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msg=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                            elif len(member)==4:
                                embed=discord.Embed(color=0xf04747,title='В вашей команде уже полный состав')
                                mem=[]
                                for id in members:
                                    member=discord.utils.get(ctx.guild.members,id=id)
                                    mem.append(member.mention)
                                embed.add_field(name='Список участников:',value=', '.join(mem),inline=False)
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msg=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                    else:
                        embed=discord.Embed(color=0xf04747,title='Вы не написали пользователя')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await msg.delete(delay=10.0)
                elif args[1]=='coach':
                    if args[2]:
                        member=discord.utils.get(ctx.guild.members,id=int(''.join(filter(str.isdigit,args[2]))))
                        if member:
                            cursor.execute("SELECT row_number() OVER() FROM teams WHERE members LIKE %s",['%'+str(member.id)+'%'])
                            info=cursor.fetchall()
                            if info!=[]:
                                mem=str(info)[2:len(str(info))-3]
                            else:
                                mem=None
                            cursor.execute("SELECT row_number() OVER() FROM teams WHERE captainid='%s'",[member.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                captian=str(info)[2:len(str(info))-3]
                            else:
                                captian=None
                            cursor.execute("SELECT row_number() OVER() FROM teams WHERE coachid='%s'",[member.id])
                            info=cursor.fetchall()
                            if info!=[]:
                                coach=str(info)[2:len(str(info))-3]
                            else:
                                coach=None
                            if not mem and not captian and not coach:
                                cursor.execute("UPDATE teams SET coachid='%s' WHERE captainid='%s'",(member.id,ctx.message.author.id))
                                conn.commit()
                                embed=discord.Embed(color=0x43b581,title='Тренер успешно добавлен в команду')
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msgs=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                            elif captian:
                                embed=discord.Embed(color=0xf04747,title='У пользователя есть команда')
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msga=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                            elif mem or coach:
                                embed=discord.Embed(color=0xf04747,title='Пользователь уже состоит в команде')
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msgx=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                    else:
                        embed=discord.Embed(color=0xf04747,title='Вы не написали пользователя')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await msg.delete(delay=10.0)
        elif args[0]=='remove':
            if args[1]:
                if args[1]=='member':
                    if args[2]:
                        member=discord.utils.get(ctx.guild.members,id=int(''.join(filter(str.isdigit,args[2]))))
                        if member:
                            cursor.execute("SELECT members FROM teams WHERE captainid='%s'",[ctx.message.author.id])
                            info=cursor.fetchall()[0]
                            if len(str(info))>7:
                                members=(str(info)[3:len(str(info))-4]).split(',')
                            for i in members:
                                members[members.index(i)]=int(members[members.index(i)])
                            if member.id in members:
                                embed=discord.Embed(color=0x43b581,title='Участник успешно кикнут из команды')
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msgs=await ctx.send(embed=embed)
                                members.remove(member.id)
                                cursor.execute("UPDATE teams SET members=%s WHERE captainid='%s'",(str(members),ctx.message.author.id))
                                conn.commit()
                                await msg.delete(delay=10.0)
                            else:
                                embed=discord.Embed(color=0xf04747,title='Пользователь не в вашей команде')
                                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                                msgx=await ctx.send(embed=embed)
                                await msg.delete(delay=10.0)
                elif args[1]=='coach':
                    cursor.execute("SELECT coachid FROM teams WHERE captainid='%s'",[ctx.message.author.id])
                    info=cursor.fetchall()
                    if len(str(info))>10:
                        cursor.execute("UPDATE teams SET coachid=0 WHERE captainid='%s'",[ctx.message.author.id])
                        conn.commit()
                        embed=discord.Embed(color=0x43b581,title='Тренер успешно кикнут из команды')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msgs=await ctx.send(embed=embed)
                        await msg.delete(delay=10.0)
                    else:
                        embed=discord.Embed(color=0xf04747,title='В вашей команде нет тренера')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msgx=await ctx.send(embed=embed)
                        await msg.delete(delay=10.0)
        elif args[0]=='checkin':
            cursor.execute("SELECT checkin FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
            info=cursor.fetchall()
            checkin=str(info)[3:len(str(info))-4]
            if checkin=='1':
                cursor.execute("SELECT members FROM teams WHERE captainid='%s'",[ctx.message.author.id])
                info=cursor.fetchall()[0]
                membersid=[]
                if len(str(info))>7:
                    membersid=(str(info)[3:len(str(info))-4]).split(',')
                for i in membersid:
                    membersid[membersid.index(i)]=int(membersid[membersid.index(i)])
                if len(membersid)==4:
                    members=[]
                    off=[]
                    for id in membersid:
                        member=discord.utils.get(ctx.guild.members,id=id)
                        if member.status is not discord.Status.offline:
                            members.append(member)
                        else:
                            off.append(member.mention)
                    if len(members)==4:
                        cursor.execute("UPDATE teams SET cheackin='1' WHERE captainid='%s'",[ctx.message.author.id])
                        conn.commit()
                        audit=discord.utils.get(ctx.guild.text_channels,name='журнал-команд')
                        embed=discord.Embed(color=0x43b581,title='Команда успешно прошла чек-ин')
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await msg.delete(delay=10.0)
                    else:
                        embed=discord.Embed(color=0xf04747,title='Команда не прошла чек-ин')
                        embed.add_field(name='Пользователи оффлайн:',value=', '.join(off))
                        embed.set_footer(text='Автоматическое удаление через 10 секунд')
                        msg=await ctx.send(embed=embed)
                        await msg.delete(delay=10.0)
                else:
                    embed=discord.Embed(color=0xf04747,title='В команде не полный состав')
                    embed.set_footer(text='Автоматическое удаление через 10 секунд')
                    msg=await ctx.send(embed=embed)
                    await msg.delete(delay=10.0)
            else:
                embed=discord.Embed(color=0xf04747,title='Чек-ин не был активирован')
                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                msg=await ctx.send(embed=embed)
                await msg.delete(delay=10.0)
        elif args[0]=='leave':
            cursor.execute("SELECT members FROM teams WHERE members LIKE %s",['%'+str(ctx.message.author.id)+'%'])
            info=cursor.fetchall()
            if len(str(info))>7:
                members=(str(info)[4:len(str(info))-5]).split(',')
                for i in members:
                    members[members.index(i)]=int(members[members.index(i)])
            else:
                members=[]
            cursor.execute("SELECT teamname FROM teams WHERE coachid='%s'",[ctx.message.author.id])
            info=cursor.fetchall()
            if len(str(info))>7:
                cursor.execute("UPDATE teams SET coachid=0 WHERE coachid='%s'",[ctx.message.author.id])
                conn.commit()
                embed=discord.Embed(color=0x43b581,title='Вы успешно вышли из команды')
                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                msgs=await ctx.send(embed=embed)
                await msg.delete(delay=10.0)
            elif members and ctx.message.author.id in members:
                members.remove(ctx.message.author.id)
                cursor.execute("UPDATE teams SET members=%s WHERE members LIKE %s",(str(members),'%'+str(ctx.message.author.id)+'%'))
                conn.commit()
                embed=discord.Embed(color=0x43b581,title='Вы успешно вышли из команды')
                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                msgs=await ctx.send(embed=embed)
                await msg.delete(delay=10.0)
            else:
                embed=discord.Embed(color=0xf04747,title='Вы не можете выйти из команды')
                embed.set_footer(text='Автоматическое удаление через 10 секунд')
                msgx=await ctx.send(embed=embed)
                await msg.delete(delay=10.0)
        elif args[0]=='disband':
            cursor.execute("DELETE FROM teams WHERE captainid='%s'",[ctx.message.author.id])
            conn.commit()
            embed=discord.Embed(color=0x43b581,title='Команда расформирована')
            embed.set_footer(text='Автоматическое удаление через 10 секунд')
            msgs=await ctx.send(embed=embed)
            await msg.delete(delay=10.0)
        elif args[0]=='info':
            if args[1]:
                member=await ctx.guild.fetch_member(int(''.join(filter(str.isdigit,args[1]))))
                if member:
                    cursor.execute("SELECT row_number() OVER(), teamname, captainid, coachid FROM teams WHERE captainid='%s'",[member.id])
                    captian=cursor.fetchall()
                    cursor.execute("SELECT row_number() OVER(), teamname, captainid, coachid FROM teams WHERE coachid='%s'",[member.id])
                    coach=cursor.fetchall()
                    cursor.execute("SELECT row_number() OVER(), teamname, captainid, coachid FROM teams WHERE members LIKE %s",['%'+str(member.id)+'%'])
                    members=cursor.fetchall()
                else:
                    cursor.execute("SELECT row_number() OVER(), teamname, captianid, coachid FROM teams WHERE teamname='%s'",[args[1]])
                    info=cursor.fetchall()
                if captian!=[]:
                    result=captian
                elif coach!=[]:
                    result=coach
                elif members!=[]:
                    result=members
                elif info!=[]:
                    result=info
                else:
                    result=None
                if result:
                    members=[]
                    result=str(result)[2:len(str(result))-2].split(", ")
                    embed=discord.Embed(color=0x808080,title='Информация о команде '+str(result[1])[1:len(str(result[1]))-1])
                    captian=await ctx.guild.fetch_member((result[2])[1:len(str(result[2]))-1])
                    cursor.execute("SELECT members FROM teams WHERE captainid='%s'",[captian.id])
                    info=cursor.fetchall()
                    ids=str(info)[4:len(str(info))-5].split(", ")
                    for di in ids:
                        member=await ctx.guild.fetch_member(di)
                        members.append(member.mention)
                    embed.add_field(name='Капитан команды:',value=captian.mention)
                    if members!=[]:
                        embed.add_field(name='Участники команды:',value=', '.join(members),inline=False)
                    embed.add_field(name='Порядок регистрации:',value=result[0],inline=False)
                    embed.set_footer(text='Автоматическое удаление через 30 секунд')
                    msg=await ctx.send(embed=embed)
                    await msg.delete(delay=30.0)

@bot.command(pass_context=True)
async def mute(ctx, *args):
    await ctx.message.delete()
    cursor.execute("SELECT modrole FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
    roleid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    role=discord.utils.get(ctx.guild.roles,id=roleid)
    if role in ctx.message.author.roles or ctx.message.author.guild_permissions.administrator==True:
        if args[0]:
            if args[1]:
                member=discord.utils.get(ctx.guild.members,id=(int(''.join(filter(str.isdigit,args[0])))))
                if role not in member.roles and member.guild_permissions.administrator==False:
                    if member.voice and member.voice.mute==False:
                        await member.edit(mute=True)
                        cursor.execute("SELECT modchan FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                        chanid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
                        channel=discord.utils.get(ctx.guild.text_channels,id=chanid)
                        embed=discord.Embed(color=0xf04747)
                        embed.timestamp = discord.utils.utcnow()
                        embed.set_author(name='Пользователю отключили микрофон',icon_url='https://i.ibb.co/KFGkScK/give-mute.png')
                        embed.add_field(name='Пользователь:',value=member.mention+' | `'+member.name+'#'+member.discriminator+'`',inline=False)
                        embed.add_field(name='Модератор:',value=ctx.message.author.mention+' | `'+ctx.message.author.name+'#'+ctx.message.author.discriminator+'`',inline=False)
                        reason=[]
                        for arg in args[1:]:
                            reason.append(str(arg)[1:len(str(arg))-1])
                        embed.add_field(name='Причина:',value=' '.join(reason),inline=False)
                        embed.set_thumbnail(url=ctx.message.author.avatar_url)
                        await channel.send(embed=embed)
                    elif not member.voice:
                        enable=discord.Embed(color=0x808080,title='Пользователь не подключен к каналу')
                        enable.timestamp = discord.utils.utcnow()
                        enable.set_footer(text='Автоматическое удаление через 3 секунд')
                        msg=await ctx.send(embed=enable)
                        await msg.delete(delay=3.0)
                    else:
                        enable=discord.Embed(color=0x808080,title='Пользователь уже замучен')
                        enable.timestamp = discord.utils.utcnow()
                        enable.set_footer(text='Автоматическое удаление через 3 секунд')
                        msg=await ctx.send(embed=enable)
                        await msg.delete(delay=3.0)
                else:
                    enable=discord.Embed(color=0x808080,title='Вы не написали причину')
                    enable.timestamp = discord.utils.utcnow()
                    enable.set_footer(text='Автоматическое удаление через 3 секунд')
                    msg=await ctx.send(embed=enable)
                    await msg.delete(delay=3.0)
        else:
            enable=discord.Embed(color=0x808080,title='Вы не выделили участника')
            enable.timestamp = discord.utils.utcnow()
            enable.set_footer(text='Автоматическое удаление через 3 секунд')
            msg=await ctx.send(embed=enable)
            await msg.delete(delay=3.0)
    else:
        enable=discord.Embed(color=0x808080,title='У вас нет прав')
        enable.timestamp = discord.utils.utcnow()
        enable.set_footer(text='Автоматическое удаление через 3 секунд')
        msg=await ctx.send(embed=enable)
        await msg.delete(delay=3.0)
                
@bot.command(pass_context=True)
async def unmute(ctx, *args):
    await ctx.message.delete()
    cursor.execute("SELECT modrole FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
    roleid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    role=discord.utils.get(ctx.guild.roles,id=roleid)
    if role in ctx.message.author.roles or ctx.message.author.guild_permissions.administrator==True:
        if args[0]:
            member=discord.utils.get(ctx.guild.members,id=(int(''.join(filter(str.isdigit,args[0])))))
            if role not in member.roles and member.guild_permissions.administrator==False:
                if member.voice and member.voice.mute==True:
                    await member.edit(mute=False)
                    cursor.execute("SELECT modchan FROM guildsinfo WHERE guildid='%s'",[ctx.guild.id])
                    chanid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
                    channel=discord.utils.get(ctx.guild.text_channels,id=chanid)
                    embed=discord.Embed(color=0xf04747)
                    embed.timestamp = discord.utils.utcnow()
                    embed.set_author(name='Пользователю отключили микрофон',icon_url='https://i.ibb.co/KFGkScK/give-mute.png')
                    embed.add_field(name='Пользователь:',value=member.mention+' | `'+member.name+'#'+member.discriminator+'`',inline=False)
                    embed.add_field(name='Модератор:',value=ctx.message.author.mention+' | `'+ctx.message.author.name+'#'+ctx.message.author.discriminator+'`',inline=False)
                    reason=[]
                    for arg in args[1:]:
                        reason.append(str(arg)[1:len(str(arg))-1])
                    embed.add_field(name='Причина:',value=' '.join(reason),inline=False)
                    embed.set_thumbnail(url=ctx.message.author.avatar_url)
                    await channel.send(embed=embed)
                elif not member.voice:
                    enable=discord.Embed(color=0x808080,title='Пользователь не подключен к каналу')
                    enable.timestamp = discord.utils.utcnow()
                    enable.set_footer(text='Автоматическое удаление через 3 секунд')
                    msg=await ctx.send(embed=enable)
                    await msg.delete(delay=3.0)
                else:
                    enable=discord.Embed(color=0x808080,title='Пользователь уже размучен')
                    enable.timestamp = discord.utils.utcnow()
                    enable.set_footer(text='Автоматическое удаление через 3 секунд')
                    msg=await ctx.send(embed=enable)
                    await msg.delete(delay=3.0)
        else:
            enable=discord.Embed(color=0x808080,title='Вы не выделили участника')
            enable.timestamp = discord.utils.utcnow()
            enable.set_footer(text='Автоматическое удаление через 3 секунд')
            msg=await ctx.send(embed=enable)
            await msg.delete(delay=3.0)
    else:
        enable=discord.Embed(color=0x808080,title='У вас нет прав')
        enable.timestamp = discord.utils.utcnow()
        enable.set_footer(text='Автоматическое удаление через 3 секунд')
        msg=await ctx.send(embed=enable)
        await msg.delete(delay=3.0)

@bot.command()
async def test(ctx: commands.Context):
    await ctx.send(content='test', view=RoomsControl(892783747483725876))
"""

@bot.event
async def on_raw_reaction_add(pay : discord.RawReactionActionEvent):
    await AuditLogging(bot.get_guild(pay.guild_id)).edit_emoji(pay)

@bot.event
async def on_raw_reaction_remove(pay : discord.RawReactionActionEvent):
    await AuditLogging(bot.get_guild(pay.guild_id)).edit_emoji(pay)

@bot.event
async def on_member_update(beforemem:discord.Member,aftermem:discord.Member):
    await AuditLogging(beforemem.guild).member_update(beforemem,aftermem)

@bot.event
async def on_member_join(mem : discord.Member):
    await AuditLogging(mem.guild).new_member(mem)

'''@bot.event
async def on_raw_message_edit(pay):
    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[pay.guild_id])
    auditlogid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    if not pay.cached_message and auditlogid!=0:
        guild=discord.utils.get(bot.guilds,id=pay.guild_id)
        author=discord.utils.get(guild.members,id=int(pay.data['author']['id']))
        bot=bot.get_user(713831247285190726)
        if author!=bot:
            embed=discord.Embed(color=0xfaa61a)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Сообщение изменено(Сообщение не в памяти)',icon_url='https://i.ibb.co/rbcDcyW/edit-msg.png')
            channel=discord.utils.get(guild.text_channels,id=pay.channel_id)
            embed.add_field(name='Канал:',value=channel.mention)
            embed.add_field(name='Автор:',value=author.mention+' | `'+author.name+'#'+author.discriminator+'`')
            embed.set_thumbnail(url=author.avatar_url)
            embed.add_field(name='Старое сообщение:',value='Не удалось получить данные',inline=False) 
            embed.add_field(name='Новое сообщение:',value='> '+pay.data['content'],inline=False)
            msg=await channel.fetch_message(pay.message_id)
            embed.add_field(name='Ссылка на сообщение',value='[Перейти]('+msg.jump_url+')')
            channel = discord.utils.get(guild.text_channels, id=auditlogid)
            await channel.send(embed=embed)

@bot.event
async def on_message_edit(be,af):
    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[be.guild.id])
    auditlogid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    if auditlogid!=0:
        bot=bot.get_user(713831247285190726)
        if be.content!=af.content and be.author!=bot:
            embed=discord.Embed(color=0xfaa61a)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Сообщение изменено',icon_url='https://i.ibb.co/rbcDcyW/edit-msg.png')
            embed.add_field(name='Канал:',value=af.channel.mention)
            embed.add_field(name='Автор:',value=af.author.mention+' | `'+af.author.name+'#'+af.author.discriminator+'`')
            embed.set_thumbnail(url=af.author.avatar_url)
            embed.add_field(name='Старое сообщение:',value='> '+be.content,inline=False)
            embed.add_field(name='Новое сообщение:',value='> '+af.content,inline=False)
            embed.add_field(name='Ссылка на сообщение',value='[Перейти]('+af.jump_url+')')
            channel = discord.utils.get(be.guild.channels, id=auditlogid)
            await channel.send(embed=embed)
        if be.pinned!=af.pinned:
            if be.pinned==False:
                embed=discord.Embed(color=0xfaa61a)
                embed.timestamp = discord.utils.utcnow()
                embed.set_author(name='Сообщение закрепили',icon_url='https://i.ibb.co/rbcDcyW/edit-msg.png')
                embed.add_field(name='Канал:',value=af.channel.mention)
                embed.add_field(name='Автор:',value=af.author.mention+' | `'+af.author.name+'#'+af.author.discriminator+'`')
                embed.set_thumbnail(url=af.author.avatar_url)
                if be.embeds==[]:
                    embed.add_field(name='Cообщение:',value='> '+be.content,inline=False)
                else:
                    embed.add_field(name='Cообщение:',value='сообщение со вставкой',inline=False)
                embed.add_field(name='Ссылка на сообщение',value='[Перейти]('+af.jump_url+')')
                async for audits in be.guild.audit_logs(action=discord.AuditLogAction.message_pin,limit=1):
                    if (discord.utils.utcnow()-audits.created_at).seconds//60<1:
                        embed.set_thumbnail(url=audits.user.avatar_url)
                        embed.add_field(name='Модератор:',value=format(audits.user.mention)+' | `'+format(audits.user.name)+'#'+format(audits.user.discriminator)+'`',inline=False)
                        channel = discord.utils.get(be.guild.channels, id=auditlogid)
                        await channel.send(embed=embed)
            else:
                embed=discord.Embed(color=0xfaa61a)
                embed.timestamp = discord.utils.utcnow()
                embed.set_author(name='Сообщение открепили',icon_url='https://i.ibb.co/rbcDcyW/edit-msg.png')
                embed.add_field(name='Канал:',value=af.channel.mention)
                embed.add_field(name='Автор:',value=af.author.mention+' | `'+af.author.name+'#'+af.author.discriminator+'`')
                embed.set_thumbnail(url=af.author.avatar_url)
                if be.embeds==[]:
                    embed.add_field(name='Cообщение:',value='> '+be.content,inline=False)
                else:
                    embed.add_field(name='Cообщение:',value='Сообщение со вставкой',inline=False)
                embed.add_field(name='Ссылка на сообщение',value='[Перейти]('+af.jump_url+')')
                async for audits in be.guild.audit_logs(action=discord.AuditLogAction.message_unpin,limit=1):
                    if (discord.utils.utcnow()-audits.created_at).seconds//60<1:
                        embed.set_thumbnail(url=audits.user.avatar_url)
                        embed.add_field(name='Модератор:',value=format(audits.user.mention)+' | `'+format(audits.user.name)+'#'+format(audits.user.discriminator)+'`',inline=False)
                        channel = discord.utils.get(be.guild.channels, id=auditlogid)
                        await channel.send(embed=embed)'''

@bot.event
async def on_message_delete(message):
    pass


@bot.event
async def on_member_remove(mem : discord.Member):
    auditlog = AuditLog(mem.guild.id).chan
    if auditlog:
        await AuditLogging(mem.guild).member_leave(mem)


@bot.event
async def on_member_ban(g : discord.Guild, user : discord.User):
    auditlog = AuditLog(g.id).chan
    if auditlog:
        await AuditLogging(g).member_ban(user)

@bot.event
async def on_member_unban(g : discord.Guild, user : discord.User):
    auditlog = AuditLog(g.id).chan
    if auditlog:
        await AuditLogging(g).member_unban(user)

@bot.event
async def on_guild_update(be : discord.Guild, af : discord.Guild):
    auditlog = AuditLog(af.id).chan
    if auditlog:
        await AuditLogging(af).guild_update(be, af)
    
@bot.event
async def on_guild_role_create(role : discord.Role):
    auditlog = AuditLog(role.guild.id).chan
    if auditlog:
        await AuditLogging(role.guild).guild_role_create(role)

@bot.event
async def on_guild_role_delete(role: discord.Role):
    auditlog = AuditLog(role.guild.id).chan
    if auditlog:
        await AuditLogging(role.guild).guild_role_delete(role)

@bot.event
async def on_guild_role_update(be : discord.Role, af : discord.Role):
    auditlog = AuditLog(be.guild.id).chan
    if auditlog:
        await AuditLogging(be.guild).guild_role_update(be, af)
        
"""@bot.event
async def on_raw_reaction_add(pay):
    cursor=conn.cursor()
    guild=bot.get_guild(pay.guild_id)
    mem=await guild.fetch_member(pay.user_id)
    chan=guild.get_channel(pay.channel_id)
    msg=await chan.fetch_message(pay.message_id)
    cursor.execute("SELECT musicbot FROM guildsinfo WHERE guildid='%s'",[guild.id])
    musicbot=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    cursor.execute("SELECT rooms FROM guildsinfo WHERE guildid='%s'",[guild.id])
    rooms=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    bot=bot.get_user(713831247285190726)
    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[pay.guild_id])
    info=cursor.fetchall()
    if info:
        auditlogid=int(''.join(filter(str.isdigit,info.pop(0))))
    cursor.execute("SELECT roleid FROM emojirole WHERE msgid='%s'",[pay.message_id])
    info=cursor.fetchall()
    if info:
        roleid=int(''.join(filter(str.isdigit,info.pop(0))))
        cursor.execute("SELECT roleid FROM emojirole WHERE emojiid='%s'",[pay.emoji.id])
        info=cursor.fetchall()
        if info:
            roleid=int(''.join(filter(str.isdigit,info.pop(0))))
            role=discord.utils.get(guild.roles,id=roleid)
            if mem!=bot:
                await mem.add_roles(role)
    if auditlogid!=0:
        if pay.member==guild.owner:
            embed=discord.Embed(color=0x43b581)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Создатель поставил реакцию',icon_url='https://i.ibb.co/Fsk4K5H/add-react.png')
            embed.add_field(name='Сообщение:',value='> '+msg.content+'\n'+'|[Перейти]('+msg.jump_url+')')
            embed.add_field(name='Реакия:',value=pay.emoji)
            embed.set_thumbnail(url=pay.member.avatar_url)
            channel = discord.utils.get(pay.member.guild.channels, id=auditlogid)
            await channel.send(embed=embed)

        elif pay.member.guild_permissions.administrator==True:
            embed=discord.Embed(color=0x43b581)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Администратор поставил реакцию',icon_url='https://i.ibb.co/Fsk4K5H/add-react.png')
            embed.add_field(name='Сообщение:',value='> '+msg.content+'\n'+'|[Перейти]('+msg.jump_url+')')
            embed.add_field(name='Администратор:',value=pay.member.mention+' | `'+pay.member.name+'#'+pay.member.discriminator+'`',inline=False)
            embed.set_thumbnail(url=pay.member.avatar_url)
            embed.add_field(name='Реакия:',value=pay.emoji,inline=False)
            channel = discord.utils.get(pay.member.guild.channels, id=auditlogid)
            await channel.send(embed=embed)
                
        elif pay.user_id!=bot.id:
            embed=discord.Embed(color=0x43b581)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Пользователь поставил реакцию',icon_url='https://i.ibb.co/Fsk4K5H/add-react.png')
            embed.add_field(name='Сообщение:',value='> '+msg.content+'\n'+'|[Перейти]('+msg.jump_url+')')
            embed.add_field(name='Пользователь:',value=pay.member.mention+' | `'+pay.member.name+'#'+pay.member.discriminator+'`',inline=False)
            embed.set_thumbnail(url=pay.member.avatar_url)
            embed.add_field(name='Реакия:',value=pay.emoji)
            channel = discord.utils.get(pay.member.guild.channels, id=auditlogid)
            await channel.send(embed=embed)"""

"""@bot.event   
async def on_guild_channel_update(be,af):
    cursor=conn.cursor()
    cursor.execute("SELECT createid FROM guildsinfo WHERE guildid='%s'",[be.guild.id])
    rooms=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    if rooms!=0: 
        cre=discord.utils.get(af.guild.voice_channels,id=rooms)
        cat=cre.category
        if af.name!=be.name and af.category==cat and be.category==cat:  # Переименование комнаты
            cursor.execute("SELECT roomid FROM rooms WHERE roomname =%s",[af.name])
            if cursor.fetchall()!=[]:
                cursor.execute("SELECT consoleid FROM rooms WHERE roomid='%s'",[af.id])
                consoleid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
                consol=discord.utils.get(af.guild.text_channels,id=consoleid)
                embed=discord.Embed(color=0xf04747,title='Не удалось переименовать комнату')
                embed.add_field(name='Причина:',value='Новое имя имеется у другой комнаты')
                await consol.send(embed=embed)
                await af.edit(name=be.name)
            else:
                for role in be.guild.roles:
                    if role.name==be.name:
                        await role.edit(name=af.name)
                cursor.execute("UPDATE rooms SET roomname=%s WHERE roomid='%s'",[af.name,af.id])
                conn.commit()
                cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[be.guild.id])
                auditlogid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
                if auditlogid!=0:
                    embed=discord.Embed(color=0xfaa61a)
                    embed.timestamp = discord.utils.utcnow()
                    embed.set_author(name='Комната переименованна',icon_url='https://i.ibb.co/Xb23bPG/room-edit.png')
                    embed.add_field(name='Старое название:',value=be.name)
                    embed.add_field(name='Новое:',value=af.name)
                    async for audits in be.guild.audit_logs(limit=1,action=discord.AuditLogAction.channel_update):
                        embed.add_field(name='Модератор:',value=format(audits.user.mention)+' | `'+format(audits.user.name)+'#'+format(audits.user.discriminator)+'`',inline=False)
                        embed.set_thumbnail(url=audits.user.avatar_url)
                        channel = discord.utils.get(be.guild.channels, id=auditlogid)
                        await channel.send(embed=embed)
    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[be.guild.id])
    auditlogid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    if auditlogid!=0:
        if be.name!=af.name and ((rooms!=0 and af.category!=cat and be.category!=cat) or rooms==0):
            embed=discord.Embed(color=0xfaa61a)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Канал переименован',icon_url='https://i.ibb.co/Xb23bPG/room-edit.png')
            embed.add_field(name='Категория:',value=af.category.name)
            embed.add_field(name='Старое название:',value=be.name)
            embed.add_field(name='Новое:',value=af.name)
            async for audits in be.guild.audit_logs(limit=1,action=discord.AuditLogAction.channel_update):
                embed.add_field(name='Модератор:',value=format(audits.user.mention)+' | `'+format(audits.user.name)+'#'+format(audits.user.discriminator)+'`',inline=False)
                embed.set_thumbnail(url=audits.user.avatar_url)
                channel = discord.utils.get(be.guild.channels, id=auditlogid)
                await channel.send(embed=embed)
        try:
            if rooms!=0:
                if af.bitrate!=be.bitrate and af.category==cat and be.category==cat:
                    embed=discord.Embed(color=0xfaa61a)
                    embed.timestamp = discord.utils.utcnow()
                    embed.set_author(name='Битрейт комнаты изменен',icon_url='https://i.ibb.co/Xb23bPG/room-edit.png')
                    embed.add_field(name='Комната:',value=af.name)
                    embed.add_field(name='Старый битрейт:',value=str(int(be.bitrate/1000))+' кб/c',inline=False)
                    embed.add_field(name='Новый битрейт:',value=str(int(af.bitrate/1000))+' кб/c',inline=True)
                    async for audits in be.guild.audit_logs(limit=1,action=discord.AuditLogAction.channel_update):
                        embed.add_field(name='Модератор:',value=format(audits.user.mention)+' | `'+format(audits.user.name)+'#'+format(audits.user.discriminator)+'`',inline=False)
                        embed.set_thumbnail(url=audits.user.avatar_url)
                        channel = discord.utils.get(be.guild.channels, id=auditlogid)
                        await channel.send(embed=embed)
            if af.bitrate!=be.bitrate and ((rooms!=0 and af.category!=cat and be.category!=cat) or rooms==0):
                embed=discord.Embed(color=0xfaa61a)
                embed.timestamp = discord.utils.utcnow()
                embed.set_author(name='Битрейт канала изменен',icon_url='https://i.ibb.co/Xb23bPG/room-edit.png')
                embed.add_field(name='Категория:',value=af.category.name)
                embed.add_field(name='Канал:',value=af.name)
                embed.add_field(name='Старый битрейт:',value=str(int(be.bitrate/1000))+' кб/c',inline=False)
                embed.add_field(name='Новый битрейт :',value=str(int(af.bitrate/1000))+' кб/c',inline=True)
                async for audits in be.guild.audit_logs(limit=1,action=discord.AuditLogAction.channel_update):
                    embed.add_field(name='Модератор:',value=format(audits.user.mention)+' | `'+format(audits.user.name)+'#'+format(audits.user.discriminator)+'`',inline=False)
                    embed.set_thumbnail(url=audits.user.avatar_url)
                    channel = discord.utils.get(be.guild.channels, id=auditlogid)
                    await channel.send(embed=embed)
        except AttributeError:
            pass

@bot.event
async def on_thread_join(t):
    cursor=conn.cursor()
    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[t.guild.id])
    info=cursor.fetchall()[0]
    auditlogid=int(str(info)[2:len(str(info))-3])
    if auditlogid!=0:
        embed=discord.Embed(color=0x43b581)
        bot=t.guild.get_member(713831247285190726)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name='Ветка создана',icon_url='https://i.ibb.co/McPDpM3/create-msg.png')
        async for audits in t.guild.audit_logs(limit=1,action=discord.AuditLogAction.thread_create):
            if audits.user!=bot and (datetime.now(timezone.utc)-audits.created_at).seconds//60<1:
                embed.add_field(name='Модератор:',value=format(audits.user.mention)+' | `'+format(audits.user.name)+'#'+format(audits.user.discriminator)+'`')
                embed.set_thumbnail(url=audits.user.avatar_url)
                channel = discord.utils.get(t.guild.channels, id=auditlogid)
                await channel.send(embed=embed)

@bot.event
async def on_raw_reaction_remove(pay):
    cursor=conn.cursor()
    guild=bot.get_guild(pay.guild_id)
    chan=guild.get_channel(pay.channel_id)
    msg=await chan.fetch_message(pay.message_id)
    cursor.execute("SELECT musicbot FROM guildsinfo WHERE guildid='%s'",[guild.id])
    musicbot=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    cursor.execute("SELECT rooms FROM guildsinfo WHERE guildid='%s'",[guild.id])
    rooms=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    bot=bot.get_user(713831247285190726)
    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[pay.guild_id])
    auditlogid=int(''.join(filter(str.isdigit,cursor.fetchall().pop(0))))
    guild=discord.utils.get(bot.guilds,id=pay.guild_id)
    member=guild.get_member(pay.user_id)
    mem=await guild.fetch_member(pay.user_id)
    bot=bot.get_user(713831247285190726)
    cursor.execute("SELECT auditlogid FROM guildsinfo WHERE guildid='%s'",[pay.guild_id])
    info=cursor.fetchall()
    if info:
        auditlogid=int(''.join(filter(str.isdigit,info.pop(0))))
    cursor.execute("SELECT roleid FROM emojirole WHERE msgid='%s'",[pay.message_id])
    info=cursor.fetchall()
    if info:
        roleid=int(''.join(filter(str.isdigit,info.pop(0))))
        cursor.execute("SELECT roleid FROM emojirole WHERE emojiid='%s'",[pay.emoji.id])
        info=cursor.fetchall()
        if info:
            roleid=int(''.join(filter(str.isdigit,info.pop(0))))
            role=discord.utils.get(guild.roles,id=roleid)
            if mem!=bot:
                await mem.remove_roles(role)
    if auditlogid!=0:
        if member==guild.owner:
            embed=discord.Embed(color=0xf04747)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Создател убрал реакцию',icon_url='https://i.ibb.co/wy9P1wJ/remove-react.png')
            embed.add_field(name='Сообщение:',value='> '+msg.content+'\n'+'|[Перейти]('+msg.jump_url+')')
            embed.add_field(name='Автор сообщения:',value=msg.author.mention+' | `'+msg.author.name+'#'+msg.author.discriminator+'`',inline=False)
            embed.add_field(name='Реакция:',value=pay.emoji)
            embed.set_thumbnail(url=msg.author.avatar_url)
            channel = discord.utils.get(msg.guild.channels, id=auditlogid)
            await channel.send(embed=embed)
        elif member.guild_permissions.administrator==True and pay.user_id!=bot.id:
            embed=discord.Embed(color=0xf04747)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Администратор убрал реакцию',icon_url='https://i.ibb.co/wy9P1wJ/remove-react.png')
            embed.add_field(name='Сообщение:',value='> '+msg.content+'\n'+'|[Перейти]('+msg.jump_url+')')
            embed.add_field(name='Автор сообщения:',value=msg.author.mention+' | `'+msg.author.name+'#'+msg.author.discriminator+'`',inline=False)
            embed.add_field(name='Администратор:',value=member.mention+' | `'+member.name+'#'+member.discriminator+'`',inline=False)
            embed.add_field(name='Реакция:',value=pay.emoji,inline=False)
            embed.set_thumbnail(url=msg.author.avatar_url)
            channel = discord.utils.get(msg.guild.channels, id=auditlogid)
            await channel.send(embed=embed)
        elif pay.user_id!=bot.id:
            embed=discord.Embed(color=0xf04747)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name='Пользователь убрал реакцию',icon_url='https://i.ibb.co/wy9P1wJ/remove-react.png')
            embed.add_field(name='Сообщение:',value='> '+msg.content+'\n'+'|[Перейти]('+msg.jump_url+')')
            embed.add_field(name='Автор сообщения:',value=msg.author.mention+' | `'+msg.author.name+'#'+msg.author.discriminator+'`',inline=False)
            embed.add_field(name='Пользователь:',value=member.mention+' | `'+member.name+'#'+member.discriminator+'`',inline=False)
            embed.add_field(name='Реакция:',value=pay.emoji)
            embed.set_thumbnail(url=msg.author.avatar_url)
            channel = discord.utils.get(msg.guild.channels, id=auditlogid)
            await channel.send(embed=embed)"""



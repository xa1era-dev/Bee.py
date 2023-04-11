from rhvoice_wrapper import TTS
import discord
import asyncio
import psycopg2
import datetime
import random
from modules import Modules


tts = TTS(data_path='C:/Users/Xa1era/OneDrive/Smileaffo/testxa1eratts/data', quiet = True)
#tts = TTS(opus_path = '/app/opus/lib/libopus.so.0',lib_path = '/app/rhvoice_wrapper_bin/lib/libRHVoice.so', data_path = '/app/data', force_process = True, quiet = True, stream = False)

tts.set_params(absolute_rate = 0.1)

new_names = ["Макака", "Объезянка", "Мартышка", "Курица", "Яйцо", "Шиш", "Борцуха", "Блин", "Шнапс", "Робин", "Скряга", "Тарас", "Баран", "Хохол", "Чекист"]

day = ['На утро новости таковы', "Утрние новости", "Утром появились известия"]
mafia_kill_f = ['(player) утром был обнаружен в своей квартире.', "(player) был найден", "(player) был найден на чердаке дома", "(player) был обнаружен", 'Игрок (player) был найдем мертвым']
mafia_kill_s = ["На трупе было обнаружено 4 ножевых удара", "Следователи выявили, что данного игрока убили в 2 часа ночи", "Мафия города оставила на трупе монежство резаных и огнестрельные ранения", "Криминалисты города выявили, что огнестрельные раны были сделаны пистолетом калибром 9 милиметров", "По-словам жильцов дома, они ничего не слышали ночью из квартиры игрока", "(player) был расчленен"]
lover_silence = ['Любовница провела прекрасную ночь с игроком (player)', "У игрока (player) сегодня была прекрасная ночь", "(player) от действий любовницы ночью ничего не смог сделать"]
doctor_heal = ['Доктор ночью вылечил игрока (player)', "Игрок (player) был вылечен доктором", "Доктор вылечил (player)"]

async def check_voice(guild : discord.Guild):
    if guild.voice_client.is_playing():
        asyncio.sleep(0.5)
        await check_voice(guild)
    return True

def color(colorid:int):
    if colorid==1:
        return 0xf04747
    if colorid==2:
        return 0xfaa61a
    if colorid==3:
        return 0x43b581
    if colorid==4:
        return 0x808080
    if colorid == 5:
        return 0x0c1445
    if colorid == 6:
        return 0xffb70c


def connection():
    return psycopg2.connect(dbname='db3m7ilsj07lrg',
    host='ec2-52-17-1-206.eu-west-1.compute.amazonaws.com',
    port='5432',
    user='pfuorceyetldlg',
    password='15eb0cfc69a44b1233180ad1906ce1b30db92edcb31f4e2d7f68f9ce1c33a63e',
    )


def get_player(lst : list, id : int):
    return [p for p in lst if p['id'] == id][0]


def get_phase(phase : str):
    if phase == 'mafia':
        return 'Мафия'
    elif phase == 'don':
        return 'Дон мафии'
    elif phase == 'doctor':
        return 'Доктор'
    elif phase == 'lover':
        return 'Любовница'
    elif phase == 'comisar':
        return 'Коммисар'
    elif phase == 'mag_man':
        return 'Журналист'


async def speak(guild : discord.Guild, txt):
    tts.to_file(filename = f"{guild.id}.ogg", format_ = 'opus', voice = 'vitaliy',
        text = txt)
    await play(guild)

async def play(guild : discord.Guild):
    if not guild.voice_client:
        info = Modules(guild.id).mafia.dict['room_id']
        chan = guild.get_channel(int(info))
        await chan.connect()
    else:
        if guild.voice_client.is_playing() == False:
            guild.voice_client.play(discord.FFmpegPCMAudio(f'{guild.id}.ogg'))

async def drop_game(guild : discord.Guild):
    mafia_dict = Modules(guild.id).mafia.dict
    players = mafia_dict['players_a'] + mafia_dict['players_d']
    for player in players:
        mem = await guild.fetch_member(player['id'])
        await mem.edit(nick = mem['bename'])
        if mem.voice.mute == True:
            await mem.edit(mute = False)
        players.remove(player)
    room = guild.get_channel(mafia_dict['room_id'])
    await room.edit(name = mafia_dict['settings']['beforename'])
    del Modules(guild.id).mafia.dict

class MafiaLobby(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    @discord.ui.button(label = '❔', style = discord.ButtonStyle.gray)
    async def instruct(self, button : discord.Button, inter: discord.Interaction):
        await Messages(inter.guild).instruct()
        tts.to_file(filename = f'{inter.guild.id}.ogg', text = 'Вы перешли в раздел, где можно узнать о работе с мафией',
            voice = 'vitaliy', format_ = 'opus', sets = None)
        await play(inter.guild)

    @discord.ui.button(label = '👥', style = discord.ButtonStyle.gray)
    async def roles_mafia(self, button : discord.Button, inter: discord.Interaction):
        if Modules(inter.user.id).rooms.is_creator:
            await Messages(inter.guild).roles()
    @discord.ui.button(label = '⌛', style = discord.ButtonStyle.gray)
    async def time_mafia(self, button : discord.Button, inter: discord.Interaction):
        if Modules(inter.user.id).rooms.is_creator:
            await Messages(inter.guild).time()
    @discord.ui.button(label = '🔧', style = discord.ButtonStyle.gray, row = 2)
    async def other_mafia(self, button : discord.Button, inter: discord.Interaction):
        if Modules(inter.user.id).rooms.is_creator:
            await Messages(inter.guild).other()
    @discord.ui.button(label = '✏️', style = discord.ButtonStyle.blurple, row = 2, custom_id = 'editnickname')
    async def change_nick(self, button : discord.Button, inter: discord.Interaction):
        mafia_dict = Modules(inter.guild.id).mafia.dict
        modal = discord.ui.Modal(title='Изменить название комнаты')
        modal.add_item(discord.ui.InputText(
            label='Введите свое имя для мафии (ваш текущий ник вернется после игры)',
            placeholder='Новое имя',required=True))
        async def recive_modal(interaction:discord.Interaction):
            await interaction.response.defer(ephemeral = True)
            mafia_dict['players_a'].appends({'id' : int(interaction.user.id), 'bename' : str(interaction.user.nick if interaction.user.nick else None)})
            embed = discord.Embed(color = color(3))
            embed.set_author(name = 'Ваш никнейм будет изменен в начале игры')
            embed.add_field(name = 'Новое название:',value = modal.children[0].value)
            await interaction.followup.send(embed = embed,ephemeral = True)
        modal.callback = recive_modal
        await inter.response.send_modal(modal)
    @discord.ui.button(label = '✔️', style = discord.ButtonStyle.green, row = 2)
    async def start_mafia(self, button : discord.Button, inter: discord.Interaction):
        mafia_dict = Modules(inter.guild.id).mafia.dict
        for p in mafia_dict['player_a']:
            if p['id'] == inter.user.id:
                p['ready'] = True
        Modules(inter.guild.id).mafia.dict = mafia_dict
        ready_p = [p['id'] for p in mafia_dict['players_a'] if p['ready'] == True]
    @discord.ui.button(label = '❌', style = discord.ButtonStyle.red, row = 3)
    async def drop_game_btn(self, button : discord.Button, inter : discord.Interaction):
        if Modules(inter.user.id).rooms.is_creator:
            await drop_game(inter.guild)


class Messages(object):
    def __init__(self, guild : discord.Guild):
        self.guild = guild
        info = Modules(guild.id).mafia.dict['msg_id'].split(', ')
        self.chan = guild.get_channel(int(info[0]))
        self.msg_id = int(info[1])

    async def lobby(self):
        msg = await self.chan.fetch_message(self.msg_id)
        lobby = discord.Embed(color = color(4))
        lobby.set_author(name = 'Начальный экран мафии')
        in_lobby = []
        in_lobby.append('`❔` - Узнать как работает мафия')
        in_lobby.append("`👥` - Настройка ролей в мафии")
        in_lobby.append('`⌛` - Настройка длительностей фаз игры')
        in_lobby.append('`🔧` - Допольнительные настройки мафии')
        in_lobby.append('`✏️` - Изменить никнейм на сервере для игры (Бот после игры вернет вам прежнее имя)')
        in_lobby.append('`✔️` - Начать игру')
        in_lobby.append('`❌` - Выйти из мафии')
        lobby.add_field(name = 'Кнопки:', value = '\n'.join(in_lobby))
        await msg.edit(embed = lobby, view = MafiaLobby())

    async def instruct(self):

        class InstructButtons(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)
            @discord.ui.button(label = '❓', style = discord.ButtonStyle.gray)
            async def rules_mafia(self, button : discord.Button, inter : discord.Interaction):
                if inter.guild.voice_client.is_playing() == False:
                    tts.to_file(filename = f"{inter.guild.id}.ogg", text = ("""Ход игры : Игра делится на два периода: день и ночь.
                        В дневном обсуждении — вычислении мафии — участвуют все игроки, а ночью все засыпают.
                        По команде ведущего ночью просыпаются отдельные персонажи и выполняют свои ролевые функции.
                        Роли распределяются случайным образом, которые раздаются в начале игры.
                        Когда ночь заканчивается, начинается дневное обсуждение: мирные жители пытаются выяснить, кто же является мафией, а мафия выдает себя за честных горожан и осторожно склоняет город голосовать против невинных.
                        В обсуждении могут использоваться провокации, интуиция, логические доводы и прочие приемы, позволяющие раскрыть истинные намерения собеседника.
                        Чем активнее обсуждение, тем больше шансов у мирных жителей разоблачить преступников и спасти город""",
                            """Роли-""",
                                '''Черный лагерь-''',
                                    '''Мафия-''',
                                        '''Цель мафии истребить всех мирных жителей.
                                        Днем мафия выдает себя за честных горожан, а ночью мафиози осторожно просыпаются и выбирают жертву, в которую стреляют''',
                                    '''Дон мафии-''',
                                        '''Выполняет два предназначения: во-первых, принимает окончательное решение, если мафия не может прийти к согласию в процессе выбора жертвы (если будет стоять настройка на голосование), а, во-вторых, просыпается отдельно от своих подопечных и пытается вычислить комиссара — предводителя мирных жителей. Каждую ночь дон указывает ведущему на того игрока, которого считает комиссаром, и получает либо отрицательный, либо положительный ответ. Если дон вычисляет комиссара, то старается убедить город выгнать этого игрока днем''',
                                    '''Любовница Дона-''',
                                        '''Ночью просыпается отдельно, чтобы кого-то заблокировать. Любовница наугад показывает на одного из игроков, и, если у того есть активная роль, этой ночью он не сможет ее выполнять. Доктор не сможет лечить. Главная цель любовницы — попасть в комиссара, доктора или другого представителя красного лагеря, чтобы подорвать их активность против мафии. Также, как и доктор, любовница не может указывать на одного и того же игрока две ночи подряд''',
                                '''Красный лагерь (мирный город)-''',
                                    '''Мирные жители-''',
                                        '''Их большинство, но они не знают, кто есть кто. Ночью мирные горожане не просыпаются, они участвуют только в дневном обсуждении, стараясь вычислить мафию''',
                                    '''Комиссар-''',
                                        '''Уполномоченный представитель мирного города. Просыпается в свой черед и проверяет любого игрока на принадлежность к мафии. Комиссар не стреляет, он может только получить ответ от ведущего, является ли мафией тот или иной игрок. Если комиссар вычисляет мафию, днем ему необходимо, не выдав своей роли, убедить город выгнать этого игрока''',
                                    '''Доктор-''',
                                        '''Обладает способностью лечить жителей города. Каждой ночью доктор пытается угадать, в кого стреляла мафия, и указывает на этого игрока ведущему. Если доктор угадал и вылечил жертву мафии, город просыпается без потерь или с меньшими потерями.
                                        Доктор не может исцелять одного и того же игрока две ночи подряд. Себя раз в 3 ночи''',
                                    '''Журналист-''',
                                        '''Просыпается ночью и проверяет любых двух игроков на принадлежность к одному или к разным лагерям. Журналист выбирает 2 человека, а после бот напишет журналисту, в одной или в разных командах находятся выбранные игроки. При этом цвет команд не называется. Например, если журналист показал на доктора и дона мафии, то ведущий ответит, что они принадлежат к разным лагерям. Если на комиссара и мирного жителя — то к одному.'''),
                        voice = 'vitaliy', format_ = 'opus')
                    await play(inter.guild)
            @discord.ui.button(label = '🤖', style = discord.ButtonStyle.gray)
            async def bot_as_leader(self, button : discord.Button, inter : discord.Interaction):
                if inter.guild.voice_client.is_playing() == False:
                    tts.to_file(filename = f"{inter.guild.id}.ogg", text = '''Бот создает для каждого игрока ветку. Подробнее о работе с ветками, нажмите нужную кнопку.
                        Также бот создает список (живых игроков), для голосований (днем или в свой ход)
                        Для подтверждения своего голоса, необходимо нажать кнопку с галочкой.
                        После подтверждения, свой голос нельзя будет изменить. Бот напишет вам в ветку о том, что вы подтвердили голос
                        Ход игры :
                        День : Все игроки могут разговаривать на обсуждение и голосование дается 10 минут (можно будет изменит).
                        Если стоит настройка "выбор Шерифа" - это значит, что днем есть шанс (после третьей ночи),
                        что одному из игроков придется проголосовать днем без обсуждений.
                        Днем игрок с наибольшим количеством голосов (голос комиссара считается за два голоса) убывает.

                        При наступлении ночи, все игроки уходят в мут,
                        Игроки с активной ролью ночью голосуют в свой ход,
                        Также игроки одной роли могут писать игрокам своей роли в свой ход.

                        
                        При включении настройки "ожидание входа" - это значит, что игра остановится после выхода одного из игрока,
                        на ожидании игрока будет выделено 5 минут. Игра будет остановлена после голосования. Все игроки будут размучены.
                        Если игрок не вернулся в течении пяти минут, то игрок выбывает из игры. В независимости от этой настройки, если игрок выбыл из игры, то его роль объявляется утром.
                        Администрации позже придется его размутить
                        ''',
                        voice = 'vitaliy', format_ = 'opus')
                    await play(inter.guild)
            @discord.ui.button(label = '💬', style = discord.ButtonStyle.gray)
            async def work_eith_threds(self, button : discord.Button, inter : discord.Interaction):
                if inter.guild.voice_client.is_playing() == False:
                    tts.to_file(filename = f"{inter.guild.id}.ogg", text = '''Бот создает для каждого игрока ветку.
                        Данная ветка будет способом общением с другими игроками.
                        Если включена настройка "Анонимный чат" - это значит, что игроки не будут видет отправителя сообщения

                        При отправке сообщения, бот перешлет это сообщение всем доступным игрокам в ветки,
                        то есть во время хода мафии сообщение будет передано только мафиям, если отправитель - мафия.
                        Если вы умерли, то вы сможете общаться с умершими, не зависимо от текущего хода, а также видет сообщения живых игроков
                        ''',
                        voice = 'vitaliy', format_ = 'opus')
                    await play(inter.guild)
            @discord.ui.button(label = '↩️', style = discord.ButtonStyle.red)
            async def back_to_lobby(self, button : discord.Button, inter : discord.Interaction):
                if inter.guild.voice_client.is_playing() == False:
                    await Messages(inter.guild).lobby()

        instruct = discord.Embed(color = color(4))
        instruct.set_author(name = 'Как работает мафия')
        instruct.add_field(name = 'Кнопки:', value = '''
        `❓` - Правила мафии 
        `🤖` - Работа бота в роли ведущего
        `💬` - Как работают ветки (чат с игроками)
        `↩️` - Вернуться в лобби''')
        msg = await self.chan.fetch_message(self.msg_id)
        await msg.edit(embed = instruct, view = InstructButtons())
    
    async def roles(self):
        mafia_dict = Modules(self.guild.id).mafia.dict
        class RolesButtons(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)
            @discord.ui.button(label = 'Мафия', style = discord.ButtonStyle.green, disabled = not (mafia_dict['settings']['count']['mafia'] < 25) or (mafia_dict['settings']['voteall'] == True and not (mafia_dict['settings']['count']['mafia'] < 15)))
            async def mafia_add(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['count']['mafia'] += 5
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).roles()
            @discord.ui.button(label = 'Мафия', style = discord.ButtonStyle.red, disabled = not (mafia_dict['settings']['count']['mafia'] > 10))
            async def mafia_remove(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['count']['mafia'] -= 5
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).roles()
            @discord.ui.button(label = 'Любовница', style = discord.ButtonStyle.green, row = 2, disabled = mafia_dict['settings']['count']['lover'] == 2)
            async def lover_add(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['count']['lover'] += 1
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).roles()
            @discord.ui.button(label = 'Любовница', style = discord.ButtonStyle.red, row = 2, disabled = mafia_dict['settings']['count']['lover'] == 1)
            async def lover_remove(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['count']['lover'] -= 1
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).roles()
            @discord.ui.button(label = 'Доктор', style = discord.ButtonStyle.green, row = 3, disabled = mafia_dict['settings']['count']['doctor'] == 2)
            async def doctor_add(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['count']['doctor'] += 1
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).roles()
            @discord.ui.button(label = 'Доктор', style = discord.ButtonStyle.red, row = 3, disabled = mafia_dict['settings']['count']['doctor'] == 1)
            async def doctor_remove(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['count']['doctor'] -= 1
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).roles()
            @discord.ui.button(label = 'Журналист', style = discord.ButtonStyle.green, row = 4, disabled = mafia_dict['settings']['count']['mag_man'] == 2)
            async def magman_add(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['count']['mag_man'] += 1
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).roles()
            @discord.ui.button(label = 'Журналист', style = discord.ButtonStyle.red, row = 4, disabled = mafia_dict['settings']['count']['mag_man'] == 1)
            async def magman_remove(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['count']['mag_man'] -= 1
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).roles()
            @discord.ui.button(label = '↩️', style = discord.ButtonStyle.red)
            async def back_to_lobby(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    await Messages(inter.guild).lobby()
        roles = discord.Embed(color = color(4))
        roles.set_author(name = 'Настройка ролей')
        don = '+ Дон' if mafia_dict['settings']['voteall'] == False else ''
        roles.add_field(name = f'Мафия (в % соотнешнии = мафия / все игроки) {don}:', value = str(mafia_dict['settings']['count']['mafia'])+'%')
        roles.add_field(name = 'Любовница (2 шт. от 13 и более игроков):', value = mafia_dict['settings']['count']['lover'], inline = False)
        roles.add_field(name = 'Комиссар:', value = '1', inline = False)
        roles.add_field(name = 'Доктор (2 шт. от 13 и более игроков):', value = mafia_dict['settings']['count']['doctor'], inline = False)
        roles.add_field(name = 'Журналист (от 17 и более игроков):', value = mafia_dict['settings']['count']['mag_man'], inline = False)
        msg = await self.chan.fetch_message(self.msg_id)
        await msg.edit(embed = roles, view = RolesButtons())

    async def time(self):
        mafia_dict = Modules(self.guild.id).mafia.dict
        class TimeButton(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)
            @discord.ui.button(label = '☀️', style = discord.ButtonStyle.green, row = 1, disabled = (mafia_dict['settings']['time']['day'] >= 1210))
            async def add_day_time(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['time']['day'] += 30
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).time()
            @discord.ui.button(label = '☀️', style = discord.ButtonStyle.red, row = 1, disabled = (mafia_dict['settings']['time']['day'] <= 310))
            async def rem_day_time(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['time']['day'] -= 30
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).time()
            @discord.ui.button(label = '🌑', style = discord.ButtonStyle.green, row = 2, disabled = (mafia_dict['settings']['time']['night'] >= 190))
            async def add_night_time(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['time']['night'] += 15
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).time()
            @discord.ui.button(label = '🌑', style = discord.ButtonStyle.red, row = 2, disabled = (mafia_dict['settings']['time']['night'] <= 40))
            async def rem_night_time(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['time']['night'] -= 15
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).time()
            @discord.ui.button(label = '↩️', style = discord.ButtonStyle.red, row = 3)
            async def back_to_lobby(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    await Messages(inter.guild).lobby()
        time = discord.Embed(color = color(4))
        time.set_author(name = 'Настройка длительностей фаз игры')
        time.add_field(name = 'Время на дневное голосование:', value = str(datetime.timedelta(seconds = (mafia_dict['settings']['time']['day'] - 10)))[2:], inline = False)
        time.add_field(name = 'Время на ночное голосование:', value = str(datetime.timedelta(seconds = (mafia_dict['settings']['time']['night'] - 10)))[2:])
        msg = await self.chan.fetch_message(self.msg_id)
        await msg.edit(embed = time, view = TimeButton())

    async def other(self):
        mafia_dict = Modules(self.guild.id).mafia.dict
        class OtherButtons(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)
            @discord.ui.button(label = '🕶️', style = (discord.ButtonStyle.green if mafia_dict['settings']['ingognito'] == True else discord.ButtonStyle.red))
            async def ingognito(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['ingognito'] = not mafia_dict['settings']['ingognito']
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).other()
            @discord.ui.button(label = '✅', style = (discord.ButtonStyle.green if mafia_dict['settings']['voteall'] == True else discord.ButtonStyle.red))
            async def voteall(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['voteall'] = not mafia_dict['settings']['voteall']
                    if mafia_dict['settings']['voteall'] == True:
                        mafia_dict['settings']['count']['mafia'] = 15
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).other()
            @discord.ui.button(label = '👑', style = (discord.ButtonStyle.green if mafia_dict['settings']['voteby1'] == True else discord.ButtonStyle.red))
            async def voteby1(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['voteby1'] = not mafia_dict['settings']['voteby1']
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).other()
            @discord.ui.button(label = '🚪', style = (discord.ButtonStyle.green if mafia_dict['settings']['waitleave'] == True else discord.ButtonStyle.red))
            async def waitleave(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    mafia_dict['settings']['waitleave'] = not mafia_dict['settings']['waitleave']
                    Modules(inter.guild.id).mafia.dict = mafia_dict
                    await Messages(inter.guild).other()
            @discord.ui.button(label = '↩️', style = discord.ButtonStyle.red)
            async def back_to_lobby(self, button : discord.Button, inter : discord.Interaction):
                if Modules(inter.user.id).rooms.is_creator:
                    await Messages(inter.guild).lobby()
        other = discord.Embed(color = color(4))
        other.set_author(name = 'Прочие настройки мафии')
        def color_ball(bool : bool):
            if bool == True:
                return '`🟢`'
            return '`🔴`'
        other.add_field(name = f'''{color_ball(mafia_dict['settings']['ingognito'])} | `🕶️` - Режим ингогнито:''',
            value = f'''`🟢` - Во время ночного голосования, вы не будете знать, кто играет с той же ролью, что и вы
            `🔴` - Все сообщения в ветках будут иметь отправителя
            ''', inline = False)
        other.add_field(name = f'''{color_ball(mafia_dict['settings']['voteall'])} | `✅` - Единоличное голосование:''',
            value = f'''`🟢` - Ночные голосования не будут проходить по принципу (большинства голос) `каждый голос имеет значение` (При данной настройки мафии МАКС 15 %)
            `🔴` - Ночные голосования будут проходить по правилу большинства голос. В игре участвует дон мафии. Он ходит вместе с мафией если будет спорная ситуация.
            ''', inline = False)
        other.add_field(name = f'''{color_ball(mafia_dict['settings']['voteby1'])} | `👑` - Выбор Шерифа:''',
            value = f'''`🟢` - Утром есть шанс (15%, но после 3 ночи), что одному из игроков придется проголосовать в течении минуты без рассуждений
            `🔴` - Все дневные голосования будут проходить без "изюминки"
            ''', inline = False)
        other.add_field(name = f'''{color_ball(mafia_dict['settings']['waitleave'])} | `🚪` - Ожидание входа:''',
            value = f'''`🟢` - Игра после выхода живого игрока из комнаты будет остановлена после голосования и будет выделено 5 мин. После 5 мин `🔴`
            `🔴` - Игрок покидает игру, его голос не учитывается, утром его роль раскрыавется, его ник меняется
            ''', inline = False)
        msg = await self.chan.fetch_message(self.msg_id)
        await msg.edit(embed = other, view = OtherButtons())
    
    async def main(self):
        mafia_dict = Modules(self.guild.id).mafia.dict
        alive_players = [self.guild.get_member(p['id']) for p in mafia_dict['players_a']]
        select_dict = {}
        phase = mafia_dict['settings']['phase']
        main = discord.Embed(color = color(6) if phase == 'day' else color(5))
        main.set_author(name = 'Игра идет')
        main.add_field(name = 'Текущая фаза игры', value = 'День' if phase == 'day' else f'Ночь, {get_phase(phase)}')
        class ListPlayers(discord.ui.Select):
            def __init__(self):
                super().__init__(placeholder = 'Выберите за кого вы хотите проголосовать', row = 1)
                self.options = [discord.SelectOption(label = f'{mem.nick}', value = mem.id) for mem in alive_players]
                self.min_values = 2 if phase == 'mag_man' else 1
                self.max_values = self.min_values
            async def callback(self, inter: discord.Interaction):
                if self.max_values == 2:
                    select_dict[f'{inter.user.id}'] = inter.data['values']
                else:
                    select_dict[f'{inter.user.id}'] = inter.data['values'][0]
        class SelectPlayers(discord.ui.view):
            def __init__(self):
                super().__init__(timeout = None)
                self.add_item(ListPlayers())
            @discord.ui.Button(label = '✅', style = discord.ButtonStyle.green)
            async def callback(self, button : discord.Button, inter : discord.Interaction):
                player = get_player(mafia_dict['players_a'], inter.user.id)
                if phase == 'day' or phase == player['role'][1]:
                    player['select'] = select_dict[f'{inter.user.id}']
                    Modules(inter.guild.id).mafia.dict = mafia_dict
        msg = await self.chan.fetch_message(self.msg_id)
        await msg.edit(embed = main, view = SelectPlayers())

    async def game_over(self):
        pass
            



class StartGame(object):
    def __init__(self):
        pass
    async def create_lobby(self, guild : discord.Guild, room_id : int):
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO mafia (guild) VALUES (%s)", [str(guild.id)])
                conn.commit()
        room = guild.get_channel(room_id)
        tts.to_file(filename = f'{guild.id}.ogg', text = 'Добро пожаловать в мафию. На данный момент вы находитесь в лобби. Для настройки игры воспользуйтесь кнопками. Не забудьте сменить ник на сервере перед началом игры',
            voice = 'vitaliy', format_ = 'opus', sets = None)
        console = guild.get_channel(Modules(room_id).rooms.console)
        lobby_romm = await console.clone(name = 'лобби мафии')
        emb = discord.Embed(color = color(4), title = 'Лобби')
        lobby = await lobby_romm.send(embed = emb)
        mafia_dict = {"players_a" : [],
                    "players_d" : [],
                    'settings' : {'count' : {'mafia' : 20, 'doctor' : 1, 'mag_man' : 1, 'lover' : 1},
                                'time' : {'day' : 610, 'night' : 70} ,
                                'beforename' : f'{room.name}',
                                'ingognito' : False,
                                "voteby1" : False,
                                "voteall" : False,
                                "waitleave" : True},
                    "room_id" : room.id,
                    "msg_id" : f"{lobby_romm.id}, {lobby.id}"}
        Modules(guild.id).mafia.dict = mafia_dict
        await play(guild)
        await Messages(guild).lobby()
        await room.edit(name = 'Мафия (в ожидании игроков)')
        Modules(room.id).rooms.is_mafia = True

    async def give_roles(self, guild : discord.Guild):
        tts.to_file(filename = f'{guild.id}.ogg', text = 'Производится раздача ролей',
            voice = 'vitaliy', format_ = 'opus', sets = None)
        await play(guild)
        mafia_dict = Modules(guild.id).mafia.dict
        room = guild.get_channel(mafia_dict['room_id'])
        renamed_players = [p['id'] for p in mafia_dict['players_a'] if p['bename']]
        for mem in room.members:
            if mem.id not in renamed_players:
                get_player(mafia_dict['players_a'], mem.id)['bename'] = str(mem.nick if mem.nick else None)
                await mem.edit(nick = random.choice(new_names))
        players_a = mafia_dict['players_a']
        players_with_role = []
        random.shuffle(players_a)
        count = mafia_dict['settings']['count']
        for p in players_a:
            del p['ready']
        if len(players_a) < 17:
            count['mag_man'] = 0
        if len(players_a) < 13:
            count['lover'] = 1
            count['doctor'] = 1
        for player in players_a[:(count['mafia'] / 100 * len(players_a))]:
            player['role'] = ['black', 'mafia']
            players_with_role.append(player)
            players_a.remove(player)
        for player in players_a[:count['doctor']]:
            player['role'] = ['red', 'doctor']
            players_with_role.append(player)
            players_a.remove(player)
        for player in players_a[:count['lover']]:
            player['role'] = ['black', 'lover']
            players_with_role.append(player)
            players_a.remove(player)
        players_a[0]['role'] = ['red', 'comisar']
        players_with_role.append(players_a[0])
        del players_a[0]
        if mafia_dict['settings']['voteall'] == True:
            players_a[0]['role'] = ['black', 'don']
            players_with_role.append(player)
            players_a.remove(player)
        if count['mag_man'] != 0:
            players_a[0]['role'] = ['red', 'mag_man']
            players_with_role.append(players_a[0])
            del players_a[0]
        for player in players_a:
            player['role'] = ['red', 'red']
            players_with_role.append(player)
            players_a.remove(player)
        mafia_dict['players_a'] = players_with_role
        Modules(guild.id).mafia.dict = mafia_dict
    
    
class Game():
    def __init__(self, guild : discord.Guild):
        self.guild = guild
        self.mafia_dict = Modules(self.guild.id).mafia.dict
        self.ids = self.mafia_dict['msg_id'].split(', ')
        self.chan = self.guild.get_channel(int(self.ids[0]))
        self.msg_id = int(self.ids[1])
    async def check_win(self):
        red_players = [p for p in self.mafia_dict['players_a'] if p['role'][0] == 'red']
        black_players = [p for p in self.mafia_dict['plyers_a'] if p['role'][0] == 'black']
        return [len(red_players) == 0, len(black_players) == 0]
    async def morning(self):
        self.mafia_dict['settings']['day'] += 1
        voted_dict = {'mafia' : [], 'lover' : [], 'doctor' : []}
        for p in self.mafia_dict['players_a']:
            if 'mafia' in p['voted']:
                voted_dict['mafia'].append({'id' : p['id'], 'name' : str(self.guild.get_member(p['id']).nick)})
            if 'lover' in p['voted']:
                voted_dict['lover'].append({'id' : p['id'], 'name' : str(self.guild.get_member(p['id']).nick)})
            if 'doctor' in p['voted']:
                voted_dict['doctor'].append({'id' : p['id'], 'name' : str(self.guild.get_member(p['id']).nick)})
        await speak(self.guild, ('''Город просыпается.''', random.choice(day)))
        asyncio.sleep(0.5)
        if await check_voice(self.guild):
            await speak(self.guild, [(random.choice(mafia_kill_f).replace('(player)', p['name']), random.choice(mafia_kill_s).replace('(player)', p['name'])) for p in voted_dict['mafia']])
        asyncio.sleep(0.5)
        if await check_voice(self.guild):
            await speak(self.guild, [random.choice(lover_silence).replace('(player)', p['name']) for p in voted_dict['lover']])
        asyncio.sleep(0.5)
        if await check_voice(self.guild):
            await speak(self.guild, [random.choice(doctor_heal).replace('(player)', p['name']) for p in voted_dict['doctor']])
        for p in voted_dict['mafia']:
            if p not in voted_dict['doctor']:
                dead_player = get_player(self.mafia_dict['plsyer_a'], p['id'])
                self.mafia_dict['players_d'].append(dead_player)
                self.mafia_dict['players_a'].remove(dead_player)
        if True in await self.check_win():
            await speak(self.guild, ['Игра окончена.:', 'Команда мафии победила' if (await self.check_win())[0] else 'Команда красных победила'])
        else:
            pass
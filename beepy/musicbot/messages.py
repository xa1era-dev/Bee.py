import discord
import discord.utils
from client import bot
from modules import Colors
from .utils import SongInQueueException, MaxLenghtException
from .music_bot_db import MusicBotData
from .queue import Queue
from .song import Song
from .settings import Settings
from .utils import ReapetVaritions
import datetime


class Messages():
    def __init__(self, guild : discord.Guild) -> None:
        self.guild = guild
        self.music_bot_data = MusicBotData(guild)
        self.channel = self.guild.get_channel(self.music_bot_data.channel_id)
        self.voice = discord.utils.get(bot.voice_clients, guild=guild) # type: ignore

    async def edit_now(self):
        self.now_msg = await self.channel.fetch_message(self.music_bot_data.now_msg_id)# type: ignore
        if len(self.music_bot_data.queue) != 0:
            if self.voice.is_playing():# type: ignore    
                embed = discord.Embed(color = Colors.GREEN.value)
                embed.set_author(name='Музыка играет')
            else:
                embed = discord.Embed(color = Colors.RED.value)
                embed.set_author(name = 'Музыка остановлена')
            song = self.music_bot_data.queue.next_song
            embed.timestamp = discord.utils.utcnow()
            if song is not None:
                if not song.is_stream:
                    embed.add_field(name = 'Трек:', value = f"""> [{str(song)}]({song.url})""", inline = False)
                    tractime = song.duration
                    time = datetime.timedelta(seconds=tractime)
                    embed.add_field(name = 'Длительность трека:', value = str(time), inline = False)
                else:
                    embed.add_field(name = 'Стрим:',value = f"""> [{str(song)}]({song.url})""", inline=False)
            embed.add_field(name = 'Громкость музыки:', value = f"{self.music_bot_data.settings.volume}%")
            queue = MusicBotData(self.guild).queue
            settings = MusicBotData(self.guild).settings
            await self.now_msg.edit(embed = embed, view = MusicControls(self.guild,
                                                                        discord.utils.get(bot.voice_clients, guild=self.guild),
                                                                        settings,
                                                                        queue))# type: ignore
        else:
            embed = discord.Embed(color = Colors.GRAY.value)
            embed.timestamp = discord.utils.utcnow()
            embed.set_author(name = 'Музыка не играет', icon_url = '')
            await self.now_msg.edit(embed = embed, view = None)

        await self.edit_guide_msg()

    async def edit_queue(self):
        self.queue_msg = await self.channel.fetch_message(self.music_bot_data.queue_msg_id)# type: ignore
        if len(self.music_bot_data.queue) > 1:
            embed = discord.Embed(color=Colors.GREEN.value)
            embed.set_author(name='Очередь', icon_url='')
            qtitles = self.music_bot_data.queue.names
            if len(', '.join(qtitles[1:])) < 1024:
                embed.add_field(name=f'Треки ({len(qtitles)}):',value=', '.join(qtitles),inline=False)
            else:
                qtitles_str=', '.join(qtitles[1:])
                embed.add_field(name = 'Треки:',value=str(qtitles_str[0:1020])+'...',inline=False)
            duration = self.music_bot_data.queue.duration
            time = datetime.timedelta(seconds = duration)
            embed.add_field(name = 'Длительность треков:', value = str(time), inline=False)
            embed.timestamp = discord.utils.utcnow()
            embed.set_footer(text = 'Максимальное количество песен в очереди равно 20')
            await self.queue_msg.edit(embed = embed, content = '', view = MusicQueue(self.guild, self.music_bot_data.queue))
        else:
            embed=discord.Embed(color = Colors.GRAY.value)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name = 'Очередь пуста')
            await self.queue_msg.edit(embed = embed, view = None)

    async def edit_guide_msg(self):
        self.guide_msg = await self.channel.fetch_message(self.music_bot_data.guide_msg_id)# type: ignore
        set = []
        vc = discord.utils.get(bot.voice_clients, guild=self.guild)
        if len(self.music_bot_data.queue) != 0:
            if vc:
                if vc.is_playing() is True:# type: ignore 
                    set.append('`▶️` - поставить песню на паузу')
                else:
                    set.append('`⏸` - возобновить проигрование песни')

                if len(self.music_bot_data.queue) > 1 and self.music_bot_data.settings.repeat != ReapetVaritions.Song:
                    set.append("`⏭` - включить следующую песню")
                elif len(self.music_bot_data.queue) > 1 and self.music_bot_data.settings.repeat == ReapetVaritions.Song:
                    set.append("`⏭` - включить следующую песню (не доступно из-за повтора одной песни)")

                elif len(self.music_bot_data.queue) == 1:
                    set.append("`⏹️` - очичтить очередь")

                if len(self.music_bot_data.queue) > 1:
                    set.append("`⏹️` - очистить очередь")

                if len(self.music_bot_data.queue) > 1:
                    set.append("`🔀` - перемешать песни в очереди")

                if len(self.music_bot_data.queue) > 1:
                    if self.music_bot_data.settings.repeat == ReapetVaritions.Not:
                        set.append("`🔁` - поставить очередь на повтор")
                    elif self.music_bot_data.settings.repeat == ReapetVaritions.Queue:
                        set.append("`🔁` - поставить песню на повтор")
                    elif self.music_bot_data.settings.repeat == ReapetVaritions.Song:
                        set.append("`🔂` - убрать песню с повтора")
                else:
                    if self.music_bot_data.settings.repeat == ReapetVaritions.Not:
                        set.append("`🔁` - поставить песню на повтор")
                    elif self.music_bot_data.settings.repeat == ReapetVaritions.Song:
                        set.append("`🔂` - убрать песню с повтора")

                if self.music_bot_data.settings.volume != 100:
                    set.append("`🔊` - прибавить громкость проигрования")
                if self.music_bot_data.settings.volume != 0:
                    set.append("`🔉` - убавить громкость проигрования")

                if len(self.music_bot_data.queue.history) > 0 and self.music_bot_data.settings.repeat != ReapetVaritions.Song:
                    set.append("`⏮` - включить следующую песню")
                elif len(self.music_bot_data.queue.history) > 0 and self.music_bot_data.settings.repeat == ReapetVaritions.Song:
                    set.append("`⏮` - включить следующую песню (не доступно из-за повтора одной песни)")

        howuse = discord.Embed(color = Colors.GRAY.value, title = """Для того чтобы включить песни достоточно написать в этот канал название песни|ссылку на youtube|ссылку на spotify.""")
        howuse.set_author(name = 'Как пользоваться музыкальным ботом')
        if len(set) != 0:
            howuse.add_field(name = 'Обозначения кнопок:', value = '\n'.join(set))
        await self.guide_msg.edit(embed = howuse)


class MusicHistory(discord.ui.View):
    def __init__(self, song):
        super().__init__(timeout=None)
        self.add_item(GoToQueueHistory(song))

class GoToQueueHistory(discord.ui.Button):
    def __init__(self, song):
        super().__init__(style=discord.ButtonStyle.secondary, label="🔙", custom_id="back_to_queue")
        self.song = song
    
    async def callback(self, interaction: discord.Interaction):
        
        queue = MusicBotData(interaction.guild).queue

        try:
            queue.move_to_queue(self.song)

        except SongInQueueException:
            err_emb = discord.Embed(color=Colors.RED.value, title="Песня уже в очереди")
            err_emb.set_footer(text="Автоматическое удаление через 5 секунд")
            await interaction.response.send_message(embed=err_emb, ephemeral=True, delete_after=5.0)

        except MaxLenghtException:
            err_emb = discord.Embed(color=Colors.RED.value, title="Очередь достигла максимума")
            err_emb.set_footer(text="Автоматическое удаление через 5 секунд")
            await interaction.response.send_message(embed=err_emb, ephemeral=True, delete_after=5.0)

        await interaction.response.defer()
        MusicBotData(interaction.guild).queue = queue

class PauseResumeButton(discord.ui.Button):
    def __init__(self, vc : discord.VoiceClient, is_disabled : bool = False):
        super().__init__(disabled=is_disabled, row=1, custom_id = 'pause')
        self.vc = vc
        if self.vc.is_playing():
            self.label = '▶️'
            self.style = discord.ButtonStyle.green
        else:
            self.label = '⏸️'
            self.style = discord.ButtonStyle.red

class NextSongButton(discord.ui.Button):
    def __init__(self, is_disabled : bool = False):
        super().__init__(label ='⏭️',style = discord.ButtonStyle.secondary, disabled=is_disabled, row=1, custom_id = 'next_song')

class StopButton(discord.ui.Button):
    def __init__(self, disabled : bool = False):
        super().__init__(label='⏹️', style=discord.ButtonStyle.red, row=1, custom_id="clear_queue", disabled=disabled)

class ShufleButton(discord.ui.Button):
    def __init__(self, disabled : bool = False, style : discord.ButtonStyle = discord.ButtonStyle.gray):
        super().__init__(label="🔀", row=2, disabled=disabled, style=style, custom_id = 'shufle')

class RepeatButton(discord.ui.Button):
    def __init__(self, *, style: discord.ButtonStyle = discord.ButtonStyle.gray, label: str = '🔁', disabled: bool = False):
        super().__init__(style=style, label=label, disabled=disabled, row=2, custom_id='repeat')

class VolumeUpButton(discord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(style=discord.ButtonStyle.secondary, label="🔊", disabled=disabled, custom_id='volume_up', row=2)

class VolumeDownButton(discord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(style=discord.ButtonStyle.secondary, label="🔉", disabled=disabled, custom_id='volume_down', row=2)

class PrevSongButton(discord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(style = discord.ButtonStyle.secondary, label="⏮", disabled=disabled, custom_id="prev_song", row=1)


class MusicControls(discord.ui.View):
    def __init__(self, guild : discord.Guild, vc : discord.VoiceClient, settings : Settings, queue : Queue):
        super().__init__(timeout=None)
        self.guild = guild
        self.is_confirm = False
        self.volume = settings.volume
        self.queue = queue
        self.icon_repeat = "🔁"
        self.style_repeat = discord.ButtonStyle.gray
        if settings.repeat == ReapetVaritions.Queue:
            self.style_repeat = discord.ButtonStyle.blurple
        elif settings.repeat == ReapetVaritions.Song:
            self.icon_repeat = "🔂"
            self.style_repeat = discord.ButtonStyle.green
        self.add_item(PrevSongButton(disabled=len(self.queue.history) == 0))
        self.add_item(PauseResumeButton(vc))
        self.add_item(NextSongButton())
        self.add_item(StopButton())
        self.add_item(ShufleButton(disabled=len(queue) == 1))
        self.add_item(RepeatButton(style=self.style_repeat, label=self.icon_repeat))
        self.add_item(VolumeUpButton(disabled=(self.volume == 100)))
        self.add_item(VolumeDownButton(disabled=(self.volume == 0)))
        


class MusicQueue(discord.ui.View):
    def __init__(self, guild : discord.Guild, queue : Queue):
        super().__init__(timeout = None)
        self.add_item(MusicSelect(guild, queue))

class MusicSelect(discord.ui.Select):
    def __init__(self, guild : discord.Guild, queue : Queue):
        self.guild = guild
        self.queue = queue
        opt=[]
        for song in list(self.queue.queue)[1:]: # type: ignore
            link = song.url
            opt.append(discord.SelectOption(label = str(song), description = link, value = link))
        super().__init__(placeholder='Выберите песню для удаления песни из очереди',options=opt,max_values=1)

    async def callback(self, interaction: discord.Interaction):
        song_index = self.queue.urls.index(self.values[0])
        self.queue.remove_song(self.queue.queue[song_index]) # type: ignore
        MusicBotData(self.guild).queue = self.queue
        await Messages.edit_queue(interaction.guild) # type: ignore
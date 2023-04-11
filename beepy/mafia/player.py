import discord
import enum
import rooms

class TypesRoles(enum.Enum):
    RED  = "Red"
    BLACK = "Black"
    GRAY = "GRAY"

class Roles(enum.Enum):
    MAFIA = "Mafia"
    DON = "Don"
    DOCTOR = "Doctor"
    LOVER = "Lover"
    COMMISSAR = "Commissar"
    SHERIF = "Sherif"
    KILLER = "Killer"
    LAWYER = "Lawyer"

class Settings():
    def __init__(self):
        self.percantage_mafia = 0.3
        self.is_don_in_game = False
        self.is_sherif_in_game = False
        self.is_killer_in_game = False
        self.is_lawyer_in_game = False
        self.is_lover_in_game = False

        self.is_knowing_who_dead_day = True #На утро после голосования все учстники узнают, роль убитого игрока
        self.is_knowing_who_dead_night = True #На утро перед голосованием все учстники узнают, роль игрока, на которого сходили активные роли

        self.is_dead_players_see_all_chats = True #Убитые игроки видят все переписки, а также выборы активных ролей

        self.is_don_choising = False #1 голос дона считается за 2 при False, при True дон выбирает кого убить
        self.is_don_can_see_choises = True #Во время отдельного хода дона, будет видить за кого проголосовала мафия

        self.is_killer_cant_kill = True #Маньяку дается выбор, никого не убивать
        
        self.is_doc_can_heal_himself = True #Док может себя лечить
        self.count_doc_self_heal = 5

        self.is_ingognito = False #Во время ночных действий вы не будете знать отправителя сообщений при True
        self.is_vote_by_1player = False #На утро есть шанс, что однму игроку придется самому выбирать кого застрелить утром, до 25% оставшихся игроков и после 3 ночи при True
        self.is_wait_player = True #Игра после выхода живого игрока из комнаты будет остановлена после голосования и будет выделено 5 мин. После 5 мин игрок покидает игру
        self.max_wait_time_secs = 300



class Player():
    def __init__(self, member : discord.Member):
        self.id = member.id
        self.be_name = member.nick
        self.af_name = None
        self.class_role : TypesRoles = None
        self.role : Roles = None
        self.is_ready = False
        self.is_alive = True

class Game():
    def __init__(self, channel : rooms.Room) -> None:
        pass
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""Цель файла для использования файлов сайта и бота модули,
конктретнее получение информации о модулях и изменение модулей для сервера"""
import json
import psycopg2

def connection():
    """Create conenction to db"""
    return psycopg2.connect(
        dbname = 'db3m7ilsj07lrg',
        host = 'ec2-52-17-1-206.eu-west-1.compute.amazonaws.com',
        port = '5432',
        user = 'pfuorceyetldlg',
        password = '15eb0cfc69a44b1233180ad1906ce1b30db92edcb31f4e2d7f68f9ce1c33a63e',)

class Modules(object):
    """main class"""
    def __init__(self,guild=None):
        self.guild=guild
        self.moderate=Moderate(self.guild)
        self.emojirole=EmojiRole(self.guild)
        self.mafia = Mafia(self.guild)

class Moderate(object):
    def __init__(self, guild):
        self.guild=guild
    def get_info(self):
        with connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT moderate FROM modules WHERE guildid=%s",[str(self.guild)])
                info=cursor.fetchall()[0][0]
                if info=='1':
                    return info
    @property
    def role(self):
        if self.get_info is not None:
            with connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT modrole FROM moderate WHERE guildid=%s",
                        [str(self.guild)])
                    info=cursor.fetchall()[0][0]
                    return int(info)
    @role.setter
    def role(self,value):
        if self.get_info and self.role!=value:
            with connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE moderate SET modrole=%s WHERE guildid=%s",
                        [str(value),str(self.guild)])
                    conn.commit()
    @property
    def chan(self):
        if self.get_info is not None:
            with connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT modchan FROM moderate WHERE guildid=%s",
                        [str(self.guild)])
                    info = cursor.fetchall()[0][0]
                    return int(info)
    @chan.setter
    def chan(self,value):
        if self.get_info and self.chan!=value:
            with connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE moderate SET modchan=%s WHERE guildid=%s",
                        [str(value),str(self.guild)])
                    conn.commit()
    @property
    def props(self):
        if self.get_info is not None:
            with connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT perms FROM moderate WHERE guildid=%s",
                        [str(self.guild)])
                    info=cursor.fetchall()[0][0]
                    return list(map(int,(info[1:-1]).split(', ')))
    @props.setter
    def props(self,value):
        if self.props!=value:
            with connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE moderate SET perms=%s WHERE guildid=%s",
                        [str(value),str(self.guild)])
                    conn.commit()

class EmojiRole(object):
    def __init__(self,guild):
        self.guild=guild
    def list_emojis(self,msg:int):
        with connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from emojirole where guildid=%s and msgid=%s',[str(self.guild),str(msg)])
                info=str(cursor.fetchall())
                return info
    def get_role(self,emoji:int):
        with connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('select roleid from emojirole where msgid=%s and emojiid=%s',[str(self.guild),str(emoji)])
                return int(cursor.fetchall()[0][0])
    def add_role(self,msgid:int,emojiid:int,roleid:int):
        with connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('insert into emojirole values (%s,%s,%s,%s)',[str(self.guild),str(msgid),str(emojiid),str(roleid)])
                conn.commit()

class Mafia(object):
    def __init__(self, guild):
        self.guild = guild
    @property
    def dict(self):
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT players, settings, room_id, players_dead, msg_id FROM mafia WHERE guild = '%s'", [self.guild])
                info = cur.fetchall()[0]
                return {"players_a" : list(map(json.loads, map(lambda x: "{"+str(x)+"}", info[0][2:-2].split('}, {')))), 'players_d' : list(map(json.loads, map(lambda x: "{"+str(x)+"}", info[3][2:-2].split('}, {')))) , 'settings' : json.loads(info[1]), 'room_id' : int(info[2]), 'msg_id' : info[4]}
    @dict.setter
    def dict(self, value : dict):
        setings = value['settings']
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE mafia SET players = %s, settings = %s, room_id = %s, players_dead = %s, msg_id = %s WHERE guild = %s',
                            [str(value['players_a']), json.dumps(setings), str(value["room_id"]), str(value['players_d']), str(value['msg_id']), str(self.guild)])
                conn.commit()
    @dict.deleter
    def dict(self):
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE rooms SET is_mafia = false FROM mafia WHERE roomid=mafia.room_id",)
                cur.execute("""DELETE FROM mafia WHERE guild = %s""",[str(self.guild)])
                conn.commit()

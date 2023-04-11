from database import *

class Guild(object):
    """Нужно для получения информации о сереве"""
    def __init__(self, guild=None):
        self.guild=guild

    @property
    def welcome_role(self):
        return int(select("guildsinfo", "welcomerole", "guildid", self.guild)[0][0])

    @welcome_role.setter
    def welcome_role(self, roleid : int):
        update("guildsinfo", {"welcomerole" : str(roleid)}, "guildid", self.guild)

    @welcome_role.deleter
    def welcome_role(self):
        update("guildsinfo", {'welcomerole' : None}, "guildid", self.guild)
        
    @property
    def guilds(self):
        return [int(gid[0]) for gid in select_all('guildsinfo', "guildid")]

    def add_guild(self):
        insert("guilds_modules", {"guild_id" : self.guild.id})

    def del_guild(self):
        delete("guilds_modules", "guild_id", str(self.guild.id))

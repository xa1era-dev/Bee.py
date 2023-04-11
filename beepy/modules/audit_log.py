"""Взаимодействия с журналом аудита"""

from database import insert, update, select, delete, select_all


class AuditLog(object):
    """getting auditlog info(channel,settings)"""
    def __init__(self, guild_id : int):
        self.guild = str(guild_id)

    @property
    def chan(self):
        return int(select('auditlog', "chanid", "guildid", self.guild)[0][0])
    
    @chan.setter
    def chan(self, value : int):
        if self.chan:
            update('auditlog', {'chanid' : str(value)}, "guildid", self.guild)
        else:
            insert("auditlog", {"guildid" : self.guild, 'chanid' : str(value)})
            update("modules", {'auditlog' : True}, "guildid", self.guild)

    @property
    def settings(self):
        if self.chan:
            info = select("auditlog", "*", "guildid", self.guild)[0]
            settstings = {'guildid':int(info[0]),
                "join_to_g" : info[2],
                "leave_from_g" : info[3],
                "ban_unban_on_g" : info[4],
                "time_outed" : info[5],
                "vchan_changed" : info[6],
                'vstate_changed' : info[7],
                'chan_created' : info[8],
                'msg_changed' : info[9],
                "msg_deleted" : info[10],
                "role_created" : info[11],
                "role_changed" : info[12],
                "role_delete" : info[13],
                'member_changed' : info[14],
                "g_changed" : info[15]}
        return settstings

    @settings.setter
    def settings(self, value : dict):
        if self.settings:
            update("auditlog", value, "guildid", self.guild)

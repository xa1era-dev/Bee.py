import discord
from client import get_bot as bot
#import modules
#rom bee import *

print(bot())

@bot.event
async def on_connect():
    await bot.sync_commands()
    print(f"""\n\n\n]{"-" * 20}[ bee.py is online as {bot.user}, my ping = {round(bot.latency * 1000)} ]{"-" * 20}[\n\n\n""")

"""@bot.event
async def on_voice_state_update(mem : discord.Member, before : discord.VoiceState | None, after : discord.VoiceState | None):
    await voice_state_update(mem, bot, before.channel, after.channel) # type: ignore

@bot.event
async def on_interaction(inter:discord.Interaction):
    await post_inter(inter, bot)

@bot.event
async def on_message(msg : discord.Message):
    await message(msg, bot)

@bot.event
async def on_guild_join(guild : discord.Guild):
    await bot.register_commands(guild_id = guild.id)
    modules.Guild(guild).add_guild()

@bot.event
async def on_guild_remove(guild : discord.Guild):
    modules.Guild(guild).del_guild()


@bot.slash_command(guild_id=[632619248241475594],name='musicbot', description='Позволяет управлять музыкальным ботом')
async def musicbot(
    ctx:discord.ApplicationContext,
    option:discord.Option(
        str,'Состояние музыкального бота',
        choices=['enable', 'disable', 'info']),):
    await musicbot_slash(ctx, option, bot)

@bot.slash_command(
    guild_id=[632619248241475594],
    name='room',
    description='Позволяет управлять комнатами')
async def rooms(
    ctx : discord.ApplicationContext,
    option : discord.Option(str, 'Состояние комнат', choices=['enable','disable'])): #type: ignore
    await rooms_slash(ctx, option, bot)"""
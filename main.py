import datetime
import logging
import random
import sqlite3

import discord
from discord.ext import commands

# логгер
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# инициализация бота
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
#инициализация базы данных
con = sqlite3.connect("banned.db")
cur = con.cursor()


#оповещение о включении бота
@bot.event
async def on_ready():
    print(f'{bot.user} подключен к Discord!')
    for guild in bot.guilds:
        print(
            f'{bot.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})'
        )


#сообщение при подключении пользователя
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1095765565370535998)
    role = discord.utils.get(member.guild.roles, id=1095764689952198676)
    await member.add_roles(role)
    await channel.send(f'Пользователь {member.name}, присоединился!')


#распределение ролей при реакции
@bot.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    if payload.message_id == 1099637285525389312 and payload.emoji.name == '🔴':
        role = discord.utils.get(member.guild.roles, id=1096033090272505967)
        await member.add_roles(role)
    elif payload.message_id == 1099637285525389312 and payload.emoji.name == '🔵':
        role = discord.utils.get(member.guild.roles, id=1096033139207442573)
        await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    if payload.message_id == 1099637285525389312 and payload.emoji.name == '🔴':
        role = discord.utils.get(member.guild.roles, id=1096033090272505967)
        await member.remove_roles(role)
    elif payload.message_id == 1099637285525389312 and payload.emoji.name == '🔵':
        role = discord.utils.get(member.guild.roles, id=1096033139207442573)
        await member.remove_roles(role)


#бан пользователя
@bot.command(name='ban')
@commands.has_role('Админ')
async def ban(ctx, member: discord.Member, reason='Без причины'):
    await ctx.message.delete()
    await member.ban(reason=reason)
    await ctx.send(f'Пользователь {member} был забанен по причине: {reason}')
    bndmember = str(member).split('#')
    cur.execute(f"INSERT INTO banned VALUES('{bndmember[0]}', '#{bndmember[1]}')")
    con.commit()


@bot.command(name='bottype')
@commands.has_role('Админ')
async def bottype(ctx, text):
    await ctx.message.delete()
    await ctx.send(text)


@bot.command(name='roll')
async def my_randint(ctx, min_int=1, max_int=100):
    await ctx.message.delete()
    num = random.randint(int(min_int), int(max_int))
    await ctx.send(num)


@bot.command(name='d6')
async def my_randint(ctx):
    await ctx.message.delete()
    d6 = random.randint(1, 6)
    await ctx.send(f'Вам выпало число {d6}')
    if d6 == 1:
        await ctx.send(file=discord.File('img/d1.jpg'))
    elif d6 == 2:
        await ctx.send(file=discord.File('img/d2.jpg'))
    elif d6 == 3:
        await ctx.send(file=discord.File('img/d3.jpg'))
    elif d6 == 4:
        await ctx.send(file=discord.File('img/d4.jpg'))
    elif d6 == 5:
        await ctx.send(file=discord.File('img/d5.jpg'))
    elif d6 == 6:
        await ctx.send(file=discord.File('img/d6.jpg'))


@bot.command(name='clear')
@commands.has_role('Админ')
async def clear(ctx, amount=30):
    await ctx.message.delete()
    await ctx.channel.purge(limit=int(amount))


@bot.command(name='mute')
@commands.has_role('Админ')
async def mute(ctx, member: discord.Member, timelimit):
    await ctx.message.delete()
    time = datetime.timedelta(seconds=int(timelimit))
    await member.edit(timed_out_until=discord.utils.utcnow() + time)


@bot.command(name='help')
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title='Помощь с командами')
    embed.add_field(name='!ban @name reason', value='Банит участника @name по причине reason')
    embed.add_field(name='!clear n', value='Очистка последних n сообщений чата, при отсутствии аргуметов n = 30')
    embed.add_field(name='!d6', value='Бросок шестигранного кубика')
    embed.add_field(name='!roll n p', value='Случайное число от n до p, при отсутствии аргуметов n = 1, p = 100')
    embed.add_field(name='!bottype "text" ', value='Бот отправляет сообщение text со своего аккаунта')
    embed.add_field(name='!mute @name time ', value='Бот запрещает писать сообщения @name участнику на time секунд')
    await ctx.send(embed=embed)


TOKEN = "MTA5MzA5MzI5NDE4MDkyNTQ5MQ.G5E7tr.3nOInKCP8pUmxyqaD8kjHL8J-kTCkxVK600Muc"

bot.run(TOKEN)

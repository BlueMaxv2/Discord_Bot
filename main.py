import discord
from discord.ext import commands
import random, logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user} подключен к Discord!')
    for guild in bot.guilds:
        print(
            f'{bot.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})'
        )


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1095765565370535998)
    role = discord.utils.get(member.guild.roles, id=1095764689952198676)
    await member.add_roles(role)
    await channel.send(f'Пользователь {member.name}, присоединился!')


@bot.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    if payload.message_id == 1096035666523074632 and payload.emoji.name == '🔴':
        role = discord.utils.get(member.guild.roles, id=1096033090272505967)
        await member.add_roles(role)
    elif payload.message_id == 1096035666523074632 and payload.emoji.name == '🔵':
        role = discord.utils.get(member.guild.roles, id=1096033139207442573)
        await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    if payload.message_id == 1096035666523074632 and payload.emoji.name == '🔴':
        role = discord.utils.get(member.guild.roles, id=1096033090272505967)
        await member.remove_roles(role)
    elif payload.message_id == 1096035666523074632 and payload.emoji.name == '🔵':
        role = discord.utils.get(member.guild.roles, id=1096033139207442573)
        await member.remove_roles(role)


@bot.command(name='bottype')
async def bottype(ctx, text):
    await ctx.send(text)


@bot.command(name='roll')
async def my_randint(ctx, min_int=1, max_int=100):
    num = random.randint(int(min_int), int(max_int))
    await ctx.send(num)


@bot.command(name='d6')
async def my_randint(ctx):
    d6 = random.randint(1, 6)
    await ctx.send(d6)


@bot.command(name='clear')
async def clear(ctx, amount=30):
    await ctx.channel.purge(limit=int(amount))


@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='Помощь с командами')
    embed.add_field(name='!clear n', value='Очистка последних n сообщений чата, при отсутствии аргуметов n = 30')
    embed.add_field(name='!d6', value='Бросок шестигранного кубика')
    embed.add_field(name='!roll n p', value='Случайное число от n до p, при отсутствии аргуметов n = 1, p = 100')
    embed.add_field(name='!bottype "text" ', value='Бот отправляет сообщение text со своего аккаунта')
    await ctx.send(embed=embed)


TOKEN = "MTA5MzA5MzI5NDE4MDkyNTQ5MQ.GnekER.1KU9YYjO-EL-2i2WkB3IhgBnhfX6HM4K4PbfGk"

bot.run(TOKEN)

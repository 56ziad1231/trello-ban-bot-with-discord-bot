import requests
import json
import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()




bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())


importpeopleids = [1058768145722134528] #DONT EDIT UNLESS YOU KNOW WHAT YOUR DOING
def botowners(ctx):
    return ctx.author.id in importpeopleids
apikey = os.getenv('apikey')
token = os.getenv('token')
idlist = os.getenv('idlist')
bottoken = os.getenv('bottoken')
webhook = os.getenv('webhook')





@bot.listen('on_ready')
async def on_ready():

    print(f'bot online- {bot.user} - {bot.user.id}')
    for s in bot.guilds:
      print(f'{s} - {s.id}')
      

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def sendlog(msg):
    json = {
        "content": msg,
        "embeds": None,
        "attachments": []
    }
    requests.post(webhook, json=json)






def getusername(userid):
  r = requests.get(f'https://api.newstargeted.com/roblox/users/v2/user.php?userId={userid}')
  response = r.json()
  plrusername = response["username"]
  print(plrusername)


def getuserid(username):
    r = requests.get(f'https://api.newstargeted.com/roblox/users/v2/user.php?username={username}')
    response = r.json()
    plruserid = response['userId']



@bot.command()
#@commands.has_role()
async def ban(ctx, user,*, reason=None):
    if user.isnumeric():
      opuser = getusername(user)
      print('User id')
      jbziscool = 'd'
    else:
        user = getuserid(user)

    url = "https://api.trello.com/1/cards"

    headers = {
      "Accept": "application/json"
    }

    query = {
      'idList': idlist,
      'key': apikey,
      'token': token
    }

    responsee = requests.request(
      "POST",
      url,
      headers=headers,
      params=query
    )

    a = responsee.json()
    this = a['shortLink']


    url = f"https://api.trello.com/1/cards/{this}"
    query = {'key': apikey, 'token': token}
    payload = {'name': user}
    response = requests.request("PUT", url, params=query, data=payload)

    try:
      plrusernamefunc = getusername(user)
      await ctx.send(f'```\nBANNED ({ctx.author}): {plrusernamefunc} unban key: {this}```')
    except:
      await ctx.send(f'\nBANNED ({ctx.author}): {user} - use key `{this}` to unban')

    sendlog(f'Banned id: `{user}` with key `{this}`')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Exploiters get banned - Jb9#6554"))
    await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')





@bot.command()
#@commands.has_role(1061432140333596683)
async def unban(ctx, trelloident,*, reason=None):

  url = f"https://api.trello.com/1/cards/{trelloident}"

  query = {
    'key': apikey,
    'token': token
  }

  response = requests.request(
    "DELETE",
    url,
    params=query
  )
  await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')




@bot.command(aliases=['e', 'evaluate'])
@commands.check(botowners)
async def eval(ctx, *, code):
    """Evaluates customized code"""
    language_specifiers = ["python", "py", "javascript", "js", "html", "css", "php", "md", "markdown", "go", "golang", "c", "c++", "cpp", "c#", "cs", "csharp", "java", "ruby", "rb", "coffee-script", "coffeescript", "coffee", "bash", "shell", "sh", "json", "http", "pascal", "perl", "rust", "sql", "swift", "vim", "xml", "yaml"]
    loops = 0
    while code.startswith("`"):
        code = "".join(list(code)[1:])
        loops += 1
        if loops == 3:
            loops = 0
            break
    for language_specifier in language_specifiers:
        if code.startswith(language_specifier):
            code = code.lstrip(language_specifier)
    try:
        while code.endswith("`"):
            code = "".join(list(code)[0:-1])
            loops += 1
            if loops == 3:
                break
        code = "\n".join(f"    {i}" for i in code.splitlines())
        code = f"async def eval_expr():\n{code}"
        def send(text):
            bot.loop.create_task(ctx.send(text))
        env = {
            "bot": bot,
            "client": bot,
            "ctx": ctx,
            "print": send,
            "_author": ctx.author,
            "_message": ctx.message,
            "_channel": ctx.channel,
            "_guild": ctx.guild,
            "_me": ctx.me
        }
        env.update(globals())
        exec(code, env)
        eval_expr = env["eval_expr"]
        result = await eval_expr()
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        if result:
            await ctx.send(result)
    except Exception as learntofuckingcode:
        await ctx.message.add_reaction("\N{WARNING SIGN}")
        await ctx.send(f'**Error**```py\n{learntofuckingcode}```')



bot.run(bottoken)

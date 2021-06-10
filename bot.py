from twitchio.ext import commands
import json, time

def openJsonDoc(nameOfDoc = "score"):
    with open(f'{nameOfDoc}.json', 'r') as f:
        data = json.load(f)
    return data

score = openJsonDoc()

def writeJsonDoc(dumpData = score, location = "score"):
    with open(f'{location}.json', 'w') as f:
        json.dump(dumpData, f, indent=4)

bot = commands.Bot(
    irc_token = "",
    client_id = "",
    nick = 'TheSmallNut_Bot',
    prefix = "+",
    initial_channels = ["itzbytez", "whoishyper", "thesmallnut"]
)

@bot.event
async def event_ready():
    print(f"Logged into Twitch | {bot.nick} ")

@bot.event
async def event_message(ctx):
    await bot.handle_commands(ctx)

@bot.event
async def after_invoke(ctx):
    
    print(ctx.content)

@bot.command(name='hyper', aliases=["HYPER", "Hyper"])
async def addToHyper(ctx):
    score["Hyper"] += 1
    await ctx.send(f"Added 1 point to Hyper, Hyper : {score['Hyper']} Bytez : {score['Bytez']}")
    writeJsonDoc()
    time.sleep(1)


@bot.command(name='bytez', aliases=["BYTEZ", "Bytez"])
async def addToBytez(ctx):
    score["Bytez"] += 1
    await ctx.send(f"Added 1 point to Bytez, Hyper : {score['Hyper']} Bytez : {score['Bytez']}")
    writeJsonDoc()
    time.sleep(1)

@bot.command(name='points', aliases=["POINTS", "Points"])
async def displayPoints(ctx):
    await ctx.send(f"Hyper : {score['Hyper']} Bytez : {score['Bytez']}")
    time.sleep(1)

bot.run()
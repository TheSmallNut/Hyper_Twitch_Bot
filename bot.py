from twitchio.ext import commands
import json, time, requests, tokens
from threading import Thread, Timer
from datetime import datetime

# Constants
CHANNELS = ["thesmallnut"]
FILE_NAME = "score.json"
BOT_NAME = "TheSmallNut_Bot"
TIMER_REFRESH_TIME = 5.0

# Globals
isTimerRunning = False
timer = None

def openJsonDoc():
    with open(FILE_NAME, 'r') as f:
        data = json.load(f)
    return data

def actuallyWriteJsonDoc():
    global isTimerRunning
    isTimerRunning = False
    time = datetime.now()
    currentTime = time.strftime("%H:%M:%S   %D")
    print(f"Writing to disk | {currentTime}")
    with open(FILE_NAME, 'w') as f:
        json.dump(score, f, indent=4)

def writeJsonDoc():
    global isTimerRunning
    if isTimerRunning:
        # do nothing... it's going to write anyway
        return
    isTimerRunning = True
    Timer(TIMER_REFRESH_TIME, actuallyWriteJsonDoc).start()


bot = commands.Bot(
    irc_token = tokens.token,
    client_id = tokens.clientID,
    nick = BOT_NAME,
    prefix = "+hnbt84yu53n7834t7843tbny8h348g4h325hg8",
    initial_channels = CHANNELS
)

@bot.event
async def event_ready():
    print(f"Logged into Twitch | {bot.nick} ")


@bot.event
async def event_message(ctx):
    await bot.handle_commands(ctx)

# @bot.event
# async def after_invoke(ctx):
    
#     print(ctx.content)


@bot.event
async def event_part(user):
    if user.name in score["currentlyWatching"]:
        score["currentlyWatching"].remove(user.name)
        writeJsonDoc()
    #print(user.name + " just left")

@bot.event
async def event_join(user):
    user_name = user.name.rstrip()
    if user_name not in score["currentlyWatching"]:
        score["currentlyWatching"].append(user_name)
        writeJsonDoc()
        #print(user_name + " just joined")


score = openJsonDoc()
score["currentlyWatching"] = []
writeJsonDoc()
bot.run()

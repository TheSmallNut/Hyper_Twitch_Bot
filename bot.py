from twitchio.ext import commands
import json, time, requests, tokens
from threading import Thread, Timer
from datetime import datetime

# Constants
CHANNELS = ["thesmallnut"]
FILE_NAME = "score.json"
BOT_NAME = "TheSmallNut_Bot"
TIMER_REFRESH_TIME = 5.0
ADDITIVE_POINTS = 10
TIME_TO_ADD_POINTS = 300
DEFAULT_STARTING_POINTS = 40

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

def makePage(pageCreationUser):
    for user in score["users"]:
        if pageCreationUser == user["name"]:
            return user
    score["users"].append({})
    location = score["users"][-1]
    location["name"] = pageCreationUser
    location["points"] = 40
    writeJsonDoc()
    return location

def addPoints():
    for user in score["currentlyWatching"]:
        currentUser = makePage(user)
        currentUser["points"] += ADDITIVE_POINTS
    writeJsonDoc()
    t = Timer(TIME_TO_ADD_POINTS, addPoints)
    t.start()

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
    makePage(user)
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
addPoints()
bot.run()

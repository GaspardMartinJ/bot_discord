from datetime import datetime, timezone
import discord
from discord.ext import commands
import sheetsAPI
import json

values = sheetsAPI.getValues()
nameDict = {'test1': ['gaspard', '1291'], 'test2': ['tp_bot_discord', '8512']}
pingList = []
messageID = 0
for person in values:
    if person[0] in nameDict:
        if person[1]== '1':
            pingList.append(nameDict[person[0]])

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix="!", intents=default_intents)

@bot.event
async def on_ready():
    print("Le bot est prêt !")

@bot.event
async def on_message(message):
    global messageID
    global sentTime
    global userList
    if message.content == "ping":
        pingString = ''
        userList = []
        for name, id in pingList:
            user = discord.utils.get(message.guild.members, name = name, discriminator=id)
            userList.append(user)
            pingString += user.mention + ' '
        pingString += ': réagissez avec :thumbsup: pour montrer que vous avez vu le message'
        pingMessage = await message.channel.send(pingString)
        sentTime = datetime.now(timezone.utc)
        messageID = pingMessage.id
        await pingMessage.add_reaction('👍')
        
    
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.id == messageID and str(reaction.emoji) == '👍' and user.bot == False and user in userList:
        reactTime = datetime.now(timezone.utc)
        timeDiff = reactTime - sentTime
        message = str(divmod(timeDiff.total_seconds(), 60)[0]) + ' minutes'
        content = list(nameDict.values())
        rowID = content.index([user.name, user.discriminator])+2
        values = [[message]]
        sheetsAPI.writeValues(rowID, values)

bot.run(json.load(open('botToken.json'))['TOKEN'])
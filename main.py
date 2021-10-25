from datetime import datetime, timezone
import discord
from discord.ext import commands
import sheetsAPI
import json
import os


default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix="!", intents=default_intents)

values = sheetsAPI.getValues()

# association des noms dans le tableau et des membres du serveur
nameDict = {'test1': ['gaspard', '1291'], 'test2': ['tp_bot_discord', '8512'], 'test3': ['CheeseNan', '0193']}

messageID = 0
userList = []
pingList = []

# création de la liste des noms et ID à ping avec les infos du tableau
for person in values:
    if person[0] in nameDict:
        if person[1]== '1':
            pingList.append(nameDict[person[0]])

@bot.event
async def on_ready():
    print("Le bot est prêt !")

# ping la liste des membres donnée
@bot.command(name="ping")
async def ping(ctx):
    global messageID
    global sentTime
    global userList
    pingString = ''
    userList = []
    # recherche des objets user à ping pour tous les avoir dans 1 message
    for name, id in pingList:
        user = discord.utils.get(ctx.guild.members, name = name, discriminator=id)
        userList.append(user)
        pingString += user.mention + ' '
    pingString += ': réagissez avec :thumbsup: pour montrer que vous avez vu le message'
    pingMessage = await ctx.channel.send(pingString)
    await pingMessage.add_reaction('👍')
    sentTime = datetime.now()
    messageID = pingMessage.id
    sheetsAPI.clearValues("C2:C4")
        
# réagi à la réaction des membres concernés en écrivant le temps mis à répondre dans le tableau
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.id == messageID and str(reaction.emoji) == '👍' and user.bot == False and user in userList:
        reactTime = datetime.now()
        timeDiff = reactTime - sentTime
        # mise en forme du message avec la difference de temps en minutes
        message = str(round(divmod(timeDiff.total_seconds(), 60)[0])) + ' minutes'
        # utilisation du dictionnaire pour trouver l'index de la ligne à modifier
        content = list(nameDict.values())
        # +2 à cause du 0 indexing et de la ligne de description dans le tableau
        rowID = content.index([user.name, user.discriminator])+2
        # [[]] parce qu'on ne modifie qu'une ligne mais on pourrait en modifier plusieurs
        values = [[message]]
        sheetsAPI.writeValues(rowID, values)

token = os.environ.get('bot_token')
bot.run(token)
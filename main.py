# import necessary modules
import datetime
import itertools
import urllib
from asyncio import sleep

import discord
from texttable import Texttable

import requests
from discord.ext import commands
from bs4 import BeautifulSoup
from itertools import combinations
import termtables as tt

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Start reading database')

# creates a bot instance with "$" as the command prefix
bot = commands.Bot("$")


TOKEN = ".XtwIdQ.nNIcMroWqJLgLuGqEFec9XSlFSQ"

steamIDs = {}
steamIDs['276083035881865216'] = {}
steamIDs['276083035881865216']['steamID'] = "76561198037206123"
steamIDs['276083035881865216']['name'] = "SnowTurtle96"

steamIDs['132009017215025153'] = {}
steamIDs['132009017215025153']['steamID'] = "76561198008626275"
steamIDs['132009017215025153']['name'] = "jordan"

steamIDs['165106314274537472'] = {}
steamIDs['165106314274537472']['steamID'] = "76561198009516269"
steamIDs['165106314274537472']['name'] = "Acax"

steamIDs['166982030129758208'] = {}
steamIDs['166982030129758208']['steamID'] = "76561198006566531"
steamIDs['166982030129758208']['name'] = "CPTblackadder"

steamIDs['181418485161787392'] = {}
steamIDs['181418485161787392']['steamID'] = "76561198145549652"
steamIDs['181418485161787392']['name'] = "KOAN"

steamIDs['309426653887725580'] = {}
steamIDs['309426653887725580']['steamID'] = "76561198013525723"
steamIDs['309426653887725580']['name'] = "fhtagn"

steamIDs['313389208339218433'] = {}
steamIDs['313389208339218433']['steamID'] = "76561198136729617"
steamIDs['313389208339218433']['name'] = "Salah Magoosh"

steamIDs['326091479250501633'] = {}
steamIDs['326091479250501633']['steamID'] = "76561198054949051"
steamIDs['326091479250501633']['name'] = "ben storey-waters"

steamIDs['364461741272203275'] = {}
steamIDs['364461741272203275']['steamID'] = "76561198048878401"
steamIDs['364461741272203275']['name'] = "Davethecave"

steamIDs['469283689503653888'] = {}
steamIDs['469283689503653888']['steamID'] = "76561198077931810"
steamIDs['469283689503653888']['name'] = "ADAM-PC"

steamIDs['183311683555426304'] = {}
steamIDs['183311683555426304']['steamID'] = "76561198119549929"
steamIDs['183311683555426304']['name'] = "Fresh Lima"


# a command in discord.py is <command-prefix><command-name>
# this creates a command that can be triggered by `$hello`, ie. "hello" is the command name
@bot.command()
async def hello(ctx):  # note: discord commands must be coroutines, so define the function with `async def`
    # the ctx argument is automatically passed as the first positional argument

    # you can access the author (type discord.Member) and channel (type discord.TextChannel) of the command as followed:
    message_author = ctx.author
    message_channel = ctx.channel

    # prints "<username> said hello" to the console
    print("{} said hello".format(message_author))

    # Member.send(...) is a coroutine, so it must be awaited
    # this sends a message "Hello, <username>!" to the message channel
    await message_channel.send("Hello, {}!".format(message_author.name))
    # more info on string formatting: https://pyformat.info


@bot.command()
async def killliam(ctx):  # note: discord commands must be coroutines, so define the function with `async def`
    # the ctx argument is automatically passed as the first positional argument

    # you can access the author (type discord.Member) and channel (type discord.TextChannel) of the command as followed:
    message_author = ctx.author
    message_channel = ctx.channel

    # prints "<username> said hello" to the console
    i = 0
    while i < 5:
        i = i + 1
        await sleep(5)
        await message_channel.send("!liam")




# This is how you define a discord.py event
@bot.event
async def on_ready():  # the event `on_ready` is triggered when the bot is ready to function
    print("The bot is READY!")
    print("Logged in as: {}".format(bot.user.name))


@bot.command()
async def balance(ctx, message):
    global steamIDs
    message_channel = ctx.channel
    await message_channel.send("Processing...")
    algorithm = Algorithm()
    usersToBalance = algorithm.parseUsers(ctx.message.mentions)

    playerData = {}
    apiKey = "CFB7FDD8F34ACA5A9C0BB4C0C5C047B4"

    print(usersToBalance)
    print("users^")
    for user in usersToBalance:
        print("user" + str(user))

        steamid = user['steamID']
        steamname = user['name']



        try:
            website = urllib.request.urlopen('https://steamcommunity.com/profiles/'+steamid+'/stats/L4D2?tab=stats&subtab=versus')  # Replace with URL to desired user page
            htmlText = website.read()
            soup = BeautifulSoup(htmlText, "html.parser")

            # Versus games played
            k = soup.find_all('div', class_='blueBoxFour')
            gamesPlayed = k[0].get_text()

            # Highest survivor team score
            temp = k[3].get_text()
            highestSurviorScore = temp[27:]

            # Get hours played
            hoursPlayed = soup.find_all('div', id='tsblVal')
            hoursPlayed = hoursPlayed[0].get_text()
            hoursPlayed = hoursPlayed.split("h")


            winRatio = soup.find_all('div', id='winlosstxtleft')
            winRatio = winRatio[0].get_text()
            winRatio = winRatio.split("%")
            winRatio = winRatio[0]

            playerData[steamid] = {}
            playerData[steamid]['Name'] = steamname
            playerData[steamid]['Hours'] = hoursPlayed[0]
            playerData[steamid]['Games Played'] = gamesPlayed[19:]
            playerData[steamid]['Highest Survivor Score'] = highestSurviorScore
            playerData[steamid]['Win Ratio'] = winRatio

            player = algorithm.assignScores(playerData[steamid], playerData[steamid]['Hours'], playerData[steamid]['Games Played'], playerData[steamid]['Highest Survivor Score'], winRatio)
            playerData[steamid] = player
            print(playerData)
            print("arrived at player data")


        except ZeroDivisionError:
            print("error for " + steamname)
            await message_channel.send("Error: Cannot balance " + steamname + " likely a private profile")

    teams = algorithm.balanceTeams(playerData, ctx)
    await algorithm.writeTeamOutput(ctx, teams[0], teams[1])
    await message_channel.send("Team 1 Score " + str(teams[2]))
    await message_channel.send("Team 2 Score " + str(teams[3]))
    if(teams[2] > teams[3]):
        await message_channel.send("Advantage to team 1 by : " + str(int(abs(teams[2] - teams[3]))))
    else:
        await message_channel.send("Advantage to team 2 by: " + str(int(abs(teams[2] - teams[3]))))


@bot.command()
async def test(ctx):
    embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~",
                          colour=discord.Colour(0x2619e0), url="https://discordapp.com",
                          description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```",
                          timestamp=datetime.datetime.utcfromtimestamp(1592417086))

    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_author(name="author name", url="https://discordapp.com",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="Team 1", value="some of these properties have certain limits...")
    embed.add_field(name="😱Team 2, value=" "")

    embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
    embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)
    message_channel = ctx.channel

    await message_channel.send(
        content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```",
        embed=embed)


@bot.command()
async def leaderboard(ctx):

    global steamIDs
    message_channel = ctx.channel
    await message_channel.send("Processing...")
    algorithm = Algorithm()

    playerData = {}
    apiKey = "CFB7FDD8F34ACA5A9C0BB4C0C5C047B4"

    print("users^")
    print(steamIDs)
    for user in steamIDs:
        print("user" + str(user))

        steamid = steamIDs[user]['steamID']
        steamname = steamIDs[user]['name']

        try:
            website = urllib.request.urlopen(
                'https://steamcommunity.com/profiles/' + steamid + '/stats/L4D2?tab=stats&subtab=versus')  # Replace with URL to desired user page
            htmlText = website.read()
            soup = BeautifulSoup(htmlText, "html.parser")

            # Versus games played
            k = soup.find_all('div', class_='blueBoxFour')
            gamesPlayed = k[0].get_text()

            # Highest survivor team score
            temp = k[3].get_text()
            highestSurviorScore = temp[27:]

            # Get hours played
            hoursPlayed = soup.find_all('div', id='tsblVal')
            hoursPlayed = hoursPlayed[0].get_text()
            hoursPlayed = hoursPlayed.split("h")

            winRatio = soup.find_all('div', id='winlosstxtleft')
            winRatio = winRatio[0].get_text()
            winRatio = winRatio.split("%")
            winRatio = winRatio[0]

            playerData[steamid] = {}
            playerData[steamid]['Name'] = steamname
            playerData[steamid]['Hours'] = hoursPlayed[0]
            playerData[steamid]['Games Played'] = gamesPlayed[19:]
            playerData[steamid]['Highest Survivor Score'] = highestSurviorScore
            playerData[steamid]['Win Ratio'] = winRatio

            player = algorithm.assignScores(playerData[steamid], playerData[steamid]['Hours'],
                                            playerData[steamid]['Games Played'],
                                            playerData[steamid]['Highest Survivor Score'], winRatio)
            playerData[steamid] = player

        except:
            print("error for " + steamname)
            await message_channel.send("Error: Cannot balance " + steamname + " likely a private profile")
    print(playerData)
    await message_channel.send("Error: Cannot balance " + steamname + " likely a private profile")


@bot.command()
async def balance1(ctx):
    members = ctx.guild.members
    for member in members:
        print("--------")
        print(member.id)
        print(member.name)


@bot.command()
async def findFuckedProfiles(ctx):
    global steamIDs
    for key, value in steamIDs.items():
        steamid = value['steamID']
        steamname = value['name']
        try:
            website = urllib.request.urlopen(
            'https://steamcommunity.com/profiles/' + steamid + '/stats/L4D2?tab=stats&subtab=versus')  # Replace with URL to desired user page
            htmlText = website.read()
            soup = BeautifulSoup(htmlText, "html.parser")
            k = soup.find_all('div', class_='blueBoxFour')
            gamesPlayed = k[0].get_text()

        except:
            message_channel = ctx.channel
            await message_channel.send(steamname + " cannot be balanced, probably private profile cannot parse")

            print("error!")

class Algorithm:
    def assignScores(self, player, hours, gamesPlayed, highestScore, winRatio):
        try:
            # Games played will be the core base stat
            gamesPlayed = int(gamesPlayed)
            highestScore = int(highestScore.replace(',', ''))
            winRatio = int(winRatio)
            #
            score = gamesPlayed / 10
            logging.info("Contribtuion from games played %s", str(score))
            # Add win ratio
            temp = winRatio * 12
            logging.info("Contribtuion from win ratio %s", str(temp))
            score += temp

            # Highest score
            temp = highestScore / 100
            logging.info("Contribtuion from highest survivor score %s", str(temp))
            score += temp

            player['Score'] = score
            return player
        except ZeroDivisionError:
            print("failure")

    def balanceTeams(self, players, ctx):
        playersSanitisedArray = []
        team1 = []
        team2 = []

        print("players")
        print(players)



        message_channel = ctx.channel

        for key in players.items():

            playerSanitised = PlayerSanitised()
            playerSanitised.name = players[key[0]]['Name']
            playerSanitised.score = players[key[0]]['Score']
            playersSanitisedArray.append(playerSanitised)

        for player in playersSanitisedArray:
            print(player.name)

        N = len(players)
        good = []
        all = []
        for perm in list(itertools.permutations(players)):
            if sorted(perm[:N // 2]) not in all and sorted(perm[N // 2:]) not in all:
                good.append(tuple([sorted(perm[:N // 2]), sorted(perm[N // 2:])]))
                all.append(sorted(perm[:N // 2]))
                all.append(sorted(perm[N // 2:]))

        lowestTeamDiff = 2147483647
        bestTeam1 = []
        bestTeam2 = []

        bestTeam1Score = None
        bestTeam2Score = None

        for i in range(len(good)):
            print("Possible Combo:", i + 1, good[i])
            print("i value")
            print(i)
            print(type(good))

            team1Score = 0
            team2Score = 0

            print("team 1")
            team1 = good[i][0]
            print("team 2")
            team2 = good[i][1]

            for playerLoop in team1:
                print("Team 1")
                print(players[playerLoop])
                team1Score += players[playerLoop]['Score']
                print(team1Score)

            for playerLoop in team2:
                print("Team 2")
                print(players[playerLoop])
                team2Score += players[playerLoop]['Score']
                print(team2Score)

            teamDiff = abs(team1Score - team2Score)
            if(teamDiff < lowestTeamDiff):
                lowestTeamDiff = teamDiff
                bestTeam1 = team1
                bestTeam2 = team2
                bestTeam1Score = team1Score
                bestTeam2Score = team2Score


            print(lowestTeamDiff)

        team1Names = []
        team2Names = []
        for name in bestTeam1:
            team1Names.append(players[name]['Name'])
        for name in bestTeam2:
            team2Names.append(players[name]['Name'])

        print("Best Team 1")
        print(team1Names)

        print("Best Team 2")
        print(team2Names)

        return team1Names, team2Names, bestTeam1Score, bestTeam2Score

    async def writeTeamOutput(self, ctx, team1, team2):
        message_channel = ctx.channel
        await message_channel.send("Team 1")
        await message_channel.send(team1)
        await message_channel.send("Team 2")
        await message_channel.send(team2)



    # Method will parse users from discord message and create a new array with our targets
    def parseUsers(self, mentions):
        global steamIDs
        usersToBalance = []
        usersToBalanceDict = []

        for mention in mentions:
            usersToBalance.append(mention.id)
            print(mention.id)

        # Add for testing
        for key in steamIDs:
            key = int(key)
            if key in usersToBalance:
                usersToBalanceDict.append(steamIDs[str(key)])

        # usersToBalanceDict.append(steamIDs[str(132009017215025153)])
        # usersToBalanceDict.append(steamIDs[str(183311683555426304)])
        print("here")
        print(usersToBalanceDict)
        print("here")

        return usersToBalanceDict

class PlayerSanitised:
    name = None
    score = False

    # def __init__(self, name, score ):
    #         PlayerSanitised.name = name
    #         PlayerSanitised.score = score

bot.run(TOKEN)



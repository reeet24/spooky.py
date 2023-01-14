import os
import discord
from discord.ext import commands
import random
import datetime
import time
import json
#from quart import Quart, render_template, redirect, url_for
#from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
#from nextcord.ext import ipc
#import nextcord
from UtilsDirectory.token import getSP

secret_token = getSP("token")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$',intents=intents)

async def log(cmd,user,arg,guild):
    print(str(datetime.datetime.now()) + ": " + user + " used: " + cmd + " with " + arg + " In " + guild)
    with open('logs/useLog.txt', 'a') as f:
        f.write(str(datetime.datetime.now()) + ": " + user + " used: " + cmd + " with " + arg + " In " + guild + "\n")

sp_prefix = "$"
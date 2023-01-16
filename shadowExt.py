from typing import final

from discord import Attachment
from UtilsDirectory.data import *

async def sblog(logType,user,msg,guild):
    print(str(datetime.datetime.now()) + ": " + logType + ": " + user + " said: " + msg)
    with open('logs/' + guild + '_Log.txt', 'a') as f:
        f.write(str(datetime.datetime.now()) + ": " + user + " said: " + msg + "\n")

async def updateSb():
    f = open('UtilsDirectory/shadow_bans.txt', 'w')
    for item in shadowList:
        f.write(item)
    f.close()

async def readSb():
    f = open('UtilsDirectory/shadow_bans.txt', 'r')
    shadowList = f.read()
    f.close()
    print(shadowList)

async def updateWhitelist():
    f = open('UtilsDirectory/whitelist.txt', 'w')
    for item in users:
        f.write(item)
    f.close()

async def readWhitelist():
    f = open('UtilsDirectory/whitelist.txt', 'r')
    users = f.read()
    f.close()
    print(users)

users = []
selfproxy = []
shadowList = []

class shadow(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        f = open('UtilsDirectory/shadow_bans.txt', 'r')
        shadowList = f.read()
        f.close()
        print(shadowList)
        f = open('UtilsDirectory/whitelist.txt', 'r')
        users = f.read()
        f.close()
        print(users)

    async def setup(bot):
        print('Commands loaded!')
    
    async def teardown(bot):
        print('Commands unloaded')

    @commands.Cog.listener()
    async def on_message(self,message):
        contents = message.content
        if (str(message.author.id)+"\n") in shadowList:
            try:
                await message.delete()
            except:
                await message.channel.send('Error exception: Could not send message')
            finally:
                await sblog("shadow ban",str(message.author.id),contents,str(message.guild.id))
        elif (str(message.author.id)) in selfproxy:
            await message.delete()
            if contents == None:
                await message.channel.send("couldn't send message")
            else:
                try:
                    await message.channel.send(contents)
                except:
                    await message.channel.send('Error exception: Could not send message')
                finally:
                    await sblog("proxy self",str(message.author.id),contents,str(message.guild.id))

    @commands.command()
    async def whitelist(self,ctx, user: discord.Member):
        if ctx.author.id == 643214257713971200:
            if (str(user.id) + "\n") not in users:
                users.append(str(user.id) + "\n")
                await ctx.send(f'<@' + (str(user.id)) + '> Has been added to the whitelist')
                print(users)
            elif (str(user.id) + "\n") in users:
                users.remove(str(user.id) + "\n")
                await ctx.send(f'<@' + (str(user.id)) + '> Has been removed from the whitelist')
                print(users)
            await updateWhitelist()
        else:
            await ctx.send(f"Sorry this command is only accessable to spooky")

    @commands.command()
    async def proxy_self(self,ctx):
        if ctx.author.id in selfproxy:
            await log("Proxy self",ctx.author.display_name,"Remove",str(ctx.message.guild.id))
            selfproxy.remove(str(ctx.author.id))
            await ctx.send(f'Done!')
        else:
            await log("Proxy self",ctx.author.display_name,"Add",str(ctx.message.guild.id))
            selfproxy.append(str(ctx.author.id))
            await ctx.send(f'Done!')


    @commands.command()
    async def shadow_ban(self,ctx, user: discord.Member):
        await log("Shadow Ban",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
        if ctx.author.id == 643214257713971200:
            if (str(user.id) + "\n") not in shadowList:
                shadowList.append(str(user.id) + "\n")
                await ctx.send(f'<@' + (str(user.id)) + '> Has been Shadowbanned')
                print(shadowList)
            elif (str(user.id) + "\n") in shadowList:
                shadowList.remove(str(user.id) + "\n")
                await ctx.send(f'<@' + (str(user.id)) + '> Has been Un-Shadowbanned')
                print(shadowList)
            await updateSb()
        else:
            await ctx.send(f"Sorry this command is only accessable to spooky")

    @commands.command( pass_context=True)
    async def server_sb_log(self, ctx):
        server = ctx.guild.id
        if ctx.author.id == 643214257713971200:
            await log("server log",ctx.author.display_name,"none",str(ctx.message.guild.id))
            await ctx.send(file=discord.File(r'logs/' + str(server) + '_Log.txt'))
        else:
            await ctx.send(f"Sorry this command is only accessable to spooky")

async def setup(bot):
    await bot.add_cog(shadow(bot)) 
import asyncio
from typing import final

from discord import Attachment
from UtilsDirectory.data import *

async def sblog(logType,user,msg,guild):
    print(str(datetime.datetime.now()) + ": " + logType + ": " + user + " said: " + msg)
    with open('logs/' + guild + '_Log.txt', 'a') as f:
        f.write(str(datetime.datetime.now()) + ": " + user + " said: " + msg + "\n")
    
def readServerWhitelist(serverId, level):
    if not os.path.exists(f'UtilsDirectory/servers/{serverId}.json'): return 0
    temp = []
    b = f'UtilsDirectory/servers/{serverId}.json'
    with open(b, "r") as f:
            SWL = json.load(f)
    f.close()
    TUsers = SWL["whitelist"]
    for lines in TUsers:
        if lines["level"] >= level:
            temp.append([lines["id"], lines["level"]])
    return temp

def readWhitelist(level):
    if not os.path.exists(f'UtilsDirectory/global_whitelist.json'): return 0
    temp = []
    b = f'UtilsDirectory/global_whitelist.json'
    with open(b, "r") as f:
            SWL = json.load(f)
    f.close()
    TUsers = SWL["users"]
    for lines in TUsers:
        if lines["level"] >= level:
            temp.append([lines["id"], lines["level"]])
    return temp

def addServerWhitelist(serverId, userId, level):
    serverInfo = readServerInfo(serverId)
    wList = serverInfo["whitelist"]
    temp = {
                "id": str(userId),
                "level": int(level)
            }
    wList.append(temp)

    with open(f'UtilsDirectory/servers/{serverId}.json', "w") as f:
        json.dump(serverInfo, f, indent=4)

    print('done')

def addWhitelist(userId, level):
    if not os.path.exists(f'UtilsDirectory/global_whitelist.json'): return 0
    b = f'UtilsDirectory/global_whitelist.json'
    with open(b, "r") as f:
            whitelist = json.load(f)
    f.close()
    wList = whitelist["users"]
    temp = {
                "id": str(userId),
                "level": int(level)
            }
    wList.append(temp)

    with open(f'UtilsDirectory/global_whitelist.json', "w") as f:
        json.dump(whitelist, f, indent=4)

    print('done')

def removeWhitelist(userId):
    if not os.path.exists(f'UtilsDirectory/global_whitelist.json'): return 0
    # Step 1: Read the server's info file to get the whitelist
    whitelist = readWhitelist(0)

    b = f'UtilsDirectory/global_whitelist.json'
    with open(b, "r") as f:
            SWL = json.load(f)
    f.close()

    # Step 2: Find the index of the user you want to remove
    index_to_remove = None
    for index, user_data in enumerate(whitelist):
        if user_data[0] == str(userId):
            index_to_remove = index
            break
    print(index_to_remove)
    if index_to_remove is not None:
        # Step 3: Remove the user from the whitelist
        removed_user = whitelist.pop(index_to_remove)
        SWL['users'] = whitelist
        print(f"Removed user {removed_user[0]} from the whitelist")

        with open(f'UtilsDirectory/global_whitelist.json', "w") as f:
            json.dump(SWL, f, indent=4)

    else:
        print(f"User with ID {userId} not found in the whitelist")

def findWhitelist(userId, level):
    if not os.path.exists(f'UtilsDirectory/global_whitelist.json'): return 0
    # Step 1: Read the server's info file to get the whitelist
    whitelist = readWhitelist(level)

    # Step 2: Find the index of the user you want to remove
    index_to_remove = None
    for index, user_data in enumerate(whitelist):
        if user_data[0] == str(userId):
            index_to_remove = index
            break
    print(index_to_remove)
    if index_to_remove is not None:
        # Step 3: Remove the user from the whitelist
        return 2

    else:
        print(f"User with ID {userId} not found in the whitelist")
        return 1

def removeServerWhitelist(serverId, userId):
    # Step 1: Read the server's info file to get the whitelist
    serverInfo = readServerInfo(serverId)
    whitelist = readServerWhitelist(serverId, 0)
    wList = serverInfo["whitelist"]

    # Step 2: Find the index of the user you want to remove
    index_to_remove = None
    for index, user_data in enumerate(whitelist):
        if user_data[0] == str(userId):
            index_to_remove = index
            break
    if index_to_remove is not None:
        # Step 3: Remove the user from the whitelist
        removed_user = wList.pop(index_to_remove)
        serverInfo["whitelist"] = wList

        # Step 4: Write the updated whitelist back to the server's info file using json.dump

        with open(f'UtilsDirectory/servers/{serverId}.json', "w") as f:
            json.dump(serverInfo, f, indent=4)

    else:
        print(f"User with ID {userId} not found in the whitelist")

def findServerWhitelist(serverId, userId, level):
    if not os.path.exists(f'UtilsDirectory/servers/{serverId}.json'): return 0
    serverInfo = readServerInfo(serverId)
    whitelist = readServerWhitelist(serverId, level)

    # Step 2: Find the index of the user you want to remove
    index_to_remove = None
    for index, user_data in enumerate(whitelist):
        if user_data[0] == str(userId):
            index_to_remove = index
            break
    print(index_to_remove)
    if index_to_remove is not None:
        return 2

    else:
        print(f"User with ID {userId} not found in the whitelist")
        return 1


async def readServerSb(serverId):
    if not os.path.exists(f'UtilsDirectory/servers/{serverId}.json'): return []
    temp = []
    b = f'UtilsDirectory/servers/{serverId}.json'
    with open(b, "r") as f:
            SWL = json.load(f)
    f.close()
    TUsers = SWL["shadow_bans"]
    for lines in TUsers:
        temp.append(lines)
    return temp

async def readSb():
    if not os.path.exists(f'UtilsDirectory/global_whitelist.json'): return 0
    temp = []
    b = f'UtilsDirectory/global_whitelist.json'
    with open(b, "r") as f:
            SWL = json.load(f)
    f.close()
    TUsers = SWL["shadow_bans"]
    for lines in TUsers:
        temp.append(lines)
    return temp

def readServerInfo(serverId):
    if not os.path.exists(f'UtilsDirectory/servers/{serverId}.json'): return 0
    b = f'UtilsDirectory/servers/{serverId}.json'
    with open(b, "r") as f:
            SWL = json.load(f)
    f.close()
    return SWL

def readGlobalInfo():
    if not os.path.exists(f'UtilsDirectory/global_whitelist.json'): return 0
    b = f'UtilsDirectory/global_whitelist.json'
    with open(b, "r") as f:
            SWL = json.load(f)
    f.close()
    return SWL

def addSb(userId, mode):
    serverInfo = readGlobalInfo()
    sblist = serverInfo["shadow_bans"]
    if mode == 1:
        sblist.append(userId)
    elif mode == 0:
        sblist.remove(userId)

    with open(f'UtilsDirectory/global_whitelist.json', "w") as f:
        json.dump(serverInfo, f, indent=4)

def addServerSb(serverId,userId, mode):
    serverInfo = readServerInfo(serverId)
    sblist = serverInfo["shadow_bans"]
    if mode == 1:
        sblist.append(userId)
    elif mode == 0:
        sblist.remove(userId)

    with open(f'UtilsDirectory/servers/{serverId}.json', "w") as f:
        json.dump(serverInfo, f, indent=4)

shadowList = []

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        shadowList.clear()

    async def setup(bot):
        print('Commands loaded!')
    
    async def teardown(bot):
        print('Commands unloaded')

    @commands.Cog.listener()
    async def on_message(self,message):
        contents = message.content
        server = message.guild.id
        shadowList = await readServerSb(server) + await readSb()
        if shadowList == 0: return
        if (message.author.id) in shadowList:
            try:
                await message.delete()
            except Exception as error:
                await message.channel.send(f'An exception occured: {error}')
            finally:
                await sblog("shadow ban",str(message.author.id),contents,str(message.guild.id))
        await bot.process_commands(message)

    @commands.command()
    async def checkPermissions(self, ctx, user: discord.Member, level = None):
        if not ctx.author.id == 643214257713971200: 
            await ctx.send("Not allowed to do that")
            return
        if level == None: level = 0
        b = findServerWhitelist(ctx.message.guild.id, user.id, level)
        await ctx.send(str(b))

    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason = None):
        """Bans user from the server"""
        a = findServerWhitelist(ctx.message.guild.id, ctx.author.id, 3)
        b = findWhitelist(ctx.author.id, 3)
        if (a == 2) or (b == 2):
            try:
                await log("ban",ctx.author.display_name,str(user),str(ctx.message.guild.id))
            except:
                await log("ban",ctx.author.display_name,"invalid user name",str(ctx.message.guild.id))
            finally:
                if not reason:
                    await user.ban()
                    await ctx.send(f"**{user}** has been banned for **no reason**.")
                else:
                    await user.ban(reason=reason)
                    await ctx.send(f"**{user}** has been banned for **{reason}**.")
        else:   
            await log("ban",ctx.author.display_name,"lol they tried",str(ctx.message.guild.id))
            await ctx.send('User is not whitelisted for this action')

    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason = None):
        """Kicks user from the server"""
        a = findServerWhitelist(ctx.message.guild.id, ctx.author.id, 3)
        b = findWhitelist(ctx.author.id, 3)
        if (a == 2) or (b == 2):
            await log("kick",ctx.author.display_name,str(user),str(ctx.message.guild.id))
            if not reason:
                await user.kick()
                await ctx.send(f"**{user}** has been kicked for **no reason**.")
            else:
                await user.kick(reason=reason)
                await ctx.send(f"**{user}** has been kicked for **{reason}**.")
        else:
            await log("Kick",ctx.author.display_name,"lol they tried",str(ctx.message.guild.id))
            await ctx.send('no')

    @commands.command()
    async def register_server(self,ctx):
        """Registers the server in the DB"""
        if not readServerInfo(ctx.message.guild.id) == 0:
            await ctx.send(f'Server with ID {ctx.message.guild.id} already registered')
            return

        print('Debug')
        
        owner = ctx.guild.owner_id
        #user = await client.fetch_user(user_id)

        print('Debug')

        temp = {
                    "owner": owner,
                    "whitelist": [
                    {
                        "id": str(owner),
                        "level": 4
                    }
                    ],
                    "shadow_bans": [
                    ]
                }

        print('Debug')

        with open(f"UtilsDirectory/servers/{ctx.message.guild.id}.json", "w") as f:
            json.dump(temp, f, indent=4)

        print('Debug')

        await ctx.send(f'Done!')
        await ctx.send(f'<@{owner}> Has been given owner permissions')

    @commands.command()
    async def global_whitelist(self,ctx, user: discord.Member, level = None):
        """Globaly whitelists user (Only Spooky.ico)"""
        if ctx.author.id == 643214257713971200:
            await log("Whitelist",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
            if level == None: level = 3
            a = findWhitelist(user.id, int(level))
            print(a)
            #serverId, userId, level, mode
            if a == 1:
                print('Test')
                addWhitelist(user.id,level)
                await ctx.send(f'<@' + (str(user.id)) + '> Has been Globally Whitelisted')
            elif a == 2:
                removeWhitelist(user.id)
                await ctx.send(f'<@' + (str(user.id)) + '> Has been Globally Un-Whitelisted')
        else:
            await ctx.send('User is not permitted to do action')

    @commands.command()
    async def whitelist(self,ctx,user: discord.Member, level = None):
        """Whitelists user serverside (Req whitelist)"""
        await log("Whitelist",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
        if level == None: level = 3
        a = findServerWhitelist(ctx.message.guild.id, ctx.author.id, 4)
        b = findServerWhitelist(ctx.message.guild.id, user.id, int(level))
        if a == 0: 
            await ctx.send("Your serverfile has not been set up yet. Please wait while the bot is finished")
            return
        elif a == 1:
            await ctx.send(f"Sorry this command is only accessable to whitelisted users")
            return
        
        #serverId, userId, level, mode
        if b == 1:
            addServerWhitelist(ctx.message.guild.id,user.id,level)
            await ctx.send(f'<@' + (str(user.id)) + '> Has been Whitelisted')
        elif b == 2:
            removeServerWhitelist(ctx.message.guild.id,user.id)
            await ctx.send(f'<@' + (str(user.id)) + '> Has been Un-Whitelisted')
        

    @commands.command()
    async def global_shadow(self,ctx, user: discord.Member):
        """Globally shadow bans user (Req global whitelist)"""
        await log("Global Shadow Ban",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
        a = findWhitelist(ctx.author.id, 2)
        if a == 1:
            await ctx.send(f"Sorry this command is only accessable to whitelisted users")
            return

        c = await readSb()
        if (user.id) not in c:
            await addSb(user.id,1)
            await ctx.send(f'<@' + (str(user.id)) + '> Has been Shadowbanned')
        elif (user.id) in c:
            await addSb(user.id,0)
            await ctx.send(f'<@' + (str(user.id)) + '> Has been Un-Shadowbanned')



    @commands.command()
    async def shadow_ban(self,ctx, user: discord.Member):
        """Shadow bans user serverside (Req whitelist)"""
        await log("Shadow Ban",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
        a = readServerWhitelist(str(ctx.message.guild.id), 3)
        if a == 0: 
            await ctx.send("Your serverfile has not been set up yet. Please wait while the bot is finished")
            return
        
        if a == 1:
            await ctx.send(f"Sorry this command is only accessable to whitelisted users")
            return

        c = await readServerSb(ctx.message.guild.id)
        if (user.id) not in c:
            await addServerSb(ctx.message.guild.id,user.id,1)
            await ctx.send(f'<@' + (str(user.id)) + '> Has been Shadowbanned')
        elif (user.id) in c:
            await addServerSb(ctx.message.guild.id,user.id,0)
            await ctx.send(f'<@' + (str(user.id)) + '> Has been Un-Shadowbanned')

    @commands.command( pass_context=True)
    async def server_sb_log(self, ctx):
        """Sends server shadow ban logs (Req whitelist)"""
        server = ctx.guild.id
        a = readServerWhitelist(str(ctx.message.guild.id), 2)
        if a == 1:
            await ctx.send(f"Sorry this command is only accessable to whitelisted users")
            
        await log("server log",ctx.author.display_name,"none",str(ctx.message.guild.id))
        await ctx.send(file=discord.File(r'logs/' + str(server) + '_Log.txt'))
            
async def setup(bot):
    await bot.add_cog(Moderation(bot)) 
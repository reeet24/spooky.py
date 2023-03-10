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
    shadowList.clear()
    f = open('UtilsDirectory/shadow_bans.txt', 'r')
    for lines in f:
        shadowList.append(lines)
    f.close()

async def updateWhitelist():
    f = open('UtilsDirectory/whitelist.txt', 'w')
    for item in users:
        f.write(item)
    f.close()

async def readWhitelist():
    users.clear()
    b = open('UtilsDirectory/whitelist.txt', 'r')
    for lines in b:
        users.append(lines)
    b.close()

users = []
selfproxy = []
shadowList = []

class shadow(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        shadowList.clear()
        f = open('UtilsDirectory/shadow_bans.txt', 'r')
        for lines in f:
            shadowList.append(lines)
        f.close()
        b = open('UtilsDirectory/whitelist.txt', 'r')
        for lines in b:
            users.append(lines)
        b.close()

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
            elif contents == "$proxy_self":
                print(selfproxy)
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
                await readWhitelist()
                users.append(str(user.id) + "\n")
                await ctx.send(f'<@' + (str(user.id)) + '> Has been added to the whitelist')
                await log("Whitelist",ctx.author.display_name,"Add",str(user.id))
            elif (str(user.id) + "\n") in users:
                users.remove(str(user.id) + "\n")
                await ctx.send(f'<@' + (str(user.id)) + '> Has been removed from the whitelist')
                await log("Whitelist",ctx.author.display_name,"Remove",str(user.id))
            await updateWhitelist()
        else:
            await ctx.send(f"Sorry this command is only accessable to spooky")

    @commands.command()
    async def id(self,ctx,user: discord.member):
        await ctx.send(f'Debug')
        await ctx.send(str(user.id))

    @commands.command()
    async def proxy_self(self,ctx):
        if str(ctx.author.id) in selfproxy:
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
        if (str(ctx.author.id)+"\n") in users:
            if (str(user.id) + "\n") not in shadowList:
                shadowList.append(str(user.id) + "\n")
                await ctx.send(f'<@' + (str(user.id)) + '> Has been Shadowbanned')
                print(shadowList)
            elif (str(user.id) + "\n") in shadowList:
                shadowList.remove(str(user.id) + "\n")
                await ctx.send(f'<@' + (str(user.id)) + '> Has been Un-Shadowbanned')
                print(shadowList)
            await updateSb()
            await readSb()
        else:
            await ctx.send(f"Sorry this command is only accessable to whitelisted users")

    @commands.command( pass_context=True)
    async def server_sb_log(self, ctx):
        server = ctx.guild.id
        if (str(ctx.author.id)+"\n") in users:
            await log("server log",ctx.author.display_name,"none",str(ctx.message.guild.id))
            await ctx.send(file=discord.File(r'logs/' + str(server) + '_Log.txt'))
        else:
            await ctx.send(f"Sorry this command is only accessable to whitelisted users")

    @commands.command( pass_context=True)
    async def vault(self, ctx, action = None, filename = None):
        if action == 'store':
            if (str(ctx.author.id)+"\n") in users:
                if ctx.message.attachments:
                    for attachment in ctx.message.attachments:
                        url = attachment.url
                        response = requests.get(url)
                        with open(f'vault/{attachment.filename}', "wb") as f:
                            f.write(response.content)
                    await ctx.send("File downloaded successfully!")
                await log("vault",ctx.author.display_name,"store",str(ctx.message.guild.id))
            else:
                await ctx.send(f"Sorry this command is only accessable to whitelisted users")
        elif action == 'retrieve':
            file_path = None
            for f in os.listdir("vault"):
                if f == filename:
                    file_path = os.path.join("vault", f)
                    break
            if file_path is None:
                await ctx.send(f"No file with name {filename} found in the vault directory!")
            else:
                with open(file_path, "rb") as f:
                    file = discord.File(f)
                    await ctx.send(file=file)
            await log("vault",ctx.author.display_name,"retrieve",str(ctx.message.guild.id))
        elif action == "list":
            files = os.listdir("vault")
            if len(files) == 0:
                await ctx.send("The vault directory is empty!")
            else:
                file_list = "\n".join(files)
                await ctx.send(f"Files in the vault directory:```\n{file_list}```")
            await log("vault",ctx.author.display_name,"list",str(ctx.message.guild.id))
        elif action == None:
            await ctx.send(f'Invalid args')

async def setup(bot):
    await bot.add_cog(shadow(bot)) 
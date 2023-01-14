from typing import final

from discord import Attachment
from UtilsDirectory.data import *

async def sblog(logType,user,msg,guild):
    print(str(datetime.datetime.now()) + ": " + logType + ": " + user + " said: " + msg)
    with open('logs/' + guild + '_Log.txt', 'a') as f:
        f.write(str(datetime.datetime.now()) + ": " + user + " said: " + msg + "\n")


users = []
repeatlist = []
proxylist = []
selfproxy = []

class shadow(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def setup(bot):
        print('Commands loaded!')
    
    async def teardown(bot):
        print('Commands unloaded')

    @commands.Cog.listener()
    async def on_message(self,message):
        contents = message.content
        with open('UtilsDirectory/shadow_bans.txt') as f:
            users = f.readlines()
            f.close()
        with open('UtilsDirectory/proxy_list.txt') as p:
            proxylist = p.readlines()
            p.close()
        if (str(message.author.id)+"\n") in users:
            try:
                await message.delete()
            except:
                await message.channel.send('Error exception: Could not send message')
            finally:
                await sblog("shadow ban",str(message.author.id),contents,str(message.guild.id))
        elif (str(message.author.id)) in repeatlist:
            try:
                await message.channel.send(contents)
            except:
                await message.channel.send('Error exception: Could not send message')
            finally:
                await sblog("repeat",str(message.author.id),contents,str(message.guild.id))
        elif (str(message.author.id)+'\n') in proxylist:
            await message.delete()
            if contents == None:
                await message.channel.send("couldn't send message")
            else:
                try:
                    await message.channel.send(contents)
                except:
                    await message.channel.send('Error exception: Could not send message')
                finally:
                    await sblog("proxy",str(message.author.id),contents,str(message.guild.id))
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
        #elif (message.author.id == 1014023330262691880):
        #   await message.channel.send("I like Cock lol")

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
    async def proxy(self,ctx, user: discord.Member):
        await log("Proxy",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
        if ctx.author.id == 643214257713971200:
            with open('UtilsDirectory/proxy_list.txt', 'a') as p:
                p.write(str(user.id) + "\n")
                p.close()
            await ctx.send(f'done')
            p.close()
        else:
            await ctx.send(f"Sorry this command is only accessable to spooky")

    @commands.command()
    async def repeat(self,ctx, user: discord.Member):
        await log("Repeat",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
        if ctx.author.id == 643214257713971200 :
            repeatlist.append(str(user.id))
            await ctx.send(f'done')
        else:
            await ctx.send(f"Sorry this command is only accessable to spooky")

    @commands.command()
    async def rp_remove(self,ctx,user: discord.member):
        await log("Repeat remove",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
        if ctx.author.id == 643214257713971200:
            if str(user.id) in repeatlist:
                repeatlist.append(str(user.id))
                await ctx.send(f'Done!')
            else:
                await ctx.send(f'User not found in list')
        else:
            await ctx.send(f"Sorry this command is only accessable to spooky")

    @commands.command()
    async def shadow_ban(self,ctx, user: discord.Member):
        await log("Shadow Ban",ctx.author.display_name,str(user.id),str(ctx.message.guild.id))
        if ctx.author.id == 643214257713971200:
            with open('UtilsDirectory/shadow_bans.txt', 'a') as asf:
                asf.write(str(user.id) + "\n")
            await ctx.send(f'done')
            asf.close()
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
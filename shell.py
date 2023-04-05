from UtilsDirectory.data import *

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
cwd = 'home/'
lwd = 'home/'

class shell(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        users.clear()
        b = open('UtilsDirectory/whitelist.txt', 'r')
        for lines in b:
            users.append(lines)
        b.close()

    async def setup(bot):
        print('Commands loaded!')
    
    async def teardown(bot):
        print('Commands unloaded')

#    @commands.command()
#    async def shTest(self,ctx):
#        print(f'Test passed')
#        await ctx.send(f'Test passed')

    @commands.command()
    async def cd(self, ctx, directory = None):
        print(f'"{cwd}" Is the current Directory\n"{lwd}" Is the last used directory')
        if directory == None:
            await ctx.send(f'Invalid syntax')
        else:
            cwd =+ directory
            print(cwd)
            await ctx.send(cwd)

async def setup(bot):
    await bot.add_cog(shell(bot))
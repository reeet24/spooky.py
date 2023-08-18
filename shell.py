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

    @commands.command()
    async def r34(self,ctx,tag1 = None, tag2 = None, tag3 = None, tag4 = None):
        tagList = []

        if not tag1 == None: tags.append(tag1)
        if not tag2 == None: tags.append(tag2)
        if not tag3 == None: tags.append(tag3)
        if not tag4 == None: tags.append(tag4)

        r = requests.get(f'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index', limit=(1), tags=(tagList))
        print(r)
        await ctx.send(r)

async def setup(bot):
    await bot.add_cog(shell(bot))
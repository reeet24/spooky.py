from UtilsDirectory.data import *

def updateWhitelist():
    f = open('UtilsDirectory/whitelist.txt', 'w')
    for item in users:
        f.write(item)
    f.close()

def readWhitelist():
    users.clear()
    b = open('UtilsDirectory/whitelist.txt', 'r')
    for lines in b:
        users.append(lines)
    b.close()

def get_comms_list(user_id):
    # Get the user's inventory, or create a new one if it doesn't exist
    comms_file = f"commission_invs/{str(user_id)}.json"
    if os.path.exists(comms_file):
        print('Check 1')
        with open(comms_file, "r") as f:
            print('Check 2')
            comms_list = json.load(f)
            return comms_list
    else:
        print('fuck')
    

users = []


class coms(commands.Cog):
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

    @commands.command()
    async def artist_add(self, ctx, user: discord.member):
        if ctx.author.id() == 643214257713971200:
            print('Help?')
            comms_list = get_comms_list(str(user.id()))
            await ctx.send(comms_list)
            print(comms_list)



async def setup(bot):
    await bot.add_cog(coms(bot))
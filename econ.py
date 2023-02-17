from UtilsDirectory.data import *

class econ(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def setup(bot):
        print('Econ loaded!')
    
    async def teardown(bot):
        print('Econ unloaded')

async def setup(bot):
    await bot.add_cog(econ(bot))
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

class vaulting(commands.Cog):
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

    @commands.command( pass_context=True)
    async def vault(self, ctx, action = None, filename = None):
        await readWhitelist()
        if action == 'store':
            if (str(ctx.author.id)+"\n") in users:
                if ctx.message.attachments:
                    for attachment in ctx.message.attachments:
                        if not os.path.exists("vault"):
                            os.mkdir("vault")
                        try:
                            await attachment.save(f"vault/{attachment.filename}")
                            await ctx.send(f"Image {attachment.filename} has been saved!")
                        except Exception as e:
                            await ctx.send(f'Error: {e}\n')
                    await ctx.message.delete()
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
            await ctx.message.delete()
            await log("vault",ctx.author.display_name,"retrieve",str(ctx.message.guild.id))
        elif action == "retMe":
            file_path = None
            for f in os.listdir("vault"):
                if f == filename:
                    file_path = os.path.join("vault", f)
                    break
            if file_path is None:
                await ctx.author.send(f"No file with name {filename} found in the vault directory!")
            else:
                with open(file_path, "rb") as f:
                    file = discord.File(f)
                    await ctx.author.send(file=file)
            await ctx.message.delete()
            await log("vault",ctx.author.display_name,"retMe",str(ctx.message.guild.id))
        elif action == "list":
            files = os.listdir("vault")
            if len(files) == 0:
                await ctx.send("The vault directory is empty!")
            else:
                file_list = "\n".join(files)
                await ctx.send(f"Files in the vault directory:```\n{file_list}```")
            await log("vault",ctx.author.display_name,"list",str(ctx.message.guild.id))
        else:
            await ctx.send(f'Invalid args')


async def setup(bot):
    await bot.add_cog(vaulting(bot))
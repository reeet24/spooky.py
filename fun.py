from UtilsDirectory.data import *

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx, arg = None):
        await log("say",ctx.author.display_name,arg,str(ctx.message.guild.id))
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command()
    async def sayDm(self, ctx, user: discord.Member, arg = None):
        await log("say",ctx.author.display_name,arg,str(ctx.message.guild.id))
        await ctx.message.delete()
        await user.send(arg)
    
    @commands.command()
    async def roshambo(self, ctx,*,choice = None):
        aiChoose = ["rock","paper","scissors"]
        aiChoice = random.choice(aiChoose)
        if choice == None:
            await ctx.send(f'type rock, paper, or scissors')
        elif choice == "rock":
            await ctx.send(f'my choice is: ' + aiChoice)
            if aiChoice == "rock":
                await ctx.send(f'Tie')
            elif aiChoice == "paper":
                await ctx.send(f'I win')
            elif aiChoice == 'scissors':
                await ctx.send(f'I lose')
        elif choice == "paper":
            await ctx.send(f'my choice is: ' + aiChoice)
            if aiChoice == "rock":
                await ctx.send(f'I lose')
            elif aiChoice == "paper":
                await ctx.send(f'Tie')
            elif aiChoice == 'scissors':
                await ctx.send(f'I win')
        elif choice == "scissors":
            await ctx.send(f'my choice is: ' + aiChoice)
            if aiChoice == "rock":
                await ctx.send(f'I win')
            elif aiChoice == "paper":
                await ctx.send(f'I lose')
            elif aiChoice == 'scissors':
                await ctx.send(f'Tie')

    @commands.command(pass_context=True)
    async def use_log(self, ctx):
        if ctx.author.id == 643214257713971200:
            await log("use log",ctx.author.display_name,"none",str(ctx.message.guild.id))
            await ctx.send(file=discord.File(r'logs/useLog.txt'))
        else:
            await ctx.send(f"Sorry this command is only accessable to spooky")
    
async def setup(client):
    await client.add_cog(Fun(client))
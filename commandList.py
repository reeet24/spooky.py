from UtilsDirectory.data import *

async def setup(bot):
    print('Commands loaded!')
    
async def teardown(bot):
    print('Commands unloaded')

@commands.command()
async def hello(ctx):
    await log("hello",ctx.author.display_name,"none",str(ctx.message.guild.id))
    await ctx.send(f'Hello {ctx.author.display_name}.')

@commands.command()
async def say(ctx, arg = None):
    await log("say",ctx.author.display_name,arg,str(ctx.message.guild.id))
    await ctx.message.delete()
    await ctx.send(arg)

@commands.command()
async def sayDm(ctx, user: discord.Member, arg = None):
    await log("say",ctx.author.display_name,arg,str(ctx.message.guild.id))
    await ctx.message.delete()
    await user.send(arg)

@commands.command()
async def git(ctx, message_id: int):
    message = await ctx.channel.fetch_message(message_id)
    for attachment in message.attachments:
        if not os.path.exists("git"):
            os.mkdir("git")
        try:
            await attachment.save("git")
            await ctx.send(f"Image {attachment.filename} has been saved!")
        except Exception as e:
            await ctx.send(f'Error: {e}\n')
        

@commands.command()
async def help_me(ctx, index = None):
    await log("help",ctx.author.display_name,str(index),str(ctx.message.guild.id))
    if index == "mod":
        await ctx.send(f'```\nKick: Self Explanitory just ping someone after the command and boom\nBan: Same as kick\nNothing else yet :P\n```')
    elif index == "fun":
        await ctx.send(f'```\nHello: Says hello thats it\nSay: Says what ever you said after the command (use quotes)\nGit: WIP command\nRoshambo: The classic game of roshambo\nno more :P\n```')
    elif index == "spooky":
        await ctx.send(f"```\nRepeat: Makes the bot repeat whoever spooky wants\nShadow ban: Sends you the the backrooms\nProxy: Like shadow ban but a little better\nLog commands: Y'all don't need to know about that :P\n```")
    elif index == None:
        await ctx.send(f'```\nSyntax is $help_me (the index of the help commands)\n```')
        await ctx.send(f'```\nList of Indexes\nmod: displays the mod commands\nfun: Displays the fun commands\nspooky: Displays commands only spooky can use :P\n```')


@commands.command()
async def kick(ctx, user: discord.Member, *, reason = None):
    if ctx.author.id == 643214257713971200:
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
async def ban(ctx, user: discord.Member, *, reason = None):
    if ctx.author.id == 643214257713971200:
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
        await ctx.send('no')
    
@commands.command()
async def roshambo(ctx,*,choice = None):
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
async def use_log(ctx):
    if ctx.author.id == 643214257713971200:
        await log("use log",ctx.author.display_name,"none",str(ctx.message.guild.id))
        await ctx.send(file=discord.File(r'logs/useLog.txt'))
    else:
        await ctx.send(f"Sorry this command is only accessable to spooky")
    
async def setup(bot):
    bot.add_command(hello)
    bot.add_command(say)
    bot.add_command(sayDm)
    bot.add_command(git)
    bot.add_command(help_me)
    bot.add_command(kick)
    bot.add_command(ban)
    bot.add_command(roshambo)
    bot.add_command(use_log)
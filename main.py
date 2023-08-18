from UtilsDirectory.data import *

@bot.event
async def on_ready():

    game = discord.Game("$help_me")
    await bot.change_presence(status=discord.Status.online, activity=game)

    await bot.load_extension('shadowExt')
    await bot.load_extension('comms')
    await bot.load_extension('commandList')
    await bot.load_extension('econ')
    await bot.load_extension('vaulting')
    await bot.load_extension('shell')
    print(f'We have logged in as {bot.user}')

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f'Pong! `{round(bot.latency * 1000)}ms`')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, that command was not found.")

@bot.command()
async def reload(ctx, choice = None):

    if choice == None:
        await ctx.send(f'Please choose which file to reload')
    elif choice == 'shadow':
        await bot.reload_extension('shadowExt')
        await ctx.send('Reloaded!')
    elif choice == 'general':
        await bot.reload_extension('commandList')
        await ctx.send('Reloaded!')
    elif choice == 'econ':
        await bot.reload_extension('econ')
        await ctx.send(f'Reloaded!')
    elif choice == 'all':
        await bot.reload_extension('shadowExt')
        await bot.reload_extension('comms')
        await bot.reload_extension('commandList')
        await bot.reload_extension('econ')
        await bot.reload_extension('vaulting')
        await bot.reload_extension('shell')
        await ctx.send('Reloaded!')
    else:
        await ctx.send('Invalid Args')


bot.run(secret_token)
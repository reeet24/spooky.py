from UtilsDirectory.data import *

@bot.event
async def on_ready():

    game = discord.Game("$help_me")
    await bot.change_presence(status=discord.Status.online, activity=game)

    await bot.load_extension('shadowExt')
    await bot.load_extension('commandList')
    print(f'We have logged in as {bot.user}')

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
    elif choice == 'all':
        await bot.reload_extension('shadowExt')
        await bot.reload_extension('commandList')
        await ctx.send('Reloaded!')
    else:
        await ctx.send('Invalid Args')


bot.run(secret_token)
import discord
import json
#extra directories
from discord.ext import commands
from host import host

intents = discord.Intents.default()
intents.members = True

def getprefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]

bot = commands.Bot(command_prefix=getprefix, intents=intents)
bot.remove_command('help')

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send('{0}ms'.format(round(bot.latency * 1000)))
    



host()
bot.run('ODkzMDM2MDQ0MjQzNTk1MzM1.YVVmoA.E1U2ZzRoHCM9O3Lh9VcMhykKgKg')

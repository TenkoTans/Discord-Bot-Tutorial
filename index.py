import discord
import json
#extra directories
from discord.ext import commands
from host import host
from commands.levels import levels

intents = discord.Intents.default()
intents.members = True

def getprefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]

bot = commands.Bot(command_prefix=getprefix, intents=intents)
bot.remove_command('help')

#events
@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')

#extra commands
@bot.command(pass_context=True, aliases=['setprefix'])
@commands.has_permissions(administrator = True)
async def prefix(ctx, pref):
  with open("prefixes.json", "r") as f:
    prefix = json.load(f)
  prefix[str(ctx.guild.id)] = pref
  with open("prefixes.json", "w") as f:
    json.dump(prefix, f, indent=4)
  await ctx.send(f"Prefix has been changed to {pref}")

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send('{0}ms'.format(round(bot.latency * 1000)))
    
#commands



host()
bot.run('ODkzMDM2MDQ0MjQzNTk1MzM1.YVVmoA.E1U2ZzRoHCM9O3Lh9VcMhykKgKg')

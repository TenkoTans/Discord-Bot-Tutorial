import discord
import json
#extra directories
from discord.ext import commands
from host import host
from commands import levels, economy, music, moderation

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

@bot.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)

    if payload.member.bot:
        return
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = bot.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                await payload.member.add_roles(role)
                await payload.member.send(f"**{guild.name}** : You have been given the {selected_role} role!")

@bot.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(
                emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = bot.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                member = await(guild.fetch_member(payload.user_id))
                if member is not None:
                    await member.remove_roles(role)

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
    
loopevent = threading.Event()

@bot.command(pass_context=True)
async def stick(ctx, *, message):
  try:
    stickyMessageContent = message
    while not loopevent.is_set():
      await ctx.send(stickyMessageContent, delete_after=15.0);
      await asyncio.sleep(15)
  except:
    print("error")

@bot.command(pass_context=True)
async def unstick(ctx):
  stickyMessageContent = "";
  loopevent.set()
    
#commands



host()
bot.run('ODkzMDM2MDQ0MjQzNTk1MzM1.YVVmoA.E1U2ZzRoHCM9O3Lh9VcMhykKgKg')

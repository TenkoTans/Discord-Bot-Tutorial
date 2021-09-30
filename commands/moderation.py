import discord
import asyncio
from discord.ext import commands

async def ban(ctx, member:discord.User=None, reason =None):
    if member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    if reason == None:
        message = f"You have been banned from {ctx.guild.name}, No reason provided"
    if reason != None:
        message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    await member.ban(reason=message)

async def unban(ctx, bot: commands.Bot, id:int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)

async def kick(ctx, member:discord.User=None, reason =None):
    if member == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself")
        return
    if reason == None:
        message = f"You have been kicked from {ctx.guild.name}, No reason provided"
    if reason != None:
        message = f"You have been kicked from {ctx.guild.name} for {reason}"
    await member.send(message)
    await member.kick(reason=message)

async def purge(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.message.delete()

async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

async def mute(ctx, user : discord.Member, duration = 0,*, unit = None):
    roleobject = discord.utils.get(ctx.guild.roles, name="Muted")
    if not roleobject:
            muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted, send_messages=False)
            await user.add_roles(muted)
    if roleobject:
      await user.add_roles(roleobject)
    try:
      if unit == "s" or "seconds":
        await asyncio.sleep(duration)
      if unit == "m" or "minutes":
        await asyncio.sleep(duration*60)
      if unit == "h" or "hour":
        await asyncio.sleep(duration*60*60)
      await user.remove_roles(roleobject)
    except:
      await ctx.send('unable to execute command')

async def unmute(ctx, user : discord.Member):
    roleobject = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.remove_roles(roleobject)

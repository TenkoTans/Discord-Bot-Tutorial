import discord
import asyncio
import json

async def self_role(bot, ctx):
    questions = ["Enter Message Content: ", "Enter Emojis: ", "Enter Roles: ", "Enter Channel: ", "Message Content Title:"]
    answers = []

    def check(user):
        return user.author == ctx.author and user.channel == ctx.channel
    
    for question in questions:
      embed = discord.Embed(title='Reaction Roles', color=0x465B73)
      embed.add_field(name='Question', value=question, inline=False)
      await ctx.send(embed=embed)

      try:
        msg = await bot.wait_for('message', timeout=120.0, check=check)
      except asyncio.TimeoutError:
        await ctx.send("Timeout Error, Please Try Again")
        return
      else:
        answers.append(msg.content)

    emojis = answers[1].split(" ")
    roles = answers[2].split(", ")
    c_id = int(answers[3][2:-1])
    title = answers[4]
    channel = bot.get_channel(c_id)

    embed1 = discord.Embed(title=f'{title}', color=0x465B73)
    embed1.add_field(name='React to give yourself a role.', value=answers[0], inline=False)

    bot_msg = await channel.send(embed=embed1)

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)

    self_roles[str(bot_msg.id)] = {}
    self_roles[str(bot_msg.id)]["emojis"] = emojis
    self_roles[str(bot_msg.id)]["roles"] = roles

    with open("selfrole.json", "w") as f:
        json.dump(self_roles, f)

    for emoji in emojis:
        await bot_msg.add_reaction(emoji)

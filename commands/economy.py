import discord
import random
import json
from discord.ext import commands


async def get_bankdata():
  with open('bankholder.json', 'r') as f:
    users = json.load(f)
  return users

async def openbank(user):
  users = await get_bankdata()
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0

  with open('bankholder.json', 'w') as f:
    json.dump(users, f)
  return True

async def update_bank(user, change = 0, mode = "wallet"):
  users = await get_bankdata()
  users[str(user.id)][mode] += change
  with open("bankholder.json", "w") as f:
    json.dump(users, f)
  bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
  return bal

async def balance(ctx, member: discord.Member = None):
  if member == None:
    member = ctx.author
  else:
    member = member
  await openbank(member)
  users = await get_bankdata()
  wallet_balance = users[str(member.id)]["wallet"]
  bank_balance = users[str(member.id)]["bank"]
  embed = discord.Embed(title = f"{member.name}'s Balance",color = discord.Color(0x465B73))
  embed.add_field(name="Wallet Amount", value=f"{wallet_balance} Tenkoins", inline=False)
  embed.add_field(name="Bank Amount", value=f"{bank_balance} Tenkoins", inline=False)
  await ctx.send(embed=embed)

async def beg(ctx):
    await openbank(ctx.author)
    users = await get_bankdata()
    earnings = random.randrange(80)
    await ctx.send(f"someone gave you {earnings} Tenkoins")
    users[str(ctx.author.id)]["wallet"] += earnings
    with open('bankholder.json', 'w') as f:
      json.dump(users, f)

async def work(ctx):
  await openbank(ctx.author)
  users = await get_bankdata()
  earnings = random.randrange(300)
  await ctx.send(f"you were paid {earnings} Tenkoins for working")
  users[str(ctx.author.id)]["wallet"] += earnings
  with open('bankholder.json', 'w') as f:
    json.dump(users, f)

async def crime(ctx):
  await openbank(ctx.author)
  users = await get_bankdata()
  earnings = random.randrange(800)
  rand = random.randrange(10)
  if rand<4:
    await ctx.send(f"you commit a crime and got yourself {earnings} Tenkoins")
    users[str(ctx.author.id)]["wallet"] += earnings
  else:
    await ctx.send(f"you were caught commiting a crime and the fine cost you 1000 Tenkoins from your wallet")
    users[str(ctx.author.id)]["wallet"] -= 1000
  with open('bankholder.json', 'w') as f:
    json.dump(users, f)

async def deposit(ctx, amount = None):
  await openbank(ctx.author)
  bal = await update_bank(ctx.author)
  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("you do not have enough money to deposit")
    return
  await update_bank(ctx.author, amount, "bank")
  await update_bank(ctx.author, -1*amount)
  await ctx.send(f"deposited {amount} Tenkoins into Bank")

async def withdraw(ctx, amount = None):
  await openbank(ctx.author)
  bal = await update_bank(ctx.author)
  amount = int(amount)
  if amount>bal[1]:
    await ctx.send("you do not have enough money to withdraw")
    return
  await update_bank(ctx.author, amount)
  await update_bank(ctx.author, -1*amount, "bank")
  await ctx.send(f"withdrew {amount} Tenkoins into Wallet")

async def give(ctx, member: discord.Member = None, amount = None):
  await openbank(ctx.author)
  await openbank(member)
  bal = await update_bank(ctx.author)
  amount = int(amount)
  if member == ctx.author:
    await ctx.send("you cannot give yourself money")
    return
  if amount>bal[0]:
    await ctx.send("you do not have enough money to give")
    return
  if amount<0:
    await ctx.send("you cannot give a negative value")
    return
  if bal[0]<0:
    await ctx.send("you do not have enough money to give")
    return
  await update_bank(ctx.author, -1*amount)
  await update_bank(member, amount)
  await ctx.send(f"gave {amount} Tenkoins to {member}")

async def add(ctx, member: discord.Member, amount = None):
  if member == None:
     member = ctx.author
  await openbank(member)
  amount = int(amount)
  await update_bank(member, amount)
  await ctx.send(f"added {amount} Tenkoins to {member.name}'s Wallet")

async def remove(ctx, member: discord.Member, amount = None):
  if member == None:
     member = ctx.author
  await openbank(member)
  amount = int(amount)
  await update_bank(member, -1*amount)
  await ctx.send(f"removed {amount} Tenkoins to {member.name}'s Wallet")

async def gamble(ctx, amount = None):
  await openbank(ctx.author)
  bal = await update_bank(ctx.author)
  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("you do not have enough money to gamble")
    return
  if amount<0:
    await ctx.send("you cannot gamble negatives")
    return
  await update_bank(ctx.author, -1*amount)
  if ctx.author.id == 782492200587362315:
    gamble = random.randint(1, 10)
    if gamble<6:
     await update_bank(ctx.author, 2*amount)
     await ctx.send(f"you have won {2*amount} Tenkoins")
    else:
     await ctx.send(f"you have lost {amount} Tenkoins")
  else:
    gamble = random.randint(1, 10)
    if gamble<4:
     await update_bank(ctx.author, 2*amount)
     await ctx.send(f"you have won {2*amount} Tenkoins")
    else:
     await ctx.send(f"you have lost {amount} Tenkoins")

async def rob(ctx, member: discord.Member = None):
  await openbank(ctx.author)
  await openbank(member)
  bal = await update_bank(member)
  if bal[0]<50:
    await ctx.send(f"{member} does not have enough money in their Wallet")
    return
  earnings = random.randrange(0, bal[0])
  await update_bank(ctx.author, earnings)
  await update_bank(member, -1*earnings)
  await ctx.send(f"you have robbed {member} and gotten {earnings} Tenkoins from their Wallet")

async def leaderboard(ctx, bot: commands.Bot, x = 10):
  users = await functions.get_bankdata()
  leader_board = {}
  total = []
  for user in users:
    name = int(user)
    totalamount = users[user]["wallet"] + users[user]["bank"]
    leader_board[totalamount] = name
    total.append(totalamount)
  total = sorted(total, reverse=True)
  embed = discord.Embed(title=f"Top {x} richest users", color=0x465B73)
  index = 1
  for amt in total:
    id_ = leader_board[amt]
    member = bot.get_user(id_)
    name = member.name
    embed.add_field(name=f"{index}. {name}", value=f"{amt} Tenkoins", inline=False)
    if index == x:
      break
    else:
      index += 1
  await ctx.send(embed=embed)

import discord
from discord.ext import commands
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"users": {}}, f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": {}}

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Evil Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.red()
    )
    embed.add_field(name="!work", value="Earn random cash.", inline=False)
    embed.add_field(name="!lb", value="View the leaderboard.", inline=False)
    embed.add_field(name="!rob", value="Try robbing a bank.", inline=False)
    embed.add_field(name="!school", value="Spend cash to gain knowledge books.", inline=False)
    embed.add_field(name="!buy calculator", value="Purchase access to the calculator.", inline=False)
    embed.add_field(name="!calculator", value="Perform math operations (if purchased).", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def work(ctx):
    data = load_data()
    user_id = str(ctx.author.id)
    earned = random.randint(50, 200)
    if user_id not in data["users"]:
        data["users"][user_id] = {"cash": 0, "knowledge": 0, "calculator": False}
    data["users"][user_id]["cash"] += earned
    save_data(data)
    await ctx.send(f"{ctx.author.mention}, you worked hard and earned ${earned}!")

@bot.command()
async def lb(ctx):
    data = load_data()
    leaderboard = sorted(
        ((uid, stats["cash"]) for uid, stats in data["users"].items()), 
        key=lambda x: x[1], 
        reverse=True
    )
    embed = discord.Embed(
        title="Leaderboard",
        description="Top earners:",
        color=discord.Color.green()
    )
    for i, (uid, cash) in enumerate(leaderboard[:10], 1):
        user = await bot.fetch_user(int(uid))
        embed.add_field(name=f"{i}. {user}", value=f"${cash}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def rob(ctx):
    data = load_data()
    user_id = str(ctx.author.id)
    if user_id not in data["users"]:
        await ctx.send("You need to work first before attempting a robbery!")
        return
    success = random.choice([True, False])
    if success:
        loot = random.randint(200, 500)
        data["users"][user_id]["cash"] += loot
        save_data(data)
        await ctx.send(f"Success! You robbed the bank and got ${loot}!")
    else:
        fine = random.randint(100, 300)
        data["users"][user_id]["cash"] = max(0, data["users"][user_id]["cash"] - fine)
        save_data(data)
        await ctx.send(f"You got caught! You lost ${fine}. Better luck next time.")

@bot.command()
async def school(ctx):
    data = load_data()
    user_id = str(ctx.author.id)
    cost = 100
    if user_id not in data["users"] or data["users"][user_id]["cash"] < cost:
        await ctx.send("You don't have enough cash to attend school.")
        return
    data["users"][user_id]["cash"] -= cost
    data["users"][user_id]["knowledge"] += 1
    save_data(data)
    await ctx.send(f"{ctx.author.mention}, you attended school and gained 1 knowledge book!")

@bot.command()
async def buy(ctx, item):
    data = load_data()
    user_id = str(ctx.author.id)
    if item.lower() == "calculator":
        cost = 500
        if user_id not in data["users"] or data["users"][user_id]["cash"] < cost:
            await ctx.send("You don't have enough cash to buy the calculator.")
            return
        data["users"][user_id]["cash"] -= cost
        data["users"][user_id]["calculator"] = True
        save_data(data)
        await ctx.send("You have purchased the calculator!")

@bot.command()
async def calculator(ctx, *, expression):
    data = load_data()
    user_id = str(ctx.author.id)
    if user_id not in data["users"] or not data["users"][user_id].get("calculator", False):
        await ctx.send("You don't own calculator bro.")
        return
    try:
        result = eval(expression)
        await ctx.send(f"The result of `{expression}` is `{result}`.")
    except Exception as e:
        await ctx.send(f"Error in calculation! :warning:")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)

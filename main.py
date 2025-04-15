import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading
from utils import check_ban

# Initialisation de Flask
app = Flask(__name__)

# Load environment variables first
load_dotenv('.env', override=True)

# THEN access the environment variables
APPLICATION_ID = os.getenv("APPLICATION_ID")
TOKEN = os.getenv("TOKEN")
print("TOKEN loaded:", bool(TOKEN))  # Should print True

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

nomBot = "None"

# Route Flask pour afficher l'état du bot
@app.route('/')
def home():
    global nomBot
    if nomBot == "None":
        return "⏳ Bot is starting up, please wait..."
    return f"✅ Bot {nomBot} is working!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask).start()

@bot.event
async def on_ready():
    global nomBot
    nomBot = f"{bot.user}"
    print(f"Le bot est connecté en tant que {bot.user}")

@bot.command(name="ID")
async def check_ban_command(ctx):
    content = ctx.message.content
    user_id = content[3:].strip()
    print(f"Commande fait par {ctx.author}")

    # Vérification si l'ID est un nombre
    if not user_id.isdigit():
        await ctx.send(
            f"{ctx.author.mention} ❌ **UID invalide !**\n➡️ Veuillez fournir un UID valide sous la forme : `!ID 123456789`"
        )
        return

    try:
        ban_status = await check_ban(user_id)
    except Exception as e:
        await ctx.send(
            f"{ctx.author.mention} ⚠️ **ERROR WHILE CHEAKING:**\n```{str(e)}```"
        )
        return

    if ban_status is None:
        await ctx.send(
            f"{ctx.author.mention} ❌ **INFORMATION NOT AVAILABLE.**\nVeuillez réessayer plus tard."
        )
        return

    is_banned = int(ban_status.get("is_banned", 0))
    period = ban_status.get("period", "N/A")

    id = f"`{user_id} `"

    if isinstance(period, int):
        period_str = f"`MORE THAN {period} MONTH{'S' if period > 1 else ''}`"
    else:
        period_str = "`UNAVAILABLE`"

    embed = discord.Embed(color=0xFF0000 if is_banned else 0x00FF00,
                          timestamp=ctx.message.created_at)

    if is_banned:
        embed.title = "**▌ THIS ID IS BANNED  🛑 **\n"
        embed.description = (
            f"•**THIS ACCOUNT HAS BEEN CONFIRMED TO BE USING HACK.**\n."
            f"•**BANNED  : {period_str}**\n"
            f"•**PLAYER ID : `{id}`**\n")
        embed.set_image(url="https://i.ibb.co/tDnbYrK/standard-1.gif")
    else:
        embed.title = "**▌ THIS ID IS NOT BANNED ✅ **\n"
        embed.description = (
            f"•**THERE IS NOT ENOUGH EVIDENCE TO CONFIRM THE USE OF HACKING ON THIS ACCOUNT..**\n"
            f"•**PLAYER ID : `{id}`**\n")
        embed.set_image(url="https://i.ibb.co/CshJSf8/standard-2.gif")

    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    embed.set_footer(text="📌 Check ban free fire")
    await ctx.send(f"{ctx.author.mention}", embed=embed)

print("=== DEBUG ===")
print("TOKEN exists:", bool(TOKEN))
print("TOKEN type:", type(TOKEN))
print("=============")

bot.run(TOKEN)


import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading
from utils import check_ban

# Flask server for uptime
app = Flask(__name__)

# Load environment variables
load_dotenv('.env', override=True)

APPLICATION_ID = os.getenv("APPLICATION_ID")
TOKEN = os.getenv("TOKEN")

print("TOKEN loaded:", bool(TOKEN))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

nomBot = "None"
DEFAULT_LANG = "en"
user_languages = {}

# Flask route
@app.route('/')
def home():
    global nomBot
    if nomBot == "None":
        return "⏳ Bot is starting up, please wait..."
    return f" Bot {nomBot} is working!✅ "

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask).start()

@bot.event
async def on_ready():
    global nomBot
    nomBot = f"{bot.user}"
    print(f"Le bot est connecté en tant que {bot.user}")

@bot.command(name="lang")
async def change_language(ctx, lang_code: str):
    lang_code = lang_code.lower()
    if lang_code not in ["en", "fr"]:
        await ctx.send("❌ Invalid language. Available: `en`, `fr`")
        return

    user_languages[ctx.author.id] = lang_code
    message = "✅ Language set to English." if lang_code == 'en' else "✅ Langue définie sur le français."
    await ctx.send(f"{ctx.author.mention} {message}")

@bot.command(name="ID")
async def check_ban_command(ctx):
    content = ctx.message.content
    user_id = content[3:].strip()
    lang = user_languages.get(ctx.author.id, DEFAULT_LANG)

    print(f"Commande fait par {ctx.author} (lang={lang})")

    if not user_id.isdigit():
        message = {
            "en": f"{ctx.author.mention} ❌ **Invalid UID!**\n➡️ Please use: `!ID 123456789`",
            "fr": f"{ctx.author.mention} ❌ **UID invalide !**\n➡️ Veuillez fournir un UID valide sous la forme : `!ID 123456789`"
        }
        await ctx.send(message[lang])
        return

    try:
        ban_status = await check_ban(user_id)
    except Exception as e:
        await ctx.send(f"{ctx.author.mention} ⚠️ Error:\n```{str(e)}```")
        return

    if ban_status is None:
        message = {
            "en": f"{ctx.author.mention} ❌ **Could not get information. Please try again later.**",
            "fr": f"{ctx.author.mention} ❌ **Impossible d'obtenir les informations.**\nVeuillez réessayer plus tard."
        }
        await ctx.send(message[lang])
        return

    is_banned = int(ban_status.get("is_banned", 0))
    period = ban_status.get("period", "N/A")
    nickname = ban_status.get("nickname", "N/A")
    region = ban_status.get("region", "N/A")
    id_str = f"`{user_id}`"

    if isinstance(period, int):
        period_str = f"`MORE THAN {period} MONTH{'S' if period > 1 else ''}`" if lang == "en" else f"`PLUS DE {period} MOIS`"
    else:
        period_str = "`UNAVAILABLE`" if lang == "en" else "`INDISPONIBLE`"

    embed = discord.Embed(color=0xFF0000 if is_banned else 0x00FF00,
                          timestamp=ctx.message.created_at)

    if is_banned:
        embed.title = "**▌ BANNED ACCOUNT 🛑 **" if lang == "en" else "**▌ Compte banni 🛑 **"
        embed.description = (
            f"• {'This account was confirmed for using cheats.' if lang == 'en' else 'Ce compte a été confirmé comme utilisant des hacks.'}\n"
            f"• {'Nickname:' if lang == 'en' else 'Pseudo :'} `{nickname}`\n"
            f"• {'Player ID:' if lang == 'en' else 'ID du joueur :'} {id_str}\n"
            f"• {'Region:' if lang == 'en' else 'Région :'} `{region}`"
            f"• {'Suspension duration:' if lang == 'en' else 'Durée de la suspension :'} {period_str}\n"
        )
        embed.set_image(url="https://i.ibb.co/tDnbYrK/standard-1.gif")
    else:
        embed.title = "**▌ CLEAN ACCOUNT ✅ **" if lang == "en" else "**▌ Compte non banni ✅ **"
        embed.description = (
            f"• {'No sufficient evidence of cheat usage on this account.' if lang == 'en' else 'Aucune preuve suffisante pour confirmer l’utilisation de hacks sur ce compte.'}\n"
            f"• {'Nickname:' if lang == 'en' else 'Pseudo :'} `{nickname}`\n"
            f"• {'Player ID:' if lang == 'en' else 'ID du joueur :'} {id_str}\n"
            f"• {'Region:' if lang == 'en' else 'Région :'} `{region}`"
        )
        embed.set_image(url="https://i.ibb.co/CshJSf8/standard-2.gif")

    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    embed.set_footer(text="📌 Check ban free fire")
    await ctx.send(f"{ctx.author.mention}", embed=embed)

print("=== DEBUG ===")
print("TOKEN exists:", bool(TOKEN))
print("TOKEN type:", type(TOKEN))
print("=============")

bot.run(TOKEN)

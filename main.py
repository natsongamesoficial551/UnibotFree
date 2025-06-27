import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import aiohttp
from aiohttp import web

# Carrega variáveis do arquivo .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
MONGOURI = os.getenv("MONGOURI")
AUTOPING_URL = os.getenv("AUTOPING_URL")

# Conexão com o MongoDB
mongo_client = AsyncIOMotorClient(MONGOURI)
db = mongo_client["NatanDB"]

# Intents e inicialização do bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento ao conectar
@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")

    try:
        await db.command("ping")
        print("✅ Conectado com sucesso ao MongoDB!")
    except Exception as e:
        print(f"❌ Erro ao conectar no MongoDB: {e}")

    # Inicia a tarefa de autoping
    if AUTOPING_URL:
        autoping.start()
    else:
        print("⚠️ Variável AUTOPING_URL não configurada no .env")

# Tarefa para manter o Render ativo
@tasks.loop(minutes=5)
async def autoping():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(AUTOPING_URL) as response:
                print(f"📡 Autoping realizado: {response.status}")
    except Exception as e:
        print(f"⚠️ Erro no autoping: {e}")

# Servidor web para o Render "acordar"
async def handle(request):
    return web.Response(text="Bot está rodando.")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()
    print("🌐 Servidor web iniciado na porta 8080")

# Carrega os cogs
async def main():
    await start_webserver()

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog carregada: {filename}")
            except Exception as e:
                print(f"❌ Erro ao carregar cog {filename}: {e}")

    await bot.start(TOKEN)

# Executa o bot
asyncio.run(main())

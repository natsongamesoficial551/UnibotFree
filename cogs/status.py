import discord
from discord.ext import commands, tasks
import itertools

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statuses = itertools.cycle(["Use !ajuda", "Unibot gratuito!", "Prefixo: !"])
        self.change_status.start()
    
    @tasks.loop(seconds=30)
    async def change_status(self):
        # Aguarda o bot estar pronto antes de mudar o status
        await self.bot.wait_until_ready()
        texto = next(self.statuses)
        await self.bot.change_presence(activity=discord.Game(name=texto))
    
    @change_status.before_loop
    async def before_change_status(self):
        # Aguarda o bot estar conectado antes de iniciar o loop
        await self.bot.wait_until_ready()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} está pronto com status rotativo.")
    
    def cog_unload(self):
        # Para o loop quando o cog é descarregado
        self.change_status.cancel()

async def setup(bot):
    await bot.add_cog(Status(bot))
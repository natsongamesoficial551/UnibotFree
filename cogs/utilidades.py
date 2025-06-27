import discord
from discord.ext import commands
import platform
import datetime
import psutil

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! Latência: `{round(self.bot.latency * 1000)}ms`")
    
    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title="🤖 Informações do Bot", color=discord.Color.blue())
        embed.add_field(name="Nome", value=self.bot.user.name)
        embed.add_field(name="ID", value=self.bot.user.id)
        embed.add_field(name="Servidores", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="Usuários", value=f"{len(self.bot.users)}")
        embed.add_field(name="Versão", value="discord.py 2.5.2")
        embed.set_footer(text="Unibot gratuito")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def uptime(self, ctx):
        # Verifica se start_time existe, caso contrário usa o horário atual
        if hasattr(self.bot, 'start_time'):
            delta = datetime.datetime.utcnow() - self.bot.start_time
            await ctx.send(f"🕒 Uptime: `{str(delta).split('.')[0]}`")
        else:
            await ctx.send("⚠️ Tempo de atividade não disponível.")

async def setup(bot):
    await bot.add_cog(Utilidades(bot))
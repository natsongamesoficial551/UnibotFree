import discord
from discord.ext import commands
import random

class Sorteios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ativos = {}
        self.encerrados = {}  # Para armazenar sorteios encerrados
    
    @commands.command()
    async def comecarsorteio(self, ctx, *, premio: str):
        if ctx.channel.id in self.ativos:
            return await ctx.send("❌ Já há sorteio em andamento.")
        
        msg = await ctx.send(f"🎉 Sorteio iniciado! Prêmio: **{premio}**\nReaja com 🎉 para participar!")
        await msg.add_reaction("🎉")
        self.ativos[ctx.channel.id] = {
            'msg_id': msg.id,
            'premio': premio
        }
    
    @commands.command()
    async def encerrarsorteio(self, ctx):
        if ctx.channel.id not in self.ativos:
            return await ctx.send("❌ Nenhum sorteio em andamento.")
        
        sorteio_data = self.ativos[ctx.channel.id]
        msg = await ctx.channel.fetch_message(sorteio_data['msg_id'])
        
        # Move o sorteio para encerrados antes de remover dos ativos
        self.encerrados[ctx.channel.id] = sorteio_data
        del self.ativos[ctx.channel.id]
        
        await ctx.send("✅ Sorteio encerrado! Use `!vencedor` para selecionar o ganhador.")
    
    @commands.command()
    async def vencedor(self, ctx):
        # Verifica se há sorteio encerrado para sortear
        if ctx.channel.id not in self.encerrados:
            return await ctx.send("❌ Nenhum sorteio foi encerrado. Use `!encerrarsorteio` primeiro.")
        
        sorteio_data = self.encerrados[ctx.channel.id]
        msg = await ctx.channel.fetch_message(sorteio_data['msg_id'])
        
        # Busca a reação de participação
        reaction = discord.utils.get(msg.reactions, emoji="🎉")
        if not reaction:
            del self.encerrados[ctx.channel.id]
            return await ctx.send("❌ Ninguém participou do sorteio.")
        
        # Coleta todos os usuários que reagiram (exceto bots)
        users = []
        async for user in reaction.users():
            if not user.bot:
                users.append(user)
        
        if not users:
            del self.encerrados[ctx.channel.id]
            return await ctx.send("❌ Ninguém participou do sorteio.")
        
        # Seleciona o vencedor
        vencedor = random.choice(users)
        premio = sorteio_data['premio']
        
        await ctx.send(f"🎊 Parabéns {vencedor.mention}! Você venceu o sorteio do prêmio: **{premio}**!")
        
        # Remove o sorteio encerrado após sortear
        del self.encerrados[ctx.channel.id]
    
    @commands.command()
    async def cancelarsorteio(self, ctx):
        """Cancela um sorteio ativo"""
        if ctx.channel.id not in self.ativos:
            return await ctx.send("❌ Nenhum sorteio em andamento.")
        
        sorteio_data = self.ativos[ctx.channel.id]
        try:
            msg = await ctx.channel.fetch_message(sorteio_data['msg_id'])
            await msg.clear_reactions()
        except discord.NotFound:
            pass  # Mensagem foi deletada
        
        del self.ativos[ctx.channel.id]
        await ctx.send("❌ Sorteio cancelado.")

async def setup(bot):
    await bot.add_cog(Sorteios(bot))
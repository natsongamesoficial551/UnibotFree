import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGOURI'))
        self.db = self.client.bot_database
        self.collection = self.db.welcome_config

    async def carregar_config(self, guild_id):
        try:
            result = await self.collection.find_one({"guild_id": str(guild_id)})
            return result if result else {}
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
            return {}

    async def salvar_config(self, guild_id, config_type, canal_id):
        try:
            await self.collection.update_one(
                {"guild_id": str(guild_id)},
                {"$set": {config_type: canal_id}},
                upsert=True
            )
        except Exception as e:
            print(f"Erro ao salvar config: {e}")

    @commands.command(name='setentrada')
    @commands.has_permissions(administrator=True)
    async def set_entrada(self, ctx, canal: discord.TextChannel):
        """Define o canal de entrada."""
        try:
            await self.salvar_config(ctx.guild.id, 'entrada', canal.id)
            await ctx.send(f"✅ Canal de entrada definido para: {canal.mention}")
        except Exception as e:
            await ctx.send(f"❌ Erro ao definir canal de entrada: {e}")

    @commands.command(name='setsaida')
    @commands.has_permissions(administrator=True)
    async def set_saida(self, ctx, canal: discord.TextChannel):
        """Define o canal de saída."""
        try:
            await self.salvar_config(ctx.guild.id, 'saida', canal.id)
            await ctx.send(f"✅ Canal de saída definido para: {canal.mention}")
        except Exception as e:
            await ctx.send(f"❌ Erro ao definir canal de saída: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            data = await self.carregar_config(member.guild.id)
            canal = member.guild.get_channel(data.get('entrada')) if 'entrada' in data else None
            if canal:
                await canal.send(f"🎉 Olá {member.mention}, bem-vindo ao servidor! Não se esqueça de ler as regras e se divertir bastante!")
        except Exception as e:
            print(f"Erro no on_member_join: {e}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            data = await self.carregar_config(member.guild.id)
            canal = member.guild.get_channel(data.get('saida')) if 'saida' in data else None
            if canal:
                await canal.send(f"👋 O usuário {member.name} saiu do servidor. Até a próxima!")
        except Exception as e:
            print(f"Erro no on_member_remove: {e}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))

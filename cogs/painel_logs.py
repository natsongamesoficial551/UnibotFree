import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

class PainelLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGOURI'))  # CORRIGIDO
        self.db = self.client.bot_database
        self.collection = self.db.logs_config

    async def salvar_config(self, guild_id, canal_id):
        try:
            await self.collection.update_one(
                {"guild_id": str(guild_id)},
                {"$set": {"canal_id": canal_id}},
                upsert=True
            )
        except Exception as e:
            print(f"Erro ao salvar config de logs: {e}")

    async def carregar_config(self, guild_id):
        try:
            result = await self.collection.find_one({"guild_id": str(guild_id)})
            return result["canal_id"] if result else None
        except Exception as e:
            print(f"Erro ao carregar config de logs: {e}")
            return None

    @commands.command(name='setlogchannel')
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, canal: discord.TextChannel):
        """Define o canal de logs do servidor."""
        try:
            await self.salvar_config(ctx.guild.id, canal.id)
            await ctx.send(f"✅ Canal de logs definido para: {canal.mention}")
        except Exception as e:
            await ctx.send(f"❌ Erro ao definir canal de logs: {e}")

    async def get_log_channel(self, guild):
        try:
            canal_id = await self.carregar_config(guild.id)
            if canal_id:
                return guild.get_channel(canal_id)
            return None
        except Exception as e:
            print(f"Erro ao buscar canal de logs: {e}")
            return None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            canal = await self.get_log_channel(member.guild)
            if canal:
                embed = discord.Embed(
                    title="👥 Membro Entrou",
                    description=f"**{member.name}** entrou no servidor",
                    color=0x00ff00
                )
                embed.add_field(name="Usuário", value=member.mention, inline=True)
                embed.add_field(name="ID", value=member.id, inline=True)
                embed.set_thumbnail(url=member.display_avatar.url)
                await canal.send(embed=embed)
        except Exception as e:
            print(f"Erro no log de entrada: {e}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            canal = await self.get_log_channel(member.guild)
            if canal:
                embed = discord.Embed(
                    title="👥 Membro Saiu",
                    description=f"**{member.name}** saiu do servidor",
                    color=0xff0000
                )
                embed.add_field(name="Usuário", value=f"{member.name}#{member.discriminator}", inline=True)
                embed.add_field(name="ID", value=member.id, inline=True)
                embed.set_thumbnail(url=member.display_avatar.url)
                await canal.send(embed=embed)
        except Exception as e:
            print(f"Erro no log de saída: {e}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if message.author.bot or not message.guild:
                return
            canal = await self.get_log_channel(message.guild)
            if canal:
                embed = discord.Embed(
                    title="🗑️ Mensagem Deletada",
                    color=0xffa500
                )
                embed.add_field(name="Autor", value=message.author.mention, inline=True)
                embed.add_field(name="Canal", value=message.channel.mention, inline=True)
                embed.add_field(name="Conteúdo", value=message.content[:1000] or "Sem conteúdo", inline=False)
                embed.set_thumbnail(url=message.author.display_avatar.url)
                await canal.send(embed=embed)
        except Exception as e:
            print(f"Erro no log de mensagem deletada: {e}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            canal = await self.get_log_channel(guild)
            if canal:
                embed = discord.Embed(
                    title="🔨 Usuário Banido",
                    description=f"**{user.name}** foi banido do servidor",
                    color=0x8b0000
                )
                embed.add_field(name="Usuário", value=f"{user.name}#{user.discriminator}", inline=True)
                embed.add_field(name="ID", value=user.id, inline=True)
                embed.set_thumbnail(url=user.display_avatar.url)
                await canal.send(embed=embed)
        except Exception as e:
            print(f"Erro no log de ban: {e}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if before.nick != after.nick:
                canal = await self.get_log_channel(after.guild)
                if canal:
                    embed = discord.Embed(
                        title="✏️ Nickname Alterado",
                        color=0x0099ff
                    )
                    embed.add_field(name="Usuário", value=after.mention, inline=True)
                    embed.add_field(name="Antes", value=before.nick or "Sem nickname", inline=True)
                    embed.add_field(name="Depois", value=after.nick or "Sem nickname", inline=True)
                    embed.set_thumbnail(url=after.display_avatar.url)
                    await canal.send(embed=embed)
        except Exception as e:
            print(f"Erro no log de atualização de membro: {e}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if before.author.bot or not before.guild or before.content == after.content:
                return
            canal = await self.get_log_channel(before.guild)
            if canal:
                embed = discord.Embed(
                    title="✏️ Mensagem Editada",
                    color=0xffff00
                )
                embed.add_field(name="Autor", value=before.author.mention, inline=True)
                embed.add_field(name="Canal", value=before.channel.mention, inline=True)
                embed.add_field(name="Antes", value=before.content[:500] or "Sem conteúdo", inline=False)
                embed.add_field(name="Depois", value=after.content[:500] or "Sem conteúdo", inline=False)
                embed.set_thumbnail(url=before.author.display_avatar.url)
                await canal.send(embed=embed)
        except Exception as e:
            print(f"Erro no log de mensagem editada: {e}")

async def setup(bot):
    await bot.add_cog(PainelLogs(bot))

import discord
from discord.ext import commands

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banir(self, ctx, membro: discord.Member, *, motivo="Sem motivo"):
        await membro.ban(reason=motivo)
        await ctx.send(f"🔨 {membro} foi banido. Motivo: {motivo}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def expulsar(self, ctx, membro: discord.Member, *, motivo="Sem motivo"):
        await membro.kick(reason=motivo)
        await ctx.send(f"👢 {membro} foi expulso. Motivo: {motivo}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def limpar(self, ctx, quantidade: int = 10):
        await ctx.channel.purge(limit=quantidade + 1)
        await ctx.send(f"🧹 Limpei {quantidade} mensagens!", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mutar(self, ctx, membro: discord.Member, *, motivo="Sem motivo"):
        role = discord.utils.get(ctx.guild.roles, name="Mutado")
        if not role:
            role = await ctx.guild.create_role(name="Mutado", permissions=discord.Permissions(send_messages=False))
            for canal in ctx.guild.channels:
                await canal.set_permissions(role, send_messages=False)
        await membro.add_roles(role)
        await ctx.send(f"🔇 {membro.mention} foi mutado. Motivo: {motivo}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def desmutar(self, ctx, membro: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Mutado")
        if role in membro.roles:
            await membro.remove_roles(role)
            await ctx.send(f"🔊 {membro.mention} foi desmutado.")
        else:
            await ctx.send("Esse membro não está mutado.")

async def setup(bot):
    await bot.add_cog(Moderacao(bot))

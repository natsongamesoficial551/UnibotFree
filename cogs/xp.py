import discord
from discord.ext import commands
import json
import os
import random

CAMINHO = "data/xp.json"

def carregar():
    if not os.path.exists(CAMINHO):
        with open(CAMINHO, "w") as f:
            json.dump({}, f)
    with open(CAMINHO, "r") as f:
        return json.load(f)

def salvar(dados):
    with open(CAMINHO, "w") as f:
        json.dump(dados, f, indent=4)

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def xp_para_proximo(self, nivel):
        return 5 * (nivel ** 2) + 50 * nivel + 100

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        dados = carregar()
        uid = str(message.author.id)
        if uid not in dados:
            dados[uid] = {"xp": 0, "nivel": 1}
        dados[uid]["xp"] += random.randint(10, 20)
        xp_necessario = self.xp_para_proximo(dados[uid]["nivel"])
        if dados[uid]["xp"] >= xp_necessario:
            dados[uid]["xp"] -= xp_necessario
            dados[uid]["nivel"] += 1
            await message.channel.send(f"🎉 {message.author.mention} subiu para o nível {dados[uid]['nivel']}!")
        salvar(dados)

    @commands.command()
    async def xp(self, ctx, membro: discord.Member = None):
        membro = membro or ctx.author
        dados = carregar()
        uid = str(membro.id)
        if uid not in dados:
            return await ctx.send("Usuário sem XP registrado.")
        nivel = dados[uid]["nivel"]
        xp = dados[uid]["xp"]
        xp_max = self.xp_para_proximo(nivel)
        barra = int((xp / xp_max) * 20)
        progresso = f"[{'█'*barra}{'-'*(20-barra)}] ({xp}/{xp_max})"
        await ctx.send(f"📊 {membro.mention} - Nível: {nivel}\n{progresso}")

    @commands.command()
    async def topxp(self, ctx):
        dados = carregar()
        ranking = sorted(dados.items(), key=lambda x: (x[1]["nivel"], x[1]["xp"]), reverse=True)
        texto = "**🏆 Ranking de XP**\n"
        for i, (uid, info) in enumerate(ranking[:10]):
            membro = await self.bot.fetch_user(int(uid))
            texto += f"{i+1}. {membro.name} - Nível {info['nivel']} ({info['xp']} XP)\n"
        await ctx.send(texto)

async def setup(bot):
    await bot.add_cog(XP(bot))

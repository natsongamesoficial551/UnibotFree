import discord
from discord.ext import commands
import os
from motor.motor_asyncio import AsyncIOMotorClient
import random

# Configurações do MongoDB
MONGO_URI = os.getenv("MONGOURI")
DATABASE_NAME = "discord_bot"
COLLECTION_NAME = "economia"

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    async def get_user(self, user_id):
        user_data = await self.collection.find_one({"user_id": str(user_id)})
        if not user_data:
            new_user = {"user_id": str(user_id), "saldo": 0, "trabalhos": 0}
            await self.collection.insert_one(new_user)
            return new_user
        return user_data

    async def update_user(self, user_id, update_data):
        await self.collection.update_one(
            {"user_id": str(user_id)},
            {"$set": update_data}
        )

    @commands.command()
    async def saldo(self, ctx):
        user_data = await self.get_user(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, você tem {user_data['saldo']} moedas.")

    @commands.command()
    async def diario(self, ctx):
        user_data = await self.get_user(ctx.author.id)
        recompensa = random.randint(100, 300)
        await self.update_user(ctx.author.id, {"saldo": user_data["saldo"] + recompensa})
        await ctx.send(f"💰 {ctx.author.mention}, você coletou seu diário e recebeu {recompensa} moedas!")

    @commands.command()
    async def trabalhar(self, ctx):
        user_data = await self.get_user(ctx.author.id)
        ganhos = random.randint(50, 200)
        await self.update_user(ctx.author.id, {
            "saldo": user_data["saldo"] + ganhos,
            "trabalhos": user_data["trabalhos"] + 1
        })
        await ctx.send(f"👷 {ctx.author.mention}, você trabalhou e ganhou {ganhos} moedas.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def darcoins(self, ctx, membro: discord.Member, quantia: int):
        user_data = await self.get_user(membro.id)
        await self.update_user(membro.id, {"saldo": user_data["saldo"] + quantia})
        await ctx.send(f"{ctx.author.mention} deu {quantia} moedas para {membro.mention}!")

    @commands.command()
    async def transferir(self, ctx, membro: discord.Member, quantia: int):
        if membro.id == ctx.author.id:
            return await ctx.send("Você não pode transferir para si mesmo!")
        if quantia <= 0:
            return await ctx.send("A quantia deve ser maior que zero!")

        sender_data = await self.get_user(ctx.author.id)
        if sender_data["saldo"] < quantia:
            return await ctx.send("Você não tem saldo suficiente!")

        receiver_data = await self.get_user(membro.id)
        await self.update_user(ctx.author.id, {"saldo": sender_data["saldo"] - quantia})
        await self.update_user(membro.id, {"saldo": receiver_data["saldo"] + quantia})
        await ctx.send(f"💸 {ctx.author.mention} transferiu {quantia} moedas para {membro.mention}.")

    @commands.command()
    async def rankmoney(self, ctx):
        cursor = self.collection.find().sort("saldo", -1).limit(10)
        users = await cursor.to_list(length=10)

        if not users:
            return await ctx.send("Ainda não há dados de economia!")

        msg = "🏆 **Ranking de Riqueza**:\n"
        for i, user_data in enumerate(users):
            try:
                membro = await self.bot.fetch_user(int(user_data["user_id"]))
                msg += f"{i+1}. {membro.name} - {user_data['saldo']} moedas\n"
            except:
                msg += f"{i+1}. Usuário #{user_data['user_id']} - {user_data['saldo']} moedas\n"

        await ctx.send(msg)

    def cog_unload(self):
        self.client.close()

async def setup(bot):
    await bot.add_cog(Economia(bot))

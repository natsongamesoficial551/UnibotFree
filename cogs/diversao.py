import discord
from discord.ext import commands
import random
import asyncio
import json
from datetime import datetime

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['!', '/'], intents=intents)

# Dicionários para respostas bilíngues
RESPONSES = {
    'dice': {
        'pt': 'rodou um dado e tirou',
        'en': 'rolled a dice and got'
    },
    'coinflip': {
        'pt': ['Cara! 🪙', 'Coroa! 🪙'],
        'en': ['Heads! 🪙', 'Tails! 🪙']
    },
    'joke': {
        'pt': [
            "Por que os pássaros voam para o sul no inverno? Porque é muito longe para ir andando! 😂",
            "O que a impressora falou para a outra impressora? Essa folha é sua ou é impressão minha? 🖨️",
            "Por que o livro de matemática estava triste? Porque tinha muitos problemas! 📚"
        ],
        'en': [
            "Why don't scientists trust atoms? Because they make up everything! ⚛️",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾"
        ]
    },
    'compliment': {
        'pt': [
            "Você é incrível! ✨", "Seu sorriso ilumina o dia! 😊", 
            "Você tem uma energia maravilhosa! 🌟", "Você é muito especial! 💖"
        ],
        'en': [
            "You're amazing! ✨", "Your smile brightens the day! 😊",
            "You have wonderful energy! 🌟", "You're very special! 💖"
        ]
    },
    'magic8ball': {
        'pt': [
            "Sim, definitivamente! 🔮", "Não conte com isso 🔮", "Talvez... 🔮",
            "Sim! 🔮", "Não 🔮", "Concentre-se e pergunte novamente 🔮"
        ],
        'en': [
            "Yes, definitely! 🔮", "Don't count on it 🔮", "Maybe... 🔮",
            "Yes! 🔮", "No 🔮", "Focus and ask again 🔮"
        ]
    }
}

def detect_language(text):
    """Detecta o idioma baseado em palavras-chave"""
    pt_words = ['olá', 'oi', 'obrigado', 'por favor', 'sim', 'não', 'como', 'que']
    en_words = ['hello', 'hi', 'thanks', 'please', 'yes', 'no', 'how', 'what']
    
    text_lower = text.lower()
    pt_count = sum(1 for word in pt_words if word in text_lower)
    en_count = sum(1 for word in en_words if word_lower in text_lower)
    
    return 'pt' if pt_count > en_count else 'en'

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} está online!')
    print(f'🌐 Bot conectado em {len(bot.guilds)} servidor(s)')
    await bot.change_presence(activity=discord.Game(name="!help | /ajuda"))

@bot.command(name='dado', aliases=['dice'])
async def roll_dice(ctx, sides: int = 6):
    """🎲 Rola um dado / Roll a dice"""
    if sides < 2 or sides > 100:
        await ctx.send("❌ Número de lados deve ser entre 2-100 / Sides must be 2-100")
        return
    
    lang = detect_language(ctx.message.content)
    result = random.randint(1, sides)
    
    embed = discord.Embed(
        title="🎲 Dado / Dice",
        description=f"{ctx.author.mention} {RESPONSES['dice'][lang]} **{result}**!",
        color=0x00ff00
    )
    embed.add_field(name="Lados / Sides", value=f"{sides}", inline=True)
    await ctx.send(embed=embed)

@bot.command(name='moeda', aliases=['coinflip', 'flip'])
async def coin_flip(ctx):
    """🪙 Cara ou coroa / Heads or tails"""
    lang = detect_language(ctx.message.content)
    result = random.choice(RESPONSES['coinflip'][lang])
    
    embed = discord.Embed(
        title="🪙 Cara ou Coroa / Coin Flip",
        description=f"{ctx.author.mention}, {result}",
        color=0xffd700
    )
    await ctx.send(embed=embed)

@bot.command(name='piada', aliases=['joke'])
async def tell_joke(ctx):
    """😂 Conta uma piada / Tell a joke"""
    lang = detect_language(ctx.message.content)
    joke = random.choice(RESPONSES['joke'][lang])
    
    embed = discord.Embed(
        title="😂 Piada / Joke",
        description=joke,
        color=0xff69b4
    )
    await ctx.send(embed=embed)

@bot.command(name='elogio', aliases=['compliment'])
async def give_compliment(ctx, member: discord.Member = None):
    """💖 Faz um elogio / Give a compliment"""
    target = member or ctx.author
    lang = detect_language(ctx.message.content)
    compliment = random.choice(RESPONSES['compliment'][lang])
    
    embed = discord.Embed(
        title="💖 Elogio / Compliment",
        description=f"{target.mention}, {compliment}",
        color=0xff1493
    )
    await ctx.send(embed=embed)

@bot.command(name='bola8', aliases=['8ball', 'magic8'])
async def magic_8ball(ctx, *, question):
    """🔮 Bola mágica 8 / Magic 8 ball"""
    if len(question) < 3:
        await ctx.send("❌ Faça uma pergunta! / Ask a question!")
        return
    
    lang = detect_language(question)
    answer = random.choice(RESPONSES['magic8ball'][lang])
    
    embed = discord.Embed(
        title="🔮 Bola Mágica 8 / Magic 8 Ball",
        color=0x800080
    )
    embed.add_field(name="Pergunta / Question", value=question, inline=False)
    embed.add_field(name="Resposta / Answer", value=answer, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='ajuda', aliases=['help'])
async def help_command(ctx):
    """📋 Mostra todos os comandos / Show all commands"""
    embed = discord.Embed(
        title="🤖 Comandos do Bot / Bot Commands",
        description="Lista de comandos disponíveis / Available commands list",
        color=0x0099ff
    )
    
    commands_list = [
        "🎲 `!dado [lados]` / `!dice [sides]` - Rola um dado",
        "🪙 `!moeda` / `!coinflip` - Cara ou coroa",
        "😂 `!piada` / `!joke` - Conta uma piada",
        "💖 `!elogio [@user]` / `!compliment [@user]` - Faz elogio",
        "🔮 `!bola8 <pergunta>` / `!8ball <question>` - Bola mágica"
    ]
    
    embed.add_field(
        name="Comandos / Commands", 
        value="\n".join(commands_list), 
        inline=False
    )
    embed.set_footer(text="Feito com ❤️ / Made with ❤️")
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Comando incompleto! Use `!ajuda` / Incomplete command! Use `!help`")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando não encontrado! / Command not found!")
    else:
        print(f"Erro: {error}")

# Para iniciar o bot, descomente a linha abaixo e adicione seu token
# bot.run('SEU_TOKEN_AQUI')

"""
🔧 SETUP INSTRUCTIONS / INSTRUÇÕES DE CONFIGURAÇÃO:

1. Instale a biblioteca:
   pip install discord.py

2. Crie um bot no Discord Developer Portal:
   https://discord.com/developers/applications

3. Copie o token e substitua 'SEU_TOKEN_AQUI'

4. Convide o bot para seu servidor com permissões:
   - Send Messages
   - Use Slash Commands
   - Embed Links
   - Read Message History

5. Execute o arquivo Python!

📝 COMANDOS DISPONÍVEIS / AVAILABLE COMMANDS:
- !dado / !dice - Rola dado
- !moeda / !coinflip - Cara ou coroa  
- !piada / !joke - Conta piada
- !elogio / !compliment - Faz elogio
- !bola8 / !8ball - Bola mágica 8
- !ajuda / !help - Mostra ajuda
"""
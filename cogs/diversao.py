import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
import motor.motor_asyncio
import os
from dotenv import load_dotenv
import re

load_dotenv()

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_URI'))
        self.db = self.client.bot_database
        self.fun_collection = self.db.fun_data
        
        # Language detection patterns
        self.pt_patterns = [
            r'\b(verdade|desafio|pergunta|resposta|piada|abraço|beijar|tapa|amor|ódio|gay|ship|8ball|bola|pergunto)\b',
            r'\b(sim|não|talvez|claro|obvio|jamais|nunca|sempre|quem|como|onde|quando|porque)\b'
        ]
        
        # Multilingual responses
        self.responses = {
            'pt': {
                '8ball': [
                    "Sim, definitivamente!", "É certo!", "Sem dúvida!", "Sim, com certeza!",
                    "Você pode contar com isso!", "Como eu vejo, sim!", "Muito provável!",
                    "Parece bom!", "Sim!", "Os sinais apontam para sim!",
                    "Resposta nebulosa, tente novamente!", "Pergunte novamente mais tarde!",
                    "Melhor não te contar agora!", "Não posso prever agora!",
                    "Concentre-se e pergunte novamente!", "Não conte com isso!",
                    "Minha resposta é não!", "Minhas fontes dizem não!",
                    "Perspectivas não muito boas!", "Muito duvidoso!"
                ],
                'truth_questions': [
                    "Qual foi a coisa mais embaraçosa que você já fez?",
                    "Quem foi seu primeiro crush?",
                    "Qual é seu maior medo?",
                    "Qual foi a maior mentira que você já contou?",
                    "O que você faria se fosse invisível por um dia?",
                    "Qual é o seu segredo mais profundo?",
                    "Você já teve uma paixão por alguém deste servidor?",
                    "Qual foi o momento mais constrangedor da sua vida?",
                    "Se você pudesse mudar algo em você, o que seria?",
                    "Qual é a coisa mais infantil que você ainda faz?"
                ],
                'dare_challenges': [
                    "Mude seu nick para algo engraçado por 1 hora!",
                    "Cante uma música no chat de voz!",
                    "Conte uma piada ruim no chat!",
                    "Poste um meme nos próximos 3 canais!",
                    "Fale apenas em CAPS LOCK pelos próximos 10 minutos!",
                    "Desenhe algo terrível e poste aqui!",
                    "Imite um animal pelos próximos 5 minutos!",
                    "Conte uma história inventada sobre aliens!",
                    "Faça 20 flexões e comprove com foto!",
                    "Grave um áudio cantando parabéns!"
                ],
                'jokes': [
                    "Por que o livro de matemática estava triste? Porque tinha muitos problemas!",
                    "O que o pato disse para a pata? Vem quá!",
                    "Por que os pássaros voam para o sul no inverno? Porque é muito longe para ir andando!",
                    "O que acontece quando você cruza um peixe com um elefante? Você obtém nadar trunks!",
                    "Por que o espantalho ganhou um prêmio? Porque era excepcional em sua área!",
                    "O que você chama de um urso sem orelhas? B!",
                    "Por que não confiamos nas escadas? Porque elas estão sempre tramando algo!",
                    "O que o oceano disse para a praia? Nada, apenas acenou!",
                    "Por que o café foi para a polícia? Foi moído!",
                    "O que você chama de um dinossauro que bate carros? Tyrannosaurus Wrecks!"
                ]
            },
            'en': {
                '8ball': [
                    "Yes, definitely!", "It is certain!", "Without a doubt!", "Yes, for sure!",
                    "You may rely on it!", "As I see it, yes!", "Most likely!",
                    "Outlook good!", "Yes!", "Signs point to yes!",
                    "Reply hazy, try again!", "Ask again later!",
                    "Better not tell you now!", "Cannot predict now!",
                    "Concentrate and ask again!", "Don't count on it!",
                    "My reply is no!", "My sources say no!",
                    "Outlook not so good!", "Very doubtful!"
                ],
                'truth_questions': [
                    "What's the most embarrassing thing you've ever done?",
                    "Who was your first crush?",
                    "What's your biggest fear?",
                    "What's the biggest lie you've ever told?",
                    "What would you do if you were invisible for a day?",
                    "What's your deepest secret?",
                    "Have you ever had a crush on someone from this server?",
                    "What was the most embarrassing moment of your life?",
                    "If you could change something about yourself, what would it be?",
                    "What's the most childish thing you still do?"
                ],
                'dare_challenges': [
                    "Change your nickname to something funny for 1 hour!",
                    "Sing a song in voice chat!",
                    "Tell a bad joke in chat!",
                    "Post a meme in the next 3 channels!",
                    "Speak only in CAPS LOCK for the next 10 minutes!",
                    "Draw something terrible and post it here!",
                    "Imitate an animal for the next 5 minutes!",
                    "Tell a made-up story about aliens!",
                    "Do 20 push-ups and prove it with a photo!",
                    "Record an audio singing happy birthday!"
                ],
                'jokes': [
                    "Why was the math book sad? It had too many problems!",
                    "What do you call a duck that gets all A's? A wise quacker!",
                    "Why do birds fly south for the winter? Because it's too far to walk!",
                    "What happens when you cross a fish with an elephant? You get swimming trunks!",
                    "Why did the scarecrow win an award? Because he was outstanding in his field!",
                    "What do you call a bear with no ears? B!",
                    "Why don't we trust stairs? Because they're always up to something!",
                    "What did the ocean say to the beach? Nothing, it just waved!",
                    "Why did the coffee go to the police? It got mugged!",
                    "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!"
                ]
            }
        }

    def detect_language(self, text):
        """Detect language based on text patterns"""
        text_lower = text.lower()
        
        # Check for Portuguese patterns
        for pattern in self.pt_patterns:
            if re.search(pattern, text_lower):
                return 'pt'
        
        # Default to English if no Portuguese patterns found
        return 'en'

    async def save_interaction(self, user_id, command, data=None):
        """Save user interaction to database"""
        try:
            await self.fun_collection.insert_one({
                'user_id': user_id,
                'command': command,
                'data': data,
                'timestamp': datetime.utcnow()
            })
        except Exception as e:
            print(f"Database error: {e}")

    @commands.command(name='verdade', aliases=['truth'])
    async def truth_command(self, ctx):
        """Truth or Dare - Truth questions / Verdade ou Desafio - Perguntas"""
        try:
            lang = self.detect_language(ctx.message.content)
            
            question = random.choice(self.responses[lang]['truth_questions'])
            
            embed = discord.Embed(
                title="🤔 Verdade / Truth" if lang == 'pt' else "🤔 Truth",
                description=question,
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"Perguntado por / Asked by {ctx.author.display_name}", 
                            icon_url=ctx.author.display_avatar.url)
            
            await ctx.send(embed=embed)
            await self.save_interaction(ctx.author.id, 'truth', {'question': question, 'language': lang})
        except Exception as e:
            await ctx.send("❌ Erro ao executar comando!")
            print(f"Erro no comando verdade: {e}")

    @commands.command(name='desafio', aliases=['dare'])
    async def dare_command(self, ctx):
        """Truth or Dare - Dare challenges / Verdade ou Desafio - Desafios"""
        try:
            lang = self.detect_language(ctx.message.content)
            
            challenge = random.choice(self.responses[lang]['dare_challenges'])
            
            embed = discord.Embed(
                title="😈 Desafio / Dare" if lang == 'pt' else "😈 Dare",
                description=challenge,
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"Desafiado por / Dared by {ctx.author.display_name}", 
                            icon_url=ctx.author.display_avatar.url)
            
            await ctx.send(embed=embed)
            await self.save_interaction(ctx.author.id, 'dare', {'challenge': challenge, 'language': lang})
        except Exception as e:
            await ctx.send("❌ Erro ao executar comando!")
            print(f"Erro no comando desafio: {e}")

    @commands.command(name='8ball', aliases=['bola8', 'pergunta', 'ask'])
    async def eight_ball(self, ctx, *, question=None):
        """Magic 8-Ball / Bola Mágica 8"""
        try:
            lang = self.detect_language(ctx.message.content + (question or ''))
            
            if not question:
                error_msg = "Você precisa fazer uma pergunta!" if lang == 'pt' else "You need to ask a question!"
                await ctx.send(error_msg)
                return
            
            answer = random.choice(self.responses[lang]['8ball'])
            
            embed = discord.Embed(
                title="🎱 Bola Mágica 8 / Magic 8-Ball" if lang == 'pt' else "🎱 Magic 8-Ball",
                color=discord.Color.purple(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Pergunta / Question" if lang == 'pt' else "Question", 
                           value=question, inline=False)
            embed.add_field(name="Resposta / Answer" if lang == 'pt' else "Answer", 
                           value=f"🔮 {answer}", inline=False)
            embed.set_footer(text=f"Perguntado por / Asked by {ctx.author.display_name}", 
                            icon_url=ctx.author.display_avatar.url)
            
            await ctx.send(embed=embed)
            await self.save_interaction(ctx.author.id, '8ball', 
                                      {'question': question, 'answer': answer, 'language': lang})
        except Exception as e:
            await ctx.send("❌ Erro ao executar comando!")
            print(f"Erro no comando 8ball: {e}")

    @commands.command(name='piada', aliases=['joke'])
    async def joke_command(self, ctx):
        """Random jokes / Piadas aleatórias"""
        try:
            lang = self.detect_language(ctx.message.content)
            
            joke = random.choice(self.responses[lang]['jokes'])
            
            embed = discord.Embed(
                title="😂 Piada / Joke" if lang == 'pt' else "😂 Joke",
                description=joke,
                color=discord.Color.gold(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"Solicitado por / Requested by {ctx.author.display_name}", 
                            icon_url=ctx.author.display_avatar.url)
            
            await ctx.send(embed=embed)
            await self.save_interaction(ctx.author.id, 'joke', {'joke': joke, 'language': lang})
        except Exception as e:
            await ctx.send("❌ Erro ao executar comando!")
            print(f"Erro no comando piada: {e}")

    @commands.command(name='ship', aliases=['amor', 'love'])
    async def ship_command(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        """Ship two users / Shippar dois usuários"""
        try:
            lang = self.detect_language(ctx.message.content)
            
            if not user1:
                user1 = ctx.author
            if not user2:
                error_msg = "Mencione alguém para shippar!" if lang == 'pt' else "Mention someone to ship!"
                await ctx.send(error_msg)
                return
            
            # Verificar se é a mesma pessoa
            if user1.id == user2.id:
                selfship_msg = "💕 Amor próprio é importante!" if lang == 'pt' else "💕 Self-love is important!"
                await ctx.send(selfship_msg)
                return
            
            # Calculate ship percentage based on user IDs (consistent results)
            combined_id = str(user1.id) + str(user2.id)
            percentage = abs(hash(combined_id) % 101)
            
            # Ship name
            ship_name = user1.display_name[:len(user1.display_name)//2] + user2.display_name[len(user2.display_name)//2:]
            
            # Reaction based on percentage
            if percentage >= 90:
                reaction = "💕 Amor verdadeiro!" if lang == 'pt' else "💕 True love!"
                color = discord.Color.pink()
            elif percentage >= 70:
                reaction = "💖 Muito compatíveis!" if lang == 'pt' else "💖 Very compatible!"
                color = discord.Color.red()
            elif percentage >= 50:
                reaction = "💙 Podem dar certo!" if lang == 'pt' else "💙 Could work out!"
                color = discord.Color.blue()
            elif percentage >= 30:
                reaction = "💛 Apenas amigos!" if lang == 'pt' else "💛 Just friends!"
                color = discord.Color.gold()
            else:
                reaction = "💔 Não combina..." if lang == 'pt' else "💔 Not compatible..."
                color = discord.Color.darker_grey()
            
            embed = discord.Embed(
                title=f"💕 Ship: {ship_name}",
                color=color,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👫 Casal / Couple" if lang == 'pt' else "👫 Couple", 
                           value=f"{user1.mention} ❤️ {user2.mention}", inline=False)
            embed.add_field(name="📊 Compatibilidade / Compatibility" if lang == 'pt' else "📊 Compatibility", 
                           value=f"{percentage}%", inline=True)
            embed.add_field(name="💭 Resultado / Result" if lang == 'pt' else "💭 Result", 
                           value=reaction, inline=True)
            
            # Progress bar
            filled = int(percentage / 10)
            bar = "█" * filled + "░" * (10 - filled)
            embed.add_field(name="📈 Medidor / Meter" if lang == 'pt' else "📈 Meter", 
                           value=f"`{bar}` {percentage}%", inline=False)
            
            embed.set_footer(text=f"Shippado por / Shipped by {ctx.author.display_name}", 
                            icon_url=ctx.author.display_avatar.url)
            
            await ctx.send(embed=embed)
            await self.save_interaction(ctx.author.id, 'ship', 
                                      {'user1': user1.id, 'user2': user2.id, 'percentage': percentage, 'language': lang})
        except Exception as e:
            await ctx.send("❌ Erro ao executar comando!")
            print(f"Erro no comando ship: {e}")

    @commands.command(name='gay', aliases=['gayrate'])
    async def gay_rate(self, ctx, user: discord.Member = None):
        """Gay rate meter / Medidor gay"""
        try:
            lang = self.detect_language(ctx.message.content)
            
            if not user:
                user = ctx.author
            
            # Calculate percentage based on user ID (consistent results)
            percentage = abs(hash(str(user.id)) % 101)
            
            # Reactions based on percentage
            if percentage >= 90:
                reaction = "🏳️‍🌈 Super gay!" if lang == 'en' else "🏳️‍🌈 Super gay!"
            elif percentage >= 70:
                reaction = "🌈 Muito gay!" if lang == 'pt' else "🌈 Very gay!"
            elif percentage >= 50:
                reaction = "💖 Meio gay!" if lang == 'pt' else "💖 Kinda gay!"
            elif percentage >= 30:
                reaction = "💙 Um pouco gay!" if lang == 'pt' else "💙 A little gay!"
            else:
                reaction = "💔 Não gay!" if lang == 'pt' else "💔 Not gay!"
            
            embed = discord.Embed(
                title="🏳️‍🌈 Medidor Gay / Gay Meter" if lang == 'pt' else "🏳️‍🌈 Gay Meter",
                color=discord.Color.from_rgb(255, 105, 180),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="👤 Usuário / User" if lang == 'pt' else "👤 User", 
                           value=user.mention, inline=True)
            embed.add_field(name="📊 Taxa Gay / Gay Rate" if lang == 'pt' else "📊 Gay Rate", 
                           value=f"{percentage}%", inline=True)
            embed.add_field(name="💭 Resultado / Result" if lang == 'pt' else "💭 Result", 
                           value=reaction, inline=False)
            
            # Progress bar
            filled = int(percentage / 10)
            bar = "🌈" * filled + "⬜" * (10 - filled)
            embed.add_field(name="📈 Medidor / Meter" if lang == 'pt' else "📈 Meter", 
                           value=f"`{bar}` {percentage}%", inline=False)
            
            embed.set_footer(text=f"Testado por / Tested by {ctx.author.display_name}", 
                            icon_url=ctx.author.display_avatar.url)
            
            await ctx.send(embed=embed)
            await self.save_interaction(ctx.author.id, 'gay', 
                                      {'user': user.id, 'percentage': percentage, 'language': lang})
        except Exception as e:
            await ctx.send("❌ Erro ao executar comando!")
            print(f"Erro no comando gay: {e}")

    @commands.command(name='roleta', aliases=['roulette', 'escolher', 'choose'])
    async def roulette_command(self, ctx, *, options=None):
        """Choose randomly from options / Escolher aleatoriamente entre opções"""
        try:
            lang = self.detect_language(ctx.message.content + (options or ''))
            
            if not options:
                error_msg = "Digite as opções separadas por vírgula! Ex: `!roleta pizza, hambúrguer, sushi`" if lang == 'pt' else "Enter options separated by commas! Ex: `!roulette pizza, burger, sushi`"
                await ctx.send(error_msg)
                return
            
            choices = [choice.strip() for choice in options.split(',')]
            if len(choices) < 2:
                error_msg = "Você precisa de pelo menos 2 opções!" if lang == 'pt' else "You need at least 2 options!"
                await ctx.send(error_msg)
                return
            
            chosen = random.choice(choices)
            
            embed = discord.Embed(
                title="🎰 Roleta da Sorte / Lucky Roulette" if lang == 'pt' else "🎰 Lucky Roulette",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="🎯 Opções / Options" if lang == 'pt' else "🎯 Options", 
                           value=", ".join(f"`{choice}`" for choice in choices), inline=False)
            embed.add_field(name="🏆 Escolhido / Chosen" if lang == 'pt' else "🏆 Chosen", 
                           value=f"**{chosen}**", inline=False)
            
            embed.set_footer(text=f"Solicitado por / Requested by {ctx.author.display_name}", 
                            icon_url=ctx.author.display_avatar.url)
            
            # Add spinning animation
            message = await ctx.send("🎰 Girando a roleta..." if lang == 'pt' else "🎰 Spinning the roulette...")
            await asyncio.sleep(2)
            await message.edit(content="", embed=embed)
            
            await self.save_interaction(ctx.author.id, 'roulette', 
                                      {'options': choices, 'chosen': chosen, 'language': lang})
        except Exception as e:
            await ctx.send("❌ Erro ao executar comando!")
            print(f"Erro no comando roleta: {e}")

    @commands.command(name='estatisticas', aliases=['stats', 'funstats'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fun_stats(self, ctx, user: discord.Member = None):
        """Show fun command statistics / Mostrar estatísticas dos comandos de diversão"""
        try:
            lang = self.detect_language(ctx.message.content)
            
            if not user:
                user = ctx.author
            
            # Get user statistics from database
            stats = await self.fun_collection.find({'user_id': user.id}).to_list(length=None)
            
            if not stats:
                no_data_msg = f"Nenhuma estatística encontrada para {user.display_name}!" if lang == 'pt' else f"No statistics found for {user.display_name}!"
                await ctx.send(no_data_msg)
                return
            
            # Count commands
            command_counts = {}
            for stat in stats:
                cmd = stat.get('command', 'unknown')
                command_counts[cmd] = command_counts.get(cmd, 0) + 1
            
            total_commands = sum(command_counts.values())
            
            embed = discord.Embed(
                title=f"📊 Estatísticas de Diversão / Fun Statistics - {user.display_name}",
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="📈 Total de Comandos / Total Commands" if lang == 'pt' else "📈 Total Commands", 
                           value=str(total_commands), inline=True)
            
            # Most used command
            if command_counts:
                most_used = max(command_counts, key=command_counts.get)
                embed.add_field(name="🏆 Comando Favorito / Favorite Command" if lang == 'pt' else "🏆 Favorite Command", 
                               value=f"{most_used} ({command_counts[most_used]}x)", inline=True)
            
            # Command breakdown
            commands_text = ""
            for cmd, count in sorted(command_counts.items(), key=lambda x: x[1], reverse=True):
                commands_text += f"• **{cmd}**: {count}x\n"
            
            if commands_text:
                embed.add_field(name="🎮 Detalhes / Details" if lang == 'pt' else "🎮 Details", 
                               value=commands_text, inline=False)
            
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.set_footer(text=f"Solicitado por / Requested by {ctx.author.display_name}", 
                            icon_url=ctx.author.display_avatar.url)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            error_msg = "Erro ao buscar estatísticas!" if lang == 'pt' else "Error fetching statistics!"
            await ctx.send(error_msg)
            print(f"Stats error: {e}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandOnCooldown):
            lang = self.detect_language(ctx.message.content)
            remaining = round(error.retry_after)
            
            cooldown_msg = f"⏰ Aguarde {remaining} segundos antes de usar este comando novamente!" if lang == 'pt' else f"⏰ Wait {remaining} seconds before using this command again!"
            await ctx.send(cooldown_msg, delete_after=10)

async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(FunCog(bot))
    print("✅ Fun Cog loaded successfully!")
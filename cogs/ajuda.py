import discord
from discord.ext import commands

class HelpSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='cmds', aliases=['comandos'])
    async def cmds(self, ctx):
        """Menu principal de ajuda com todas as categorias"""
        embed = discord.Embed(
            title="🤖 Central de Ajuda - Unibot",
            description="Escolha uma categoria para ver os comandos disponíveis:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Sistema de Logs",
            value="`!ajuda logs` - Sistema de monitoramento do servidor",
            inline=False
        )
        
        embed.add_field(
            name="🎭 Sistema de Roleplay", 
            value="`!ajuda roleplay` - Comandos de interação entre usuários",
            inline=False
        )
        
        embed.add_field(
            name="💰 Sistema de Economia",
            value="`!ajuda economia` - Moedas, trabalho e transferências",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Sistema de Moderação",
            value="`!ajuda moderacao` - Comandos para moderadores",
            inline=False
        )
        
        embed.add_field(
            name="🎉 Sistema de Sorteios",
            value="`!ajuda sorteios` - Criar e gerenciar sorteios",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Utilidades",
            value="`!ajuda utils` - Informações e ferramentas úteis",
            inline=False
        )
        
        embed.add_field(
            name="👋 Sistema de Boas-vindas",
            value="`!ajuda welcome` - Configurar mensagens de entrada/saída",
            inline=False
        )
        
        embed.add_field(
            name="⭐ Sistema de XP",
            value="`!ajuda xp` - Sistema de níveis e experiência",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Diversão",
            value="`!ajuda diversao` - Jogos e entretenimento",
            inline=False
        )
        
        embed.set_footer(text="Use !ajuda [categoria] para ver comandos específicos")
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        await ctx.send(embed=embed)

    @commands.group(name='ajuda', invoke_without_subcommand=False)
    async def ajuda(self, ctx):
        """Comando de ajuda para categorias específicas"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="❓ Como usar a ajuda",
                description="Use `!cmds` para ver o menu principal ou `!ajuda [categoria]` para uma categoria específica",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    @ajuda.command(name='logs')
    async def logs(self, ctx):
        """Ajuda do sistema de logs"""
        embed = discord.Embed(
            title="📊 Sistema de Logs - Ajuda",
            description="Sistema completo de monitoramento de atividades do servidor",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="🔧 Configuração",
            value="**`!setlogchannel #canal`**\nDefine o canal onde os logs serão enviados\n*Requer: Permissão de Administrador*",
            inline=False
        )
        
        embed.add_field(
            name="📝 Logs Automáticos:",
            value="• **Entrada/saída de membros**\n• **Mensagens deletadas e editadas**\n• **Usuários banidos**\n• **Mudanças de nickname**",
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ Informações Registradas:",
            value="• Nome do usuário, ID e avatar\n• Canal onde ocorreu a ação\n• Conteúdo das mensagens\n• Horário da ação",
            inline=False
        )
        
        embed.set_footer(text="Os logs são enviados automaticamente após a configuração")
        await ctx.send(embed=embed)

    @ajuda.command(name='roleplay', aliases=['rp'])
    async def roleplay(self, ctx):
        """Ajuda do sistema de roleplay"""
        embed = discord.Embed(
            title="🎭 Sistema de Roleplay - Ajuda",
            description="Comandos de interação social entre usuários do servidor",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="💕 Ações Carinhosas",
            value="**`!abracar @usuário`** - Abraça outro usuário\n**`!beijar @usuário`** - Beija outro usuário\n**`!cafune @usuário`** - Faz cafuné relaxante",
            inline=False
        )
        
        embed.add_field(
            name="🤝 Ações Sociais",
            value="**`!tocaaqui @usuário`** - Cumprimento 'toca aqui'\n**`!dancar @usuário`** - Dança junto com outro usuário",
            inline=False
        )
        
        embed.add_field(
            name="⚔️ Ações de Combate",
            value="**`!bofetada @usuário`** - Dá uma bofetada\n**`!atacar @usuário`** - Ataca causando dano aleatório (1-100)",
            inline=False
        )
        
        embed.add_field(
            name="💡 Dicas:",
            value="• Você pode usar comandos em si mesmo\n• Todos os comandos precisam mencionar um usuário\n• As interações são apenas por diversão",
            inline=False
        )
        
        embed.set_footer(text="Divirta-se interagindo com outros membros!")
        await ctx.send(embed=embed)

    @ajuda.command(name='economia', aliases=['eco'])
    async def economia(self, ctx):
        """Ajuda do sistema de economia"""
        embed = discord.Embed(
            title="💰 Sistema de Economia - Ajuda",
            description="Sistema completo de moedas virtuais do servidor",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="💳 Comandos Básicos",
            value="**`!saldo`** - Mostra seu saldo atual\n**`!diario`** - Recompensa diária (100-300 moedas)\n**`!trabalhar`** - Trabalha para ganhar moedas (50-200)",
            inline=False
        )
        
        embed.add_field(
            name="💸 Transferências",
            value="**`!transferir @usuário [quantia]`** - Transfere moedas para outro usuário",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Rankings & Admin",
            value="**`!rankmoney`** - Ranking dos 10 mais ricos\n**`!darcoins @usuário [quantia]`** - Admin adiciona moedas",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplo:",
            value="`!transferir @João 500` - Transfere 500 moedas para João",
            inline=False
        )
        
        embed.set_footer(text="Trabalhe diariamente para acumular riqueza!")
        await ctx.send(embed=embed)

    @ajuda.command(name='moderacao', aliases=['mod'])
    async def moderacao(self, ctx):
        """Ajuda do sistema de moderação"""
        embed = discord.Embed(
            title="🛡️ Sistema de Moderação - Ajuda",
            description="Ferramentas essenciais para manter a ordem no servidor",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="🔨 Punições",
            value="**`!banir @usuário [motivo]`** - Bane um usuário\n**`!expulsar @usuário [motivo]`** - Expulsa um usuário",
            inline=False
        )
        
        embed.add_field(
            name="🔇 Sistema de Mute",
            value="**`!mutar @usuário [motivo]`** - Impede o usuário de falar\n**`!desmutar @usuário`** - Remove o mute do usuário",
            inline=False
        )
        
        embed.add_field(
            name="🧹 Limpeza",
            value="**`!limpar [quantidade]`** - Apaga mensagens do canal (padrão: 10)",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Funcionamento do Mute:",
            value="• Cria automaticamente o cargo 'Mutado'\n• Remove permissão de enviar mensagens\n• Aplica restrições a canais novos automaticamente",
            inline=False
        )
        
        embed.set_footer(text="Use os poderes de moderação com responsabilidade!")
        await ctx.send(embed=embed)

    @ajuda.command(name='sorteios')
    async def sorteios(self, ctx):
        """Ajuda do sistema de sorteios"""
        embed = discord.Embed(
            title="🎉 Sistema de Sorteios - Ajuda",
            description="Crie e gerencie sorteios interativos no seu servidor",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="🎲 Comandos",
            value="**`!comecarsorteio [prêmio]`** - Inicia um novo sorteio\n**`!encerrarsorteio`** - Encerra o sorteio atual\n**`!vencedor`** - Seleciona vencedor aleatório",
            inline=False
        )
        
        embed.add_field(
            name="📋 Como Funciona:",
            value="1. Use `!comecarsorteio` com descrição do prêmio\n2. Usuários reagem com 🎉 para participar\n3. Use `!vencedor` para escolher ganhador\n4. Bot anuncia o resultado",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Regras:",
            value="• Apenas um sorteio por canal\n• Bots não podem participar\n• Precisa ter pelo menos 1 participante",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplo:",
            value="`!comecarsorteio Nitro Classic por 1 mês`",
            inline=False
        )
        
        embed.set_footer(text="Crie sorteios divertidos para engajar sua comunidade!")
        await ctx.send(embed=embed)

    @ajuda.command(name='utils', aliases=['utilidades'])
    async def utils(self, ctx):
        """Ajuda das utilidades"""
        embed = discord.Embed(
            title="🔧 Utilidades - Ajuda",
            description="Ferramentas úteis e informações sobre o bot",
            color=discord.Color.blurple()
        )
        
        embed.add_field(
            name="🏓 Performance & Info",
            value="**`!ping`** - Mostra latência do bot\n**`!botinfo`** - Informações detalhadas do bot\n**`!uptime`** - Tempo de atividade do bot",
            inline=False
        )
        
        embed.add_field(
            name="📊 Informações Exibidas:",
            value="• Nome e ID do bot\n• Número de servidores conectados\n• Quantidade de usuários alcançados\n• Versão da biblioteca discord.py\n• Tempo online formatado",
            inline=False
        )
        
        embed.add_field(
            name="💻 Status Automático:",
            value="O bot alterna status a cada 30 segundos incluindo 'Use !cmds', 'Unibot gratuito!' e 'Prefixo: !'",
            inline=False
        )
        
        embed.set_footer(text="Comandos úteis para monitorar o bot!")
        await ctx.send(embed=embed)

    @ajuda.command(name='welcome', aliases=['boas_vindas'])
    async def welcome(self, ctx):
        """Ajuda do sistema de boas-vindas"""
        embed = discord.Embed(
            title="👋 Sistema de Boas-vindas - Ajuda",
            description="Configure mensagens automáticas para entrada e saída de membros",
            color=discord.Color.teal()
        )
        
        embed.add_field(
            name="⚙️ Configuração",
            value="**`!setentrada #canal`** - Define canal para boas-vindas\n**`!setsaida #canal`** - Define canal para despedidas\n*Requer: Permissão de Administrador*",
            inline=False
        )
        
        embed.add_field(
            name="📝 Mensagens Automáticas:",
            value="**Entrada**: `🎉 Olá @usuário, bem-vindo ao servidor!`\n**Saída**: `👋 O usuário [nome] saiu do servidor.`",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Funcionamento:",
            value="• Admin define canais usando os comandos\n• Bot detecta entrada/saída automaticamente\n• Configurações salvas em arquivo JSON\n• Configurações individuais por servidor",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplo:",
            value="`!setentrada #boas-vindas`\n`!setsaida #despedidas`",
            inline=False
        )
        
        embed.set_footer(text="Crie uma experiência acolhedora para novos membros!")
        await ctx.send(embed=embed)

    @ajuda.command(name='xp', aliases=['nivel'])
    async def xp(self, ctx):
        """Ajuda do sistema de XP"""
        embed = discord.Embed(
            title="⭐ Sistema de XP - Ajuda",
            description="Sistema automático de níveis e experiência baseado na atividade",
            color=discord.Color.from_rgb(255, 215, 0)
        )
        
        embed.add_field(
            name="📊 Comandos",
            value="**`!xp [@usuário]`** - Mostra XP e nível atual com barra de progresso\n**`!topxp`** - Ranking dos 10 usuários com maior nível/XP",
            inline=False
        )
        
        embed.add_field(
            name="⚡ Como Ganhar XP:",
            value="• **Mensagens**: 10-20 XP por mensagem enviada\n• **Automático**: XP dado automaticamente ao falar\n• **Aleatório**: Quantidade varia para manter dinamismo\n• **Sem Spam**: Bots não ganham XP",
            inline=False
        )
        
        embed.add_field(
            name="🎚️ Sistema de Níveis:",
            value="• **Fórmula**: XP necessário = 5×(nível²) + 50×nível + 100\n• **Progressão**: Cada nível fica mais difícil\n• **Anúncio**: Bot parabeniza quando você sobe de nível",
            inline=False
        )
        
        embed.add_field(
            name="📈 Barra de Progresso:",
            value="**Formato**: `[████████████--------] (1250/1500)`\n• 20 caracteres de largura\n• Mostra XP atual / XP máximo do nível",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Ranking:",
            value="• Ordenação por nível primeiro, depois por XP\n• Top 10 usuários mais ativos\n• Atualizado em tempo real\n• Considera todos os usuários do servidor",
            inline=False
        )
        
        embed.set_footer(text="Seja ativo no chat para subir de nível!")
        await ctx.send(embed=embed)

    @ajuda.command(name='diversao', aliases=['fun', 'entretenimento'])
    async def diversao(self, ctx):
        """Ajuda do sistema de diversão"""
        embed = discord.Embed(
            title="🎮 Sistema de Diversão - Ajuda",
            description="Comandos bilíngues para entretenimento e jogos interativos",
            color=discord.Color.from_rgb(255, 105, 180)
        )
        
        embed.add_field(
            name="🎯 Jogos Interativos",
            value="**`!verdade`** / **`!truth`** - Perguntas para verdade ou desafio\n**`!desafio`** / **`!dare`** - Desafios divertidos para o jogo\n**`!8ball [pergunta]`** / **`!bola8 [pergunta]`** - Bola mágica 8",
            inline=False
        )
        
        embed.add_field(
            name="😄 Entretenimento Social",
            value="**`!piada`** / **`!joke`** - Piadas aleatórias engraçadas\n**`!ship @user1 @user2`** / **`!amor @user1 @user2`** - Compatibilidade entre usuários\n**`!gay @usuário`** / **`!gayrate @usuário`** - Medidor gay divertido",
            inline=False
        )
        
        embed.add_field(
            name="🎲 Utilidades Aleatórias",
            value="**`!roleta [opção1, opção2, ...]`** / **`!roulette [option1, option2, ...]`** - Escolher entre opções\n**`!estatisticas`** / **`!stats`** - Ver estatísticas de uso dos comandos",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplos de Uso:",
            value="**PT**: `!8ball Vou passar na prova?`, `!ship @João @Maria`, `!roleta pizza, hambúrguer, sushi`\n**EN**: `!8ball Will I pass the exam?`, `!ship @John @Mary`, `!roulette pizza, burger, sushi`",
            inline=False
        )
        
        embed.add_field(
            name="🌐 Recursos Especiais:",
            value="• **Bilíngue**: Comandos funcionam em PT e EN\n• **Interativo**: Comandos precisam menções/parâmetros\n• **Estatísticas**: Acompanhe uso dos comandos\n• **Personalização**: Configuração por servidor",
            inline=False
        )
        
        embed.set_footer(text="Divirta-se com jogos em dois idiomas!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpSystem(bot))
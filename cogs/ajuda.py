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
            # Se alguém usar apenas !ajuda sem subcomando, mostra mensagem orientativa
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
            name="📝 Logs Automáticos Monitorados:",
            value="• **Entrada de membros** - Quando alguém entra no servidor\n" +
                  "• **Saída de membros** - Quando alguém sai do servidor\n" +
                  "• **Mensagens deletadas** - Registro de mensagens apagadas\n" +
                  "• **Mensagens editadas** - Antes/depois das edições\n" +
                  "• **Usuários banidos** - Quando alguém é banido\n" +
                  "• **Mudanças de nickname** - Alterações no apelido",
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ Informações Exibidas:",
            value="• Nome do usuário e ID\n• Avatar/foto de perfil\n• Canal onde ocorreu a ação\n• Conteúdo das mensagens (quando aplicável)\n• Horário da ação",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplo de Uso:",
            value="`!setlogchannel #logs-servidor`",
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
            value="**`!abracar @usuário`** (aliases: `!hug`, `!abraço`)\nAbraça outro usuário com carinho\n\n" +
                  "**`!beijar @usuário`** (aliases: `!kiss`, `!beijo`)\nBeija outro usuário com afeto\n\n" +
                  "**`!cafune @usuário`** (aliases: `!headpat`, `!pat`)\nFaz cafuné relaxante no usuário",
            inline=False
        )
        
        embed.add_field(
            name="🤝 Ações Sociais",
            value="**`!tocaaqui @usuário`** (aliases: `!highfive`, `!hifive`)\nCumprimenta com um 'toca aqui'\n\n" +
                  "**`!dancar @usuário`** (alias: `!dance`)\nDança junto com outro usuário",
            inline=False
        )
        
        embed.add_field(
            name="⚔️ Ações de Combate",
            value="**`!bofetada @usuário`** (aliases: `!slap`, `!tapa`)\nDá uma bofetada no usuário\n\n" +
                  "**`!atacar @usuário`** (alias: `!attack`)\nAtaca causando dano aleatório (1-100 pontos)",
            inline=False
        )
        
        embed.add_field(
            name="📋 Comandos de Ajuda",
            value="**`!roleplay`** ou **`!rp`** - Lista resumida de comandos\n**`!helproleplay`** - Ajuda completa e detalhada",
            inline=False
        )
        
        embed.add_field(
            name="💡 Dicas Importantes:",
            value="• Você pode usar comandos em si mesmo para ações solo\n• Todos os comandos precisam mencionar um usuário\n• As interações são apenas por diversão, sem efeitos reais",
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
            value="**`!saldo`**\nMostra seu saldo atual de moedas\n\n" +
                  "**`!diario`**\nColeta recompensa diária (100-300 moedas)\n\n" +
                  "**`!trabalhar`**\nTrabalha para ganhar moedas (50-200)",
            inline=False
        )
        
        embed.add_field(
            name="💸 Transferências",
            value="**`!transferir @usuário [quantia]`**\nTransfere moedas para outro usuário\n*Obs: Não pode transferir para si mesmo*",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Rankings",
            value="**`!rankmoney`**\nMostra o ranking dos 10 usuários mais ricos do servidor",
            inline=False
        )
        
        embed.add_field(
            name="👑 Comandos de Admin",
            value="**`!darcoins @usuário [quantia]`**\nAdiciona moedas para um usuário\n*Requer: Permissão de Administrador*",
            inline=False
        )
        
        embed.add_field(
            name="📊 Sistema de Dados:",
            value="• **Saldo** - Quantidade de moedas atual\n• **Trabalhos** - Contador de vezes que trabalhou\n• Dados salvos automaticamente em JSON",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplos de Uso:",
            value="`!transferir @João 500` - Transfere 500 moedas para João\n`!darcoins @Maria 1000` - Admin dá 1000 moedas para Maria",
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
            name="🔨 Punições Permanentes",
            value="**`!banir @usuário [motivo]`**\nBane um usuário do servidor\n*Requer: Permissão de Banir Membros*\n\n" +
                  "**`!expulsar @usuário [motivo]`**\nExpulsa um usuário do servidor\n*Requer: Permissão de Expulsar Membros*",
            inline=False
        )
        
        embed.add_field(
            name="🔇 Sistema de Mute",
            value="**`!mutar @usuário [motivo]`**\nImpede o usuário de enviar mensagens\n*Requer: Permissão de Gerenciar Cargos*\n\n" +
                  "**`!desmutar @usuário`**\nRemove o mute do usuário\n*Requer: Permissão de Gerenciar Cargos*",
            inline=False
        )
        
        embed.add_field(
            name="🧹 Limpeza de Chat",
            value="**`!limpar [quantidade]`**\nApaga mensagens do canal (padrão: 10)\n*Requer: Permissão de Gerenciar Mensagens*\n*Máximo recomendado: 100 mensagens*",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Funcionamento do Mute:",
            value="• Cria automaticamente o cargo 'Mutado' se não existir\n• Remove permissão de enviar mensagens em todos os canais\n• Aplica as restrições a canais novos automaticamente",
            inline=False
        )
        
        embed.add_field(
            name="📝 Sobre os Motivos:",
            value="• Se não especificar motivo, será usado 'Sem motivo'\n• Motivos são registrados nos logs do Discord\n• Use motivos descritivos para melhor organização",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplos de Uso:",
            value="`!banir @usuário spam excessivo`\n`!limpar 50`\n`!mutar @usuário comportamento inadequado`",
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
            name="🎲 Gerenciar Sorteios",
            value="**`!comecarsorteio [prêmio]`**\nInicia um novo sorteio com o prêmio especificado\n\n" +
                  "**`!encerrarsorteio`**\nEncerra o sorteio atual (não seleciona vencedor)\n\n" +
                  "**`!cancelarsorteio`**\nEncerra o sorteio atual (não seleciona vencedor)\n\n" +
                  "**`!vencedor`**\nSeleciona aleatoriamente um vencedor do sorteio ativo",
            inline=False
        )
        
        embed.add_field(
            name="📋 Como Funciona:",
            value="1. **Início**: Use `!comecarsorteio` com descrição do prêmio\n" +
                  "2. **Participação**: Usuários reagem com 🎉 para participar\n" +
                  "3. **Seleção**: Use `!vencedor` para escolher ganhador aleatório\n" +
                  "4. **Resultado**: Bot anuncia o vencedor automaticamente",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Regras e Limitações:",
            value="• Apenas um sorteio por canal simultaneamente\n• Bots não podem participar dos sorteios\n• Precisa ter pelo menos 1 participante para sortear\n• Reactions são removidas ao encerrar",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplos de Uso:",
            value="`!comecarsorteio Nitro Classic por 1 mês`\n`!comecarsorteio 1000 moedas do servidor`\n`!comecarsorteio Cargo VIP`",
            inline=False
        )
        
        embed.add_field(
            name="💡 Dicas:",
            value="• Seja claro na descrição do prêmio\n• Aguarde participantes antes de sortear\n• Use `!encerrarsorteio` se precisar cancelar\n• Mantenha os prêmios justos e atraentes",
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
            name="🏓 Performance",
            value="**`!ping`**\nMostra a latência atual do bot em milissegundos\nÚtil para verificar se o bot está respondendo bem",
            inline=False
        )
        
        embed.add_field(
            name="🤖 Informações do Bot",
            value="**`!botinfo`**\nExibe informações detalhadas sobre o bot:\n• Nome e ID do bot\n• Número de servidores conectados\n• Quantidade de usuários alcançados\n• Versão da biblioteca discord.py",
            inline=False
        )
        
        embed.add_field(
            name="🕒 Tempo de Atividade",
            value="**`!uptime`**\nMostra há quanto tempo o bot está online\nFormato: dias, horas, minutos e segundos",
            inline=False
        )
        
        embed.add_field(
            name="📊 Status Automático:",
            value="• O bot alterna status a cada 30 segundos\n• Status incluem: 'Use !cmds', 'Unibot gratuito!', 'Prefixo: !'\n• Ajuda usuários a descobrirem comandos básicos",
            inline=False
        )
        
        embed.add_field(
            name="💻 Informações Técnicas:",
            value="• Plataforma: " + "Linux/Windows/Mac" + "\n• RAM: Monitoramento via psutil\n• Versão Python: Detectada automaticamente\n• Biblioteca: discord.py 2.5.2",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplos de Resposta:",
            value="**Ping**: `🏓 Pong! Latência: 45ms`\n**Uptime**: `🕒 Uptime: 2:14:35`\n**Info**: Embed com estatísticas completas",
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
            name="⚙️ Configuração de Canais",
            value="**`!setentrada #canal`**\nDefine o canal para mensagens de boas-vindas\n*Requer: Permissão de Administrador*\n\n" +
                  "**`!setsaida #canal`**\nDefine o canal para mensagens de despedida\n*Requer: Permissão de Administrador*",
            inline=False
        )
        
        embed.add_field(
            name="📝 Mensagens Automáticas:",
            value="**Entrada de Membro:**\n`🎉 Olá @usuário, bem-vindo ao servidor! Não se esqueça de ler as regras e se divertir bastante!`\n\n" +
                  "**Saída de Membro:**\n`👋 O usuário [nome] saiu do servidor. Até a próxima!`",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Como Funciona:",
            value="• **Configuração**: Admin define canais usando os comandos\n• **Automático**: Bot detecta entrada/saída de membros\n• **Envio**: Mensagens são enviadas nos canais configurados\n• **Segurança**: Configurações salvas em arquivo JSON",
            inline=False
        )
        
        embed.add_field(
            name="💾 Armazenamento:",
            value="• Configurações salvas em `data/welcome_config.json`\n• Backup automático das configurações\n• Diretório criado automaticamente se não existir\n• Configurações individuais por servidor",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplos de Configuração:",
            value="`!setentrada #boas-vindas`\n`!setsaida #despedidas`\n`!setentrada #geral` (usar mesmo canal para ambos)",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Troubleshooting:",
            value="• Verifique se o bot tem permissão no canal\n• Confirme se o canal ainda existe\n• Bot precisa de permissão para enviar mensagens\n• Configurações são por servidor (não globais)",
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
            name="📊 Comandos de Consulta",
            value="**`!xp [@usuário]`**\nMostra XP e nível atual (seu ou de outro usuário)\nInclui barra de progresso visual\n\n" +
                  "**`!topxp`**\nRanking dos 10 usuários com maior nível/XP do servidor",
            inline=False
        )
        
        embed.add_field(
            name="⚡ Como Ganhar XP:",
            value="• **Mensagens**: Ganhe 10-20 XP por mensagem enviada\n• **Automático**: XP é dado automaticamente ao falar\n• **Aleatório**: Quantidade varia para manter dinamismo\n• **Sem Spam**: Bots não ganham XP",
            inline=False
        )
        
        embed.add_field(
            name="🎚️ Sistema de Níveis:",
            value="• **Fórmula**: XP necessário = 5×(nível²) + 50×nível + 100\n• **Exemplo**: Nível 1→2 = 155 XP, Nível 2→3 = 220 XP\n• **Progressão**: Cada nível fica mais difícil de alcançar\n• **Anúncio**: Bot parabeniza quando você sobe de nível",
            inline=False
        )
        
        embed.add_field(
            name="📈 Barra de Progresso:",
            value="**Formato**: `[████████████--------] (1250/1500)`\n• **Cheia**: █ (XP atual)\n• **Vazia**: - (XP restante)\n• **Total**: 20 caracteres de largura\n• **Números**: XP atual / XP máximo do nível",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Sistema de Ranking:",
            value="• **Ordenação**: Por nível primeiro, depois por XP\n• **Top 10**: Mostra os usuários mais ativos\n• **Atualização**: Ranking atualizado em tempo real\n• **Global**: Considera todos os usuários do servidor",
            inline=False
        )
        
        embed.add_field(
            name="💾 Dados Salvos:",
            value="• **XP atual**: Experiência acumulada no nível\n• **Nível**: Posição atual no sistema\n• **Arquivo**: `data/xp.json` (backup automático)\n• **Persistência**: Dados mantidos entre reinicializações",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplos de Resposta:",
            value="**XP**: `📊 @Usuário - Nível: 5`\n`[████████--------] (420/650)`\n**Level Up**: `🎉 @Usuário subiu para o nível 6!`",
            inline=False
        )
        
        embed.set_footer(text="Seja ativo no chat para subir de nível!")
        await ctx.send(embed=embed)

    @ajuda.command(name='diversao', aliases=['fun', 'entretenimento'])
    async def diversao(self, ctx):
        """Ajuda do sistema de diversão"""
        embed = discord.Embed(
            title="🎮 Sistema de Diversão - Ajuda | Fun System - Help",
            description="Comandos bilíngues para entretenimento e jogos | Bilingual commands for entertainment and games",
            color=discord.Color.from_rgb(255, 105, 180)
        )
        
        embed.add_field(
            name="⚙️ Configuração de Idioma | Language Settings",
            value="**`!setlang pt`** - Define idioma para português\n**`!setlang en`** - Set language to English\n*Afeta todas as respostas do bot | Affects all bot responses*",
            inline=False
        )
        
        embed.add_field(
            name="🎲 Jogos de Sorte | Luck Games",
            value="**`!dado [lados]`** / **`!dice [sides]`**\nRola dado personalizado | Roll custom dice (padrão/default: 6)\n\n" +
                  "**`!moeda`** / **`!coin`**\nCara ou coroa | Heads or tails\n\n" +
                  "**`!rps [pedra/papel/tesoura]`** / **`!rps [rock/paper/scissors]`**\nPedra, papel e tesoura | Rock, paper, scissors\n\n" +
                  "**`!8ball [pergunta]`** / **`!bola8 [pergunta]`**\nBola 8 mágica | Magic 8-ball oracle\n\n" +
                  "**`!aleatorio [min] [max]`** / **`!random [min] [max]`**\nNúmero aleatório | Random number",
            inline=False
        )
        
        embed.add_field(
            name="😄 Entretenimento | Entertainment",
            value="**`!piada`** / **`!joke`**\nPiadas aleatórias | Random jokes\n\n" +
                  "**`!curiosidade`** / **`!fact`**\nFatos interessantes | Interesting facts\n\n" +
                  "**`!pergunta`** / **`!question`**\nPerguntas para reflexão | Thought-provoking questions\n\n" +
                  "**`!escolher [opção1, opção2, ...]`** / **`!choose [option1, option2, ...]`**\nEscolhe uma opção | Choose an option\n\n" +
                  "**`!love @usuário`**\nCalculadora do amor | Love calculator\n\n" +
                  "**`!motivar`** / **`!motivate`**\nFrases motivacionais | Motivational quotes",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Exemplos de Uso | Usage Examples:",
            value="**PT**: `!dado 20`, `!8ball Vou passar na prova?`, `!escolher pizza, hambúrguer, sushi`\n" +
                  "**EN**: `!dice 20`, `!8ball Will I pass the exam?`, `!choose pizza, burger, sushi`",
            inline=False
        )
        
        embed.add_field(
            name="🌐 Recursos Especiais | Special Features:",
            value="• **Bilíngue**: Comandos funcionam em PT e EN | Commands work in PT and EN\n" +
                  "• **APIs**: JokeAPI, FactAPI para conteúdo dinâmico | Dynamic content\n" +
                  "• **Personalização**: Configuração por servidor | Per-server settings\n" +
                  "• **Interativo**: Alguns comandos precisam menções/parâmetros | Interactive commands",
            inline=False
        )
        
        embed.add_field(
            name="💡 Dicas | Tips:",
            value="**PT**: Use comandos em português para respostas em português\n**EN**: Use English commands for English responses\n• Configuração de idioma salva por servidor | Language settings saved per server\n• Todos os jogos são justos e aleatórios | All games are fair and random",
            inline=False
        )
        
        embed.set_footer(text="Divirta-se com jogos em dois idiomas! | Have fun with bilingual games!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpSystem(bot))

# 🤖 Unibot - Versão Gratuita

O **Unibot** é um bot profissional para Discord com diversos sistemas essenciais: economia, moderação, boas-vindas, XP, sorteios, utilidades e muito mais.  
Essa versão é 100% funcional, gratuita e pronta para rodar em múltiplos servidores sem painel ou dashboard.

---

## ✅ Funcionalidades Inclusas

- 💰 Economia básica (`!saldo`, `!trabalhar`, `!comprar`, `!vender`, `!daily`)
- 🛡️ Moderação (`!banir`, `!mutar`, `!avisar`, `!limparmensagem`)
- 🎁 Sorteios (`!comecarsorteio`, `!encerrarsorteio`, `!vencedor`)
- 👋 Boas-vindas automáticas com frases bonitas e profissionais
- 📈 XP e Nível (`!xp`, `!topxp`)
- ⚙️ Status rotativo (`!statusmodo`, `!statusmanual`)
- ⚡ Comandos de utilidade (`!ping`, `!botinfo`, `!serverinfo`, `!avatar`)
- 🎭 Roleplay interativo (`!abraçar`, `!beijar`, `!atacar`, etc.)
- 📋 Sistema de ajuda organizado por categorias

> ⚠️ Nesta versão gratuita, os canais e mensagens estão pré-definidos e não podem ser configurados via comandos (função reservada à versão paga).

---

## 🧑‍💻 Como Rodar Localmente

1. Clone o projeto:
   ```bash
   git clone https://github.com/seu-usuario/unibot-gratis.git
   cd unibot-gratis
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` com o seguinte conteúdo:
   ```env
   TOKEN=SEU_TOKEN_DO_DISCORD
   ```

4. Execute o bot:
   ```bash
   python main.py
   ```

---

## ☁️ Como Hospedar Gratuitamente no Render

> A Render permite hospedar seu bot gratuitamente, com hibernação automática após 15 minutos de inatividade.

### 🔧 Passo a passo:

1. Suba o projeto para um repositório no GitHub (não inclua o `.env`)
2. Vá até [https://render.com](https://render.com) e crie sua conta
3. Clique em **New Web Service** e conecte seu repositório
4. Configure:
   - **Name:** unibot
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
5. Em *Environment Variables*, adicione:
   - `TOKEN` → seu token do Discord

---

## 🔁 Mantendo o Bot Online com AutoPing (UptimeRobot)

1. Vá para [https://uptimerobot.com](https://uptimerobot.com)
2. Crie uma conta gratuita
3. Clique em **Create Monitor**
   - **Monitor Type:** HTTP(s)
   - **URL:** `https://SEUAPP.onrender.com`
   - **Interval:** 5 minutos
4. Pronto! O UptimeRobot enviará pings para manter seu bot vivo.

### 🧠 Código `keep_alive` no `main.py`:
Adicione isso antes do `bot.run(...)`:

```python
from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "Estou vivo!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
```

---

## 📂 Estrutura do Projeto

```
Unibot/
├── cogs/
│   ├── ajuda.py
│   ├── economia.py
│   ├── moderacao.py
│   ├── painel_logs.py
│   ├── roleplay.py
│   ├── sorteios.py
│   ├── status.py
│   ├── utilidades.py
│   ├── welcome.py
│   └── xp.py
├── main.py
├── requirements.txt
├── .env (NÃO INCLUIR NO GITHUB)
└── README.md
```

---

## ⚠️ Avisos Importantes

- **Nunca suba o `.env` para o GitHub!**
- Use o token do Discord apenas via variáveis de ambiente (`getenv("TOKEN")`)
- Para mais comandos, personalizações, painel de configuração, dashboards e suporte completo, conheça a versão paga!

---

Feito com 💙 por [SeuNome] • Projeto Unibot Gratuito

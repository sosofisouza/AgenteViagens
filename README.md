# Agente de Viagens com Semantic Kernel e GitHub Models✈️💙

Este projeto é um agente simples de viagens criado em Python. Ele usa o **Semantic Kernel** para organizar a lógica do agente e o **GitHub Models** como serviço de IA para gerar roteiros de viagem em português.

O agente sugere destinos aleatórios e, quando a IA está disponível, monta um roteiro prático de 1 dia dividido em **manhã**, **tarde** e **noite**.

---

## ✨ Funcionalidades

- Sugere destinos aleatórios para viagem.
- Evita repetir o último destino sugerido.
- Gera roteiros de 1 dia usando IA.
- Mantém o contexto do destino atual durante a conversa.
- Permite pedir outro destino caso o usuário não goste da sugestão.
- Usa GitHub Models com cliente compatível com OpenAI.
- Usa `truststore` para melhorar a compatibilidade SSL em Windows e redes corporativas.
- Continua funcionando parcialmente mesmo se a IA não estiver disponível.

---

## 🧠 Como o agente funciona

Fluxo simplificado:

```text
Usuário
  ↓
agentkernel.py
  ↓
Semantic Kernel
  ↓
Plugin local de destinos
  ↓
Cliente AsyncOpenAI
  ↓
GitHub Models API
  ↓
Resposta com roteiro de viagem
```

O projeto possui um plugin local chamado `DestinationPlugin`, responsável por escolher destinos aleatórios. Depois disso, o destino escolhido é enviado para o modelo de IA, que monta o roteiro.

---

## 🛠️ Tecnologias utilizadas

- Python
- Semantic Kernel
- GitHub Models
- OpenAI Python SDK
- HTTPX
- python-dotenv
- truststore

---

## 📋 Pré-requisitos

Antes de executar o projeto, você precisa ter:

- Python 3.10 ou superior instalado.
- Uma conta no GitHub.
- Um token do GitHub com permissão para usar GitHub Models.
- Um ambiente virtual Python configurado.

---

## ⚙️ Configuração do ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie e ative o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No macOS ou Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install semantic-kernel openai httpx python-dotenv truststore
```

Depois instale com:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração do `.env`

Crie um arquivo chamado `.env` na raiz do projeto.

Exemplo:

```env
GITHUB_TOKEN=github_pat_seu_token_aqui
GITHUB_MODELS_BASE_URL=https://models.github.ai/inference
MODEL_ID=openai/gpt-4o-mini
```

> Nunca suba o arquivo `.env` para o GitHub.
> Ele contém informações sensíveis, como o token de acesso.

---

## 🔐 Segurança

Adicione um arquivo `.gitignore` ao projeto para evitar subir arquivos sensíveis ou desnecessários.

Exemplo de `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.vscode/
.idea/
```

---

## 🚀 Como executar

Com o ambiente virtual ativado, execute:

```bash
python agentkernel.py
```

Você verá algo parecido com:

```text
Token carregado? True
Prefixo do token: github_pat_1
Base URL: https://models.github.ai/inference
Modelo: openai/gpt-4o-mini
Teste Semantic Kernel: Semantic Kernel funcionando.

✈️ Agente de viagens iniciado!
Digite algo como:
- "planeje um dia de viagem"
Digite "sair" para encerrar.
```

---

## 💬 Exemplos de uso

### Planejar uma viagem

```text
Você: planeje um dia de viagem
```

O agente irá sortear um destino e pedir para a IA montar um roteiro.

Exemplo de resposta:

```text
Agente:
Que tal conhecer Paris, França?

Manhã:
- Visite a Torre Eiffel.
- Caminhe pelo Champ de Mars.

Tarde:
- Conheça o Museu do Louvre.
- Faça uma pausa em um café local.

Noite:
- Passeie pelo Rio Sena.
- Experimente uma comida típica francesa.
```

### Pedir outro destino

```text
Você: quero outro destino
```

O agente sorteará outro local e gerará um novo roteiro.

### Continuar a conversa

```text
Você: qual comida típica eu deveria experimentar?
```

O agente responderá considerando o destino atual da conversa.

---


## 📁 Estrutura do projeto

```text
.
├── agentkernel.py
├── README.md
├── requirements.txt
├── .env
└── .gitignore
```


---

## 🚨 Tratamento de erros

O projeto possui uma função para exibir erros de forma mais detalhada:

```python
def imprimir_erro_detalhado(e: Exception):
    print("\n⚠️ Não consegui chamar o modelo de IA.")
    print(f"Tipo do erro: {type(e)}")
    print(f"Detalhe técnico: {repr(e)}")
    print(f"Causa: {repr(getattr(e, '__cause__', None))}")
    print(f"Contexto: {repr(getattr(e, '__context__', None))}")
```

Essa função ajuda a descobrir se o problema está relacionado a:

- autenticação;
- conexão;
- certificado SSL;
- modelo inválido;
- indisponibilidade do serviço;
- erro de configuração.

---

## 🧩 Problemas comuns

### `GITHUB_TOKEN não encontrado`

Verifique se o arquivo `.env` existe e se a variável está escrita corretamente:

```env
GITHUB_TOKEN=github_pat_seu_token_aqui
```

### `APIConnectionError('Connection error.')`

Possível problema de conexão HTTPS ou certificado SSL.

Verifique se o código está usando `truststore`:

```python
ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
```

### Erro de modelo não encontrado

Confirme se o `MODEL_ID` está correto:

```env
MODEL_ID=openai/gpt-4o-mini
```

### Erro de autenticação

Confirme se o token do GitHub é válido e possui permissão para usar GitHub Models.

---

## 🔮 Melhorias futuras

Algumas ideias para evoluir o projeto:

- Salvar histórico da conversa em arquivo.
- Permitir que o usuário escolha o tipo de viagem.
- Adicionar orçamento estimado.
- Adicionar duração personalizada da viagem.
- Integrar busca de clima.
- Criar interface web.
- Adicionar testes automatizados.
- Separar o código em módulos.

---

## 📌 Observação importante

Este projeto foi criado com foco em aprendizado. Ele demonstra como integrar:

- um plugin local com Semantic Kernel;
- um modelo de IA hospedado no GitHub Models;
- configuração segura via `.env`;
- tratamento de erros de conexão;
- uso de certificados confiáveis do sistema operacional com `truststore`.

---


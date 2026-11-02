<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rounded&color=0:fbcfe8,100:f9a8d4&height=170&section=header&text=Agente%20de%20Viagens&fontSize=42&fontColor=831843&fontAlignY=42&desc=Semantic%20Kernel%20%C2%B7%20GitHub%20Models&descSize=16&descAlignY=68" width="100%" />

<img src="https://readme-typing-svg.demolab.com?font=Quicksand&weight=600&size=19&pause=1400&color=DB2777&center=true&vCenter=true&width=620&lines=%22Planeje+um+dia+de+viagem%22;Manh%C3%A3%2C+tarde+e+noite+em+um+roteiro;%22Quero+outro+destino%22" />

</div>

<br>

### Sobre o projeto

Agente de viagens em Python que sorteia um destino e pede para a IA montar um roteiro de 1 dia, dividido em **manhã**, **tarde** e **noite**. Usa o **Semantic Kernel** para organizar a lógica do agente e o **GitHub Models** como serviço de IA.

<br>

### Funcionalidades

- Sugere destinos aleatórios, sem repetir o último
- Gera roteiros de 1 dia com IA
- Mantém o destino atual como contexto da conversa
- Troca o destino quando você não gosta da sugestão
- Continua funcionando, só com os destinos, se a IA não estiver disponível

<br>

### Como funciona

```
Você  ──►  agentkernel.py  ──►  Semantic Kernel
                                     │
                     Plugin local de destinos (sorteio)
                                     │
                         GitHub Models  ──►  roteiro de viagem
```

O plugin `DestinationPlugin` escolhe o destino. Em seguida, o destino é enviado ao modelo de IA, que monta o roteiro.

<br>

### Tecnologias

<div align="center">
  <img src="https://skillicons.dev/icons?i=py,github&theme=light" />
  <br>
  <sub>Python · Semantic Kernel · GitHub Models · OpenAI SDK · HTTPX · truststore</sub>
</div>

<br>

### Como executar

**1. Instalar**

```bash
git clone https://github.com/sosofisouza/AgenteViagens.git
cd AgenteViagens
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux e macOS
pip install -r requirements.txt
```

**2. Configurar**

Crie um arquivo `.env` na raiz do projeto:

```env
GITHUB_TOKEN=seu_token_do_github
GITHUB_MODELS_BASE_URL=https://models.github.ai/inference
MODEL_ID=openai/gpt-4o-mini
```

O token precisa ter permissão para usar o GitHub Models. O `.env` está no `.gitignore` e nunca vai para o repositório.

**3. Executar**

```bash
python agentkernel.py
```

<br>

### Exemplo de conversa

```text
Você: planeje um dia de viagem

Agente:
Que tal conhecer Paris, França?

Manhã:  Torre Eiffel e Champ de Mars
Tarde:  Museu do Louvre e um café local
Noite:  passeio pelo Rio Sena e comida típica

Você: quero outro destino
Você: qual comida típica eu deveria experimentar?
```

<br>

<details>
<summary><b>Problemas comuns</b></summary>
<br>

| Mensagem | O que fazer |
|:---|:---|
| `GITHUB_TOKEN não encontrado` | Confira se o `.env` existe e se o nome da variável está correto |
| `APIConnectionError` | Problema de conexão ou certificado SSL. O projeto usa `truststore` para usar os certificados do sistema |
| Modelo não encontrado | Confira o `MODEL_ID` |
| Erro de autenticação | Confira se o token é válido e tem permissão para o GitHub Models |

</details>

<br>

### Próximos passos

- Escolher o tipo de viagem, o orçamento e a duração
- Integrar a previsão do tempo
- Criar uma interface web
- Separar o código em módulos e adicionar testes

<br>

<div align="center">

Feito por **Sofia Rodrigues** &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/sosofisouza/)

</div>

<img src="https://capsule-render.vercel.app/api?type=rounded&color=0:fbcfe8,100:f9a8d4&height=60&section=footer" width="100%" />

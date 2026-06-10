import os
import asyncio
import random
import ssl
import httpx
import truststore

from dotenv import load_dotenv
from openai import APIConnectionError, AsyncOpenAI

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAIChatPromptExecutionSettings,
)


class DestinationPlugin:
    """Lista de destinos aleatórios para férias."""

    def __init__(self):
        self.destinations = [
            "Barcelona, Espanha",
            "Paris, França",
            "Berlim, Alemanha",
            "Tóquio, Japão",
            "Sydney, Austrália",
            "Nova York, EUA",
            "Cairo, Egito",
            "Cidade do Cabo, África do Sul",
            "Rio de Janeiro, Brasil",
            "Bali, Indonésia",
        ]
        self.last_destination = None

    @kernel_function
    def get_random_destination(self) -> str:
        available = self.destinations.copy()

        if self.last_destination and len(available) > 1:
            available.remove(self.last_destination)

        destination = random.choice(available)
        self.last_destination = destination

        return destination


def quer_planejamento(texto: str) -> bool:
    texto = texto.lower()
    gatilhos = [
        "planeje um dia",
        "planeja um dia",
        "roteiro de 1 dia",
        "roteiro de um dia",
        "planeje uma viagem",
        "planejar viagem",
        "quero planejar uma viagem",
    ]
    return any(g in texto for g in gatilhos)


def quer_outro_destino(texto: str) -> bool:
    texto = texto.lower()
    gatilhos = [
        "não gostei",
        "nao gostei",
        "quero outro",
        "outro destino",
        "sugira outro",
        "me dê outro",
        "me de outro",
        "troque o destino",
    ]
    return any(g in texto for g in gatilhos)


async def gerar_resposta_ia(chat_service, history, prompt_usuario):
    history.add_user_message(prompt_usuario)

    response = await chat_service.get_chat_message_content(
        chat_history=history,
        settings=OpenAIChatPromptExecutionSettings(
            service_id="agent",
            temperature=0.7,
            max_tokens=800,
        ),
    )

    history.add_message(response)
    return response.content


def imprimir_erro_detalhado(e: Exception):
    print("\n⚠️ Não consegui chamar o modelo de IA.")
    print(f"Tipo do erro: {type(e)}")
    print(f"Detalhe técnico: {repr(e)}")
    print(f"Causa: {repr(getattr(e, '__cause__', None))}")
    print(f"Contexto: {repr(getattr(e, '__context__', None))}")


async def main():
    load_dotenv(override=True)

    token = os.getenv("GITHUB_TOKEN")
    base_url = os.getenv(
        "GITHUB_MODELS_BASE_URL",
        "https://models.github.ai/inference",
    )
    model_id = os.getenv("MODEL_ID", "openai/gpt-4o-mini")

    print("Token carregado?", bool(token))
    print("Prefixo do token:", token[:12] if token else "nenhum")
    print("Base URL:", base_url)
    print("Modelo:", model_id)

    kernel = Kernel()
    plugin = DestinationPlugin()
    kernel.add_plugin(plugin, plugin_name="destinations")

    chat_service = None
    history = None
    http_client = None

    if token:
        try:
            # Usa a cadeia de certificados do sistema operacional.
            # Isso costuma resolver erros SSL em Windows/rede corporativa.
            ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

            http_client = httpx.AsyncClient(
                verify=ssl_context,
                timeout=60.0,
            )

            client = AsyncOpenAI(
                api_key=token,
                base_url=base_url,
                http_client=http_client,
                default_headers={
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            )

            chat_service = OpenAIChatCompletion(
                ai_model_id=model_id,
                async_client=client,
                service_id="agent",
            )

            kernel.add_service(chat_service)

            # Teste rápido do Semantic Kernel.
            teste_history = ChatHistory()
            teste_history.add_user_message(
                "Responda apenas: Semantic Kernel funcionando."
            )

            teste_response = await chat_service.get_chat_message_content(
                chat_history=teste_history,
                settings=OpenAIChatPromptExecutionSettings(
                    service_id="agent",
                    temperature=0.2,
                    max_tokens=50,
                ),
            )

            print("Teste Semantic Kernel:", teste_response.content)

            history = ChatHistory()
            history.add_system_message(
                "Você é um assistente de viagens. "
                "Sempre responda em português. "
                "Quando receber um destino específico, monte um plano prático de 1 dia nesse local. "
                "Organize em manhã, tarde e noite. "
                "Se o usuário fizer perguntas adicionais, continue falando sobre o destino atual."
            )

        except Exception as e:
            print("⚠️ Não foi possível inicializar o serviço de IA.")
            imprimir_erro_detalhado(e)

            chat_service = None
            history = None

            if http_client:
                await http_client.aclose()
                http_client = None

    else:
        print("⚠️ GITHUB_TOKEN não encontrado. O modo com IA não estará disponível.")

    print("\n✈️ Agente de viagens iniciado!")
    print("Digite algo como:")
    print('- "planeje um dia de viagem"')
    print('Digite "sair" para encerrar.')

    destino_atual = None

    try:
        while True:
            try:
                user_input = input("\nVocê: ").strip()
            except EOFError:
                print("\nEntrada encerrada. Até mais!")
                break
            except KeyboardInterrupt:
                print("\nOperação interrompida pelo usuário. Até mais!")
                break

            if user_input.lower() in {"sair", "exit", "quit"}:
                print("Encerrando o agente. Até mais!")
                break

            if not user_input:
                continue

            # 1) Se o usuário pedir planejamento inicial
            if quer_planejamento(user_input):
                result = await kernel.invoke(
                    plugin_name="destinations",
                    function_name="get_random_destination",
                )
                destino_atual = str(result)

                if chat_service and history:
                    try:
                        prompt = (
                            f"O usuário quer planejar uma viagem. "
                            f"Sugira o destino '{destino_atual}' como uma surpresa e monte um roteiro de 1 dia "
                            f"nesse local. Organize em manhã, tarde e noite. "
                            f"Se possível, inclua uma sugestão de comida local."
                        )

                        resposta = await gerar_resposta_ia(
                            chat_service=chat_service,
                            history=history,
                            prompt_usuario=prompt,
                        )

                        print("\nAgente:")
                        print(resposta)

                    except Exception as e:
                        imprimir_erro_detalhado(e)

                        if isinstance(e, (APIConnectionError, httpx.HTTPError, OSError)):
                            print(
                                "⚠️ Falha de conexão detectada. "
                                "Desabilitando o modo IA e continuando apenas com o destino local."
                            )
                            chat_service = None
                            history = None

                        print("\n✈️ Destino sugerido:")
                        print(destino_atual)
                        print("💡 A IA deveria montar o roteiro, mas a conexão falhou.")
                else:
                    print("\n✈️ Destino sugerido:")
                    print(destino_atual)
                    print("💡 O roteiro com IA não está disponível no momento.")

                continue

            # 2) Se o usuário não gostar do destino atual
            if quer_outro_destino(user_input):
                result = await kernel.invoke(
                    plugin_name="destinations",
                    function_name="get_random_destination",
                )
                destino_atual = str(result)

                if chat_service and history:
                    try:
                        prompt = (
                            f"O usuário não gostou da sugestão anterior. "
                            f"Sugira um novo destino: '{destino_atual}'. "
                            f"Depois, monte um roteiro de 1 dia nesse local com manhã, tarde e noite."
                        )

                        resposta = await gerar_resposta_ia(
                            chat_service=chat_service,
                            history=history,
                            prompt_usuario=prompt,
                        )

                        print("\nAgente:")
                        print(resposta)

                    except Exception as e:
                        imprimir_erro_detalhado(e)

                        if isinstance(e, (APIConnectionError, httpx.HTTPError, OSError)):
                            print(
                                "⚠️ Falha de conexão detectada. "
                                "Desabilitando o modo IA e continuando apenas com o destino local."
                            )
                            chat_service = None
                            history = None

                        print("\n✈️ Novo destino sugerido:")
                        print(destino_atual)
                else:
                    print("\n✈️ Novo destino sugerido:")
                    print(destino_atual)
                    print("💡 O roteiro com IA não está disponível no momento.")

                continue

            # 3) Se o usuário continuar a conversa sem ter destino atual
            if destino_atual is None:
                print("\nAgente:")
                print(
                    'Peça algo como "planeje um dia de viagem" '
                    "para eu sugerir um destino e montar o roteiro."
                )
                continue

            # 4) Continuação da conversa sobre o destino atual
            if chat_service and history:
                try:
                    prompt = (
                        f"O destino atual da conversa é '{destino_atual}'. "
                        f"Responda ao usuário considerando esse destino. "
                        f"Pergunta do usuário: {user_input}"
                    )

                    resposta = await gerar_resposta_ia(
                        chat_service=chat_service,
                        history=history,
                        prompt_usuario=prompt,
                    )

                    print("\nAgente:")
                    print(resposta)

                except Exception as e:
                    imprimir_erro_detalhado(e)

                    if isinstance(e, (APIConnectionError, httpx.HTTPError, OSError)):
                        print(
                            "⚠️ Falha de conexão detectada. "
                            "Desabilitando o modo IA e continuando apenas com o destino local."
                        )
                        chat_service = None
                        history = None

                    print(f"💡 O destino atual é: {destino_atual}")
            else:
                print("\nAgente:")
                print(
                    f"O destino atual é {destino_atual}. "
                    "Configure a IA para continuar a conversa com roteiro."
                )

    finally:
        if http_client:
            await http_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())

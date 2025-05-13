import tkinter as tk
from tkinter import scrolledtext
import requests
import json

#  CONFIGURAÇÕES

# Chave API do Groq = GROQ_API_KEY = "Chave API aqui"
GROQ_MODEL = "llama3-8b-8192"
BASE_CONHECIMENTO_JSON = "base_conhecimento_unip.json"

#  FUNÇÕES

def carregar_base_conhecimento():
    try:
        with open(BASE_CONHECIMENTO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def gerar_contexto_base_conhecimento():

    cursos = carregar_base_conhecimento()

    if not isinstance(cursos, list) or not cursos:
        return "Erro: a base de conhecimento está vazia."

    contexto = (
        "Você é um agente de suporte da UNIP Tatuapé chamado TatuChat. Responda apenas com base nas informações abaixo "
        "sobre os cursos disponíveis na universidade. Seja direto, objetivo, amigável e utilize emojis.\n\n"
    )

    for curso in cursos:
        contexto += f"- Curso: {curso.get('curso', 'N/A')}\n"
        contexto += f"  • Modalidade: {curso.get('modalidade', 'N/A')}\n"
        contexto += f"  • Duração: {curso.get('duracao', 'N/A')}\n"
        contexto += f"  • Mensalidade: {curso.get('mensalidade', 'N/A')}\n"
        contexto += f"  • Link: {curso.get('link', 'N/A')}\n\n"

    return contexto

def chamar_groq(mensagem_usuario):
    contexto = gerar_contexto_base_conhecimento()

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": contexto},
            {"role": "user", "content": mensagem_usuario}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Erro de requisição: {e}"
    except (KeyError, IndexError):
        return "Erro ao processar a resposta da IA."

#  INTERFACE

def enviar_mensagem():
    mensagem = entrada_usuario.get()
    if mensagem.strip():
        chat_box.insert(tk.END, f"Você: {mensagem}\n")
        entrada_usuario.delete(0, tk.END)
        resposta = chamar_groq(mensagem)
        chat_box.insert(tk.END, f"TatuChat: {resposta}\n\n")
        chat_box.see(tk.END)

def iniciar_interface():
    global entrada_usuario, chat_box

    janela = tk.Tk()
    janela.title("TatuChat")
    janela.geometry("800x600")
    janela.iconbitmap('logoTatuChat.ico')

    fonte_padrao = ("Arial", 12)

    chat_box = scrolledtext.ScrolledText(janela, wrap=tk.WORD, state='normal', font=fonte_padrao)
    chat_box.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

    frame_inferior = tk.Frame(janela)
    frame_inferior.pack(padx=15, pady=5, fill=tk.X)

    entrada_usuario = tk.Entry(frame_inferior, font=fonte_padrao)
    entrada_usuario.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    entrada_usuario.bind("<Return>", lambda event: enviar_mensagem())

    botao_enviar = tk.Button(frame_inferior, text="Enviar", command=enviar_mensagem, font=fonte_padrao)
    botao_enviar.pack(side=tk.RIGHT)

    janela.mainloop()

# EXECUÇÃO DIRETA

iniciar_interface()

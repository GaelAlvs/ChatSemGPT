#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 = Chave API do Groq

import tkinter as tk
from tkinter import scrolledtext
import requests
import json

# =================== CONFIGURAÇÕES ===================

GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-8b-8192"
BASE_CONHECIMENTO_JSON = "base_conhecimento_unip.json"

# =================== FUNÇÕES DE SUPORTE ===================

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
        return "Erro: a base de conhecimento está vazia ou mal formatada."

    contexto = (
        "Você é um agente de suporte da UNIP Tatuapé chamado Chat Sem GPT. Responda apenas com base nas informações abaixo "
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

# =================== INTERFACE GRÁFICA ===================

def enviar_mensagem():
    mensagem = entrada_usuario.get()
    if mensagem.strip():
        chat_box.insert(tk.END, f"Você: {mensagem}\n")
        entrada_usuario.delete(0, tk.END)
        resposta = chamar_groq(mensagem)
        chat_box.insert(tk.END, f"Chat Sem GPT: {resposta}\n\n")
        chat_box.see(tk.END)

def iniciar_interface():
    global entrada_usuario, chat_box

    janela = tk.Tk()
    janela.title("Chat Sem GPT")
    janela.geometry("600x500")

    chat_box = scrolledtext.ScrolledText(janela, wrap=tk.WORD, state='normal')
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entrada_usuario = tk.Entry(janela, width=80)
    entrada_usuario.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.X, expand=True)
    entrada_usuario.bind("<Return>", lambda event: enviar_mensagem())

    botao_enviar = tk.Button(janela, text="Enviar", command=enviar_mensagem)
    botao_enviar.pack(padx=10, pady=5, side=tk.RIGHT)

    janela.mainloop()

# =================== EXECUÇÃO DIRETA ===================

iniciar_interface()

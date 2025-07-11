import tkinter as tk
import numpy as np
import faiss
import pickle
import json
import os
import re
from datetime import datetime
from utils import gerar_embedding
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Carregue seus dados aqui (FAISS, metadados, etc)
index = faiss.read_index("chatquimica_index.faiss")
with open("metadados.pkl", "rb") as f:
    metadados = pickle.load(f)


print("✅ ValQ iniciado! (Digite 'sair' para encerrar)\n")

# Loop do chat (exemplo mínimo)
while True:
    pergunta = input("Você: ").strip()
    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("👋 Encerrando ValQ. Até mais!")
        break

    # Sua lógica de resposta aqui, por exemplo:
    emb_pergunta = gerar_embedding(pergunta)
    D, I = index.search(np.array([emb_pergunta]).astype("float32"), k=3)

    contexto = "\n\n".join(
        metadados[i]["conteudo"] if isinstance(metadados[i], dict) else str(metadados[i])
        for i in I[0]
    )

    prompt = f"""Você é um assistente químico. Responda com base nas seguintes informações:
{contexto}

Pergunta: {pergunta}
Resposta:"""

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

    print(f"\n🤖 {resposta}")

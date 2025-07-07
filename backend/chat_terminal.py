import numpy as np
import faiss
import pickle
from utils import gerar_embedding
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Carrega banco vetorial
index = faiss.read_index("chatquimica_index.faiss")
with open("metadados.pkl", "rb") as f:
    metadados = pickle.load(f)

print("🤖 Chat Químico iniciado (digite 'sair' para encerrar)\n")

while True:
    pergunta = input("Você: ")
    if pergunta.lower() in ["sair", "exit", "quit"]:
        break

    emb_pergunta = gerar_embedding(pergunta)
    D, I = index.search(np.array([emb_pergunta]).astype("float32"), k=3)

    contexto = "\n\n".join([metadados[i] for i in I[0]])

    prompt = f"""Você é um assistente químico. Responda com base nestas informações:
{contexto}

Pergunta: {pergunta}
Resposta:"""

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

    print(f"\n🤖 {resposta}\n")

import fitz  # PyMuPDF
import tiktoken
from openai import OpenAI
import os
from dotenv import load_dotenv
from docx import Document
from bs4 import BeautifulSoup

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extrair_texto_txt(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler TXT: {caminho} -> {e}")
        return ""

def extrair_texto_html(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        print(f"Erro ao ler HTML: {caminho} -> {e}")
        return ""

def extrair_texto_docx(caminho):
    try:
        doc = Document(caminho)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        print(f"Erro ao ler DOCX: {caminho} -> {e}")
        return ""

def extrair_texto_pdf(path):
    try:
        doc = fitz.open(path)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        return texto.strip()
    except Exception as e:
        print(f"Erro ao ler PDF: {path} -> {e}")
        return ""

def dividir_em_chunks(texto, max_tokens=300):
    tokens = texto.split()
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = " ".join(tokens[i:i+max_tokens])
        chunks.append(chunk.strip())
    return chunks

def gerar_embedding(texto):
    if not texto.strip():
        return [0.0] * 1536  # Retorna vetor nulo se o texto estiver vazio (1536 é o tamanho do modelo usado)
    
    try:
        response = client.embeddings.create(
            input=texto,
            model="text-embedding-3-small"  # mais barato e eficiente
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Erro ao gerar embedding: {e}")
        return [0.0] * 1536

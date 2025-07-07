import fitz  # PyMuPDF
import tiktoken
from openai import OpenAI
import os
from dotenv import load_dotenv
from docx import Document
from bs4 import BeautifulSoup

def extrair_texto_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()
    
def extrair_texto_html(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    return soup.get_text()


def extrair_texto_docx(caminho):
    doc = Document(caminho)
    return "\n".join([p.text for p in doc.paragraphs])

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extrair_texto_pdf(path):
    doc = fitz.open(path)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

def dividir_em_chunks(texto, max_tokens=300):
    tokens = texto.split()
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = " ".join(tokens[i:i+max_tokens])
        chunks.append(chunk)
    return chunks

def gerar_embedding(texto):
    response = client.embeddings.create(
        input=texto,
        model="text-embedding-3-small"  # mais barato e eficiente
    )
    return response.data[0].embedding

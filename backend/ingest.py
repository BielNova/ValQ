import os
import numpy as np
import faiss
import pickle
from utils import (
    extrair_texto_pdf,
    extrair_texto_docx,
    extrair_texto_html,
    extrair_texto_txt,
    dividir_em_chunks,
    gerar_embedding
)

vetores = []
metadados = []

pasta_pdfs = "pdfs"

# Filtra somente arquivos suportados
todos_arquivos = [f for f in os.listdir(pasta_pdfs)
                  if f.lower().split('.')[-1] in ["pdf", "docx", "html", "htm", "txt"]]

total = len(todos_arquivos)
print(f"🔎 Encontrados {total} arquivos válidos na pasta '{pasta_pdfs}'...\n")

for idx, arquivo in enumerate(todos_arquivos, start=1):
    ext = arquivo.lower().split('.')[-1]
    caminho = os.path.join(pasta_pdfs, arquivo)

    print(f"[{idx}/{total}] 📂 Processando: {arquivo}")

    if ext == "pdf":
        texto = extrair_texto_pdf(caminho)
    elif ext == "docx":
        texto = extrair_texto_docx(caminho)
    elif ext in ["html", "htm"]:
        texto = extrair_texto_html(caminho)
    elif ext == "txt":
        texto = extrair_texto_txt(caminho)
    else:
        print(f"❌ Tipo de arquivo não suportado: {arquivo}")
        continue

    chunks = dividir_em_chunks(texto)

    for chunk in chunks:
        emb = gerar_embedding(chunk)
        vetores.append(emb)
        metadados.append(chunk)

if not vetores:
    print("⚠️ Nenhum vetor foi gerado. Verifique os arquivos na pasta.")
    exit()

print(f"\n✅ Total de chunks gerados: {len(vetores)}")

# Cria e salva banco vetorial
dim = len(vetores[0])
index = faiss.IndexFlatL2(dim)
index.add(np.array(vetores).astype("float32"))

faiss.write_index(index, "chatquimica_index.faiss")
with open("metadados.pkl", "wb") as f:
    pickle.dump(metadados, f)

print("✅ Tudo pronto! Base vetorial salva com sucesso.")

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
arquivos = [f for f in os.listdir(pasta_pdfs)
            if f.lower().split('.')[-1] in ["pdf", "docx", "html", "htm", "txt"]]

print(f"🔎 Encontrados {len(arquivos)} arquivos na pasta '{pasta_pdfs}'...\n")

for idx, arquivo in enumerate(arquivos, 1):
    caminho = os.path.join(pasta_pdfs, arquivo)
    ext = arquivo.lower().split('.')[-1]

    print(f"[{idx}/{len(arquivos)}] 📂 Processando: {arquivo}")

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

    # Caso especial: tratar o arquivo de clientes
    if arquivo.lower() == "clientes.txt":
        blocos = texto.split("\n\n")
        print(f"🔎 Arquivo 'clientes.txt' detectado com {len(blocos)} blocos...\n")

        for i, bloco in enumerate(blocos, 1):
            if not bloco.strip():
                continue

            primeira_linha = bloco.strip().splitlines()[0]
            if "*" in primeira_linha:
                nome_cliente = primeira_linha.strip("* ").strip()
            else:
                nome_cliente = f"Cliente {i}"

            chunks = dividir_em_chunks(bloco)
            for chunk in chunks:
                emb = gerar_embedding(chunk)
                vetores.append(emb)
                metadados.append({
                    "nome_cliente": nome_cliente,
                    "conteudo": chunk
                })
    else:
        # Documento comum (sem relação com cliente)
        chunks = dividir_em_chunks(texto)
        for chunk in chunks:
            emb = gerar_embedding(chunk)
            vetores.append(emb)
            metadados.append(chunk)

if not vetores:
    print("⚠️ Nenhum vetor foi gerado. Verifique os arquivos.")
    exit()

print(f"\n✅ Total de chunks gerados: {len(vetores)}")

# Criação do índice vetorial
dim = len(vetores[0])
index = faiss.IndexFlatL2(dim)
index.add(np.array(vetores).astype("float32"))

faiss.write_index(index, "chatquimica_index.faiss")
with open("metadados.pkl", "wb") as f:
    pickle.dump(metadados, f)

# Mostrar nomes únicos se houver clientes
nomes = {d['nome_cliente'] for d in metadados if isinstance(d, dict) and 'nome_cliente' in d}
if nomes:
    print("\n🧪 Nomes únicos extraídos dos metadados:")
    for nome in sorted(nomes):
        print(f"- {nome}")

print("\n✅ Tudo pronto! Base vetorial salva com sucesso.")

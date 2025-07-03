import os
from pathlib import Path

# Caminho da pasta com seus documentos
root_folder = Path("docs_teste")  # ou Path("C:/Users/Leonardo/valenca_ai/docs_teste")

# Extensões que serão mantidas
allowed_extensions = {'.pdf', '.docx', '.txt'}

# Contador
removed_files = 0

# Percorrer e remover arquivos não permitidos
for path in root_folder.rglob("*"):
    if path.is_file() and path.suffix.lower() not in allowed_extensions:
        try:
            path.unlink()
            print(f"[REMOVIDO] {path}")
            removed_files += 1
        except Exception as e:
            print(f"[ERRO] Não foi possível remover {path}: {e}")

print(f"\nTotal de arquivos removidos: {removed_files}")

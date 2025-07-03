import os
import sys
from pathlib import Path
from rich import print
from langchain_community.vectorstores import FAISS
from langchain_unstructured import UnstructuredLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains.question_answering import load_qa_chain
import pickle

def load_or_create_vector_store(folder_path: str, index_path: str):
    index_path = Path(index_path)
    if index_path.exists() and (index_path / "faiss_store.pkl").exists():
        print("[bold yellow]Carregando índice FAISS existente...[/bold yellow]")
        with open(index_path / "faiss_store.pkl", "rb") as f:
            db = pickle.load(f)
        db.index = FAISS.load_local(index_path, OpenAIEmbeddings()).index
    else:
        print("[bold green]Criando novo índice FAISS...[/bold green]")
        all_docs = []
        for file_path in Path(folder_path).glob("*.*"):
            loader = UnstructuredLoader(str(file_path))
            docs = loader.load()
            all_docs.extend(docs)

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(all_docs)

        db = FAISS.from_documents(docs, OpenAIEmbeddings())
        index_path.mkdir(parents=True, exist_ok=True)
        db.save_local(index_path)
        with open(index_path / "faiss_store.pkl", "wb") as f:
            pickle.dump(db, f)
    return db

def run_qa(folder_path: str):
    index_path = "faiss_index"
    db = load_or_create_vector_store(folder_path, index_path)

    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")

    print("\n[bold cyan]ValQ - IA Corporativa Valença Química[/bold cyan]")
    print("[green]Digite sua pergunta (ou 'sair' para encerrar):[/green]")

    while True:
        query = input("\n🧠 Pergunta: ")
        if query.lower() in ("sair", "exit", "quit"):
            print("[red]Encerrando...[/red]")
            break

        docs = db.similarity_search(query)
        answer = chain.run(input_documents=docs, question=query)
        print(f"\n[bold green]Resposta:[/bold green] {answer}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[red]Uso: python main.py <pasta_com_arquivos>[/red]")
    else:
        run_qa(sys.argv[1])

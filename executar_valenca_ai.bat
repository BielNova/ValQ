@echo off
REM Define a variável de ambiente com sua chave da OpenAI
set OPENAI_API_KEY=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

REM Navega até a pasta do projeto
cd /d %~dp0

REM Executa o script passando o nome da pasta de documentos
python main.py docs_teste

pause

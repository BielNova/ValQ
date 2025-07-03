@echo off
title ValQ - IA da Valen�a Qu�mica

echo ============================================
echo        ValQ - IA da Valen�a Qu�mica
echo ============================================
echo.
echo Informe o nome da pasta com os documentos
echo (ex: docs_teste) e pressione Enter:
set /p folder="Pasta: "

if "%folder%"=="" (
    echo Nenhuma pasta informada. Encerrando...
    pause
    exit
)

echo.
echo Iniciando ValQ com a pasta "%folder%"...
echo --------------------------------------------
cd /d "%~dp0"
powershell -NoExit -Command "python main.py %folder%"

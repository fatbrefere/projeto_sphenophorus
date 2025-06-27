@echo off
cd /d "C:\Users\fatbr\OneDrive\Documents\GitHub\projeto_sphenophorus"

echo ================================================
echo Atualizando projeto no GitHub...
echo ================================================

git status

echo.
echo Adicionando arquivos alterados...
git add .

echo.
set /p mensagem=Digite a mensagem do commit: 
git commit -m "%mensagem%"

echo.
echo Enviando para o repositório remoto...
git push origin main

echo.
echo ✅ Projeto atualizado com sucesso!
pause

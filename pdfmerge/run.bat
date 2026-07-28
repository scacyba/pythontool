@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo 仮想環境がありません。最初に setup_and_run.bat を実行してください。
  pause
  exit /b 1
)
.venv\Scripts\python.exe merge.py

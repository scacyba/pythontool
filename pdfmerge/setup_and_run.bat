@echo off
setlocal
cd /d "%~dp0"

py -3 -m venv .venv
if errorlevel 1 goto :error

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

python merge.py
goto :end

:error
echo.
echo セットアップまたは実行に失敗しました。
pause
exit /b 1

:end
endlocal

@echo off
cd /d "%~dp0"
if not exist .env (
  echo Missing .env file. Copy .env.example to .env and add Telegram settings.
  pause
  exit /b 1
)
for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do set "%%A=%%B"
python server.py
pause

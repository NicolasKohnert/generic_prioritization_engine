@echo off
cd /d "%~dp0"

echo start Data Pipeline...
python main.py

echo Pipeline ready. start Web-Server...
start http://localhost:8000
python -m http.server 8000
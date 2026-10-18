@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
 echo Python introuvable. Installer Python 3.10+ depuis https://www.python.org/downloads/windows/
 pause
 exit /b 1
)
py -3 -m venv .venv
if errorlevel 1 goto erreur
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto erreur
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto erreur
echo Installation terminee. Adapter config.ini puis lancer Exporter.cmd.
pause
exit /b 0
:erreur
echo Echec de l'installation.
pause
exit /b 1

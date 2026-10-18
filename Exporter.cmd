@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Installation absente : lancer Installer.cmd.
 pause
 exit /b 1
)
".venv\Scripts\python.exe" export_index_chaufferie.py %*
set "RC=%ERRORLEVEL%"
echo.
pause
exit /b %RC%

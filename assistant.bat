@echo off
title Winky Assistant Control
echo =========================================
echo       STARTING WINKY VOICE ASSISTANT
echo =========================================
echo.

:: Get the directory of the batch script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%agent-starter-react"

:: Check if port 3000 is active and listening
netstat -ano | findstr /R /C:":3000 " | findstr LISTENING >nul
if %errorlevel% equ 0 (
    echo [+] Port 3000 is already active. Winky web server is likely already running.
) else (
    echo [+] Starting backend and frontend dev servers...
    :: Start in a new command prompt window so they can see logs and stop it easily
    start "Winky Server Logs" cmd /k "pnpm.cmd dev"
    
    echo [+] Waiting 5 seconds for servers to initialize...
    timeout /t 5 /nobreak >nul
)

echo.
echo [+] Opening WinkyTalk at http://localhost:3000...
start http://localhost:3000
echo.
echo =========================================
echo Winky is ready! You can minimize this window.
echo =========================================
timeout /t 3 >nul

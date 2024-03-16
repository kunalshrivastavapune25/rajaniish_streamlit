@echo off
:loop
tasklist | findstr "python" > nul
if errorlevel 1 (
    echo No Python processes found.
    goto :eof
) else (
    echo Python processes found. Killing them...
    taskkill /f /im python.exe > nul
)
timeout /t 5 /nobreak > nul
goto loop

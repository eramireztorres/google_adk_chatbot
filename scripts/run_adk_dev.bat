@echo off
REM Batch script to run ADK development environment on Windows
REM Usage: scripts\run_adk_dev.bat

setlocal enabledelayedexpansion

REM Get script directory and root directory
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
cd /d "%ROOT_DIR%"

set "CHATBOT_DIR=%ROOT_DIR%\chatbot"
set "AGENT_DIR=%CHATBOT_DIR%\ADK_assistant"
set "ENV_SRC=%ROOT_DIR%\.env"
set "ENV_DEST=%AGENT_DIR%\.env"

REM Copy .env file if it exists
if exist "%ENV_SRC%" (
    copy /Y "%ENV_SRC%" "%ENV_DEST%" >nul
    REM Load environment variables from .env
    for /f "usebackq tokens=1,* delims==" %%a in ("%ENV_SRC%") do (
        set "line=%%a"
        if not "!line:~0,1!"=="#" (
            set "%%a=%%b"
        )
    )
) else (
    echo Warning: .env file not found at %ENV_SRC%. Continuing without it.
)

REM Set default ports if not defined
if not defined MCP_PORT set "MCP_PORT=8001"
if not defined ADK_WEB_PORT set "ADK_WEB_PORT=8000"
if not defined ADK_LOG_LEVEL set "ADK_LOG_LEVEL=INFO"

echo ================================================
echo Starting ADK Development Environment
echo ================================================
echo MCP Server Port: %MCP_PORT%
echo ADK Web Port: %ADK_WEB_PORT%
echo ================================================
echo.

REM Start MCP server in background
echo Starting MCP server on port %MCP_PORT%...
start "MCP Server" /B python "%ROOT_DIR%\rag\run_adk_mcp_server.py" --port %MCP_PORT%

REM Wait for MCP server to start
timeout /t 2 /nobreak >nul

REM Start ADK web interface (foreground)
echo Starting ADK web interface on port %ADK_WEB_PORT%...
cd /d "%CHATBOT_DIR%"
adk web --log_level %ADK_LOG_LEVEL% --port %ADK_WEB_PORT% .

REM Note: When adk web exits, the MCP server will continue running
REM User needs to manually close it or use Task Manager
echo.
echo ADK web interface stopped. MCP server may still be running.
echo Use Task Manager to stop python processes if needed.

endlocal

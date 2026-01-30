# PowerShell script to run ADK development environment on Windows
# Usage: .\scripts\run_adk_dev.ps1

$ErrorActionPreference = "Stop"

$ROOT_DIR = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$CHATBOT_DIR = Join-Path $ROOT_DIR "chatbot"
$AGENT_DIR = Join-Path $CHATBOT_DIR "ADK_assistant"
$ENV_SRC = Join-Path $ROOT_DIR ".env"
$ENV_DEST = Join-Path $AGENT_DIR ".env"

# Copy .env file if it exists
if (Test-Path $ENV_SRC) {
    Copy-Item $ENV_SRC $ENV_DEST -Force
    # Load environment variables from .env
    Get-Content $ENV_SRC | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
} else {
    Write-Warning ".env file not found at $ENV_SRC. Continuing without it."
}

# Set default ports
$MCP_PORT = if ($env:MCP_PORT) { $env:MCP_PORT } else { "8001" }
$ADK_WEB_PORT = if ($env:ADK_WEB_PORT) { $env:ADK_WEB_PORT } else { "8000" }
$ADK_LOG_LEVEL = if ($env:ADK_LOG_LEVEL) { $env:ADK_LOG_LEVEL } else { "INFO" }

Write-Host "Starting ADK Development Environment" -ForegroundColor Green
Write-Host "MCP Server Port: $MCP_PORT"
Write-Host "ADK Web Port: $ADK_WEB_PORT"
Write-Host ""

# Start MCP server in background
$mcpScript = Join-Path $ROOT_DIR "rag\run_adk_mcp_server.py"
Write-Host "Starting MCP server on port $MCP_PORT..." -ForegroundColor Cyan
$mcpProcess = Start-Process -FilePath "python" -ArgumentList "$mcpScript --port $MCP_PORT" -PassThru -NoNewWindow

# Cleanup function
$cleanup = {
    param($process)
    if ($process -and !$process.HasExited) {
        Write-Host "`nStopping MCP server..." -ForegroundColor Yellow
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    }
}

# Register cleanup on script exit
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action {
    & $cleanup $mcpProcess
} | Out-Null

try {
    # Give MCP server time to start
    Start-Sleep -Seconds 2

    # Start ADK web interface
    Write-Host "Starting ADK web interface on port $ADK_WEB_PORT..." -ForegroundColor Cyan
    Set-Location $CHATBOT_DIR
    adk web --log_level $ADK_LOG_LEVEL --port $ADK_WEB_PORT .
} finally {
    # Cleanup MCP server
    & $cleanup $mcpProcess
}

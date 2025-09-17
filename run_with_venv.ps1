# Run GPS Area Tracking System with Virtual Environment (PowerShell)
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚗 GPS Area Tracking System - Run with Virtual Environment" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Yellow
    & ".\setup_venv.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Setup failed" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
try {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting GPS Area Tracking System..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Server will be available at: http://localhost:17890" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:17890/docs" -ForegroundColor Cyan
Write-Host "🗺️  Map Interface: http://localhost:17890" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

try {
    python run.py
} catch {
    Write-Host "❌ Error running the system: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "👋 System stopped" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
}

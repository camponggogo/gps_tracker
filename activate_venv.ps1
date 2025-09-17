# Activate Virtual Environment (PowerShell)
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🐍 Activating Virtual Environment" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run .\setup_venv.ps1 first" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
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
Write-Host "📋 You can now run:" -ForegroundColor Cyan
Write-Host "   python run.py" -ForegroundColor White
Write-Host "   python test_system.py" -ForegroundColor White
Write-Host "   python simulator/start_simulator.py" -ForegroundColor White
Write-Host ""
Write-Host "💡 To deactivate, type: deactivate" -ForegroundColor Yellow
Write-Host ""

# Keep PowerShell open
Write-Host "Press Ctrl+C to exit or type 'deactivate' to deactivate venv" -ForegroundColor Gray
Write-Host ""

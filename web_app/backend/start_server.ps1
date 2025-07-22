# Script para iniciar el servidor UltraEfficientLLM
# Maneja el cierre de procesos automáticamente

Write-Host "🔧 Iniciando UltraEfficientLLM Web API..." -ForegroundColor Green

# Matar cualquier proceso Python que esté usando el puerto 8001 o 8001
Write-Host "🛑 Limpiando procesos anteriores..." -ForegroundColor Yellow

# Buscar y matar procesos Python
$pythonProcesses = Get-Process | Where-Object {$_.ProcessName -eq "python"}
if ($pythonProcesses) {
    Write-Host "📋 Encontrados $($pythonProcesses.Count) procesos Python" -ForegroundColor Yellow
    $pythonProcesses | Stop-Process -Force
    Write-Host "✅ Procesos Python terminados" -ForegroundColor Green
}

# Esperar un momento para que los puertos se liberen
Start-Sleep -Seconds 2

# Verificar que los puertos estén libres
$port8001 = netstat -ano | findstr :8001
$port8001 = netstat -ano | findstr :8001

if ($port8001 -or $port8001) {
    Write-Host "⚠️ Los puertos aún están ocupados. Intentando liberar..." -ForegroundColor Red
    
    # Matar procesos por PID específico
    if ($port8001) {
        $pid8001 = ($port8001 -split '\s+')[-1]
        taskkill /F /PID $pid8001 2>$null
        Write-Host "🔄 Puerto 8001 liberado" -ForegroundColor Yellow
    }
    
    if ($port8001) {
        $pid8001 = ($port8001 -split '\s+')[-1]
        taskkill /F /PID $pid8001 2>$null
        Write-Host "🔄 Puerto 8001 liberado" -ForegroundColor Yellow
    }
    
    Start-Sleep -Seconds 2
}

Write-Host "🚀 Iniciando servidor en puerto 8001..." -ForegroundColor Green
Write-Host "📍 Backend: http://localhost:8001" -ForegroundColor Cyan
Write-Host "📚 Documentación: http://localhost:8001/api/docs" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Iniciar el servidor
try {
    python simple_main.py
} catch {
    Write-Host "❌ Error iniciando el servidor: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} 
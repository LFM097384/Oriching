# 简化版启动脚本 - 保证可以正常启动前后端

Write-Host "🔮 Oriching - 纳甲六爻排盘系统启动" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 检查目录
if (-not (Test-Path "najia") -or -not (Test-Path "frontend")) {
    Write-Host "❌ 错误: 请在项目根目录运行此脚本" -ForegroundColor Red
    exit 1
}

# 启动后端服务
Write-Host ""
Write-Host "🚀 启动后端服务..." -ForegroundColor Green
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd '$PWD\najia'; python start_server.py"

# 等待2秒
Start-Sleep -Seconds 2

# 启动前端服务
Write-Host "🌐 启动前端服务..." -ForegroundColor Green
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Write-Host ""
Write-Host "✅ 服务启动命令已执行!" -ForegroundColor Green
Write-Host "📱 前端地址: http://localhost:5173" -ForegroundColor Cyan
Write-Host "⚙️  后端地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📖 API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 两个新的PowerShell窗口将打开来运行服务" -ForegroundColor Yellow
Write-Host "💡 关闭那些窗口来停止对应的服务" -ForegroundColor Yellow

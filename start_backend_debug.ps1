# 后端调试启动脚本
# 设置编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $scriptPath "backend"

Write-Host "=== 易经占卜后端调试启动 ===" -ForegroundColor Yellow
Write-Host "后端路径: $backendPath" -ForegroundColor Gray

# 切换到后端目录
Set-Location $backendPath

# 检查 conda 环境
Write-Host "检查 Conda 环境..." -ForegroundColor Cyan
$envExists = conda env list | Select-String "oriching"
if (-not $envExists) {
    Write-Host "错误：未找到 Conda 环境 'oriching'" -ForegroundColor Red
    Write-Host "请先运行 start_conda.ps1 创建环境" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit
}

Write-Host "找到 Conda 环境 'oriching'" -ForegroundColor Green

# 检查依赖
Write-Host "检查 Python 包..." -ForegroundColor Cyan
conda run -n oriching pip list | Select-String -Pattern "fastapi|uvicorn"

Write-Host "`n=== 启动后端服务 ===" -ForegroundColor Yellow
Write-Host "启动地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Blue
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Yellow

# 启动服务，显示详细日志
try {
    conda run -n oriching python main.py
} catch {
    Write-Host "`n错误：后端启动失败" -ForegroundColor Red
    Write-Host "错误详情: $_" -ForegroundColor Red
}

Write-Host "`n后端服务已停止" -ForegroundColor Yellow
Read-Host "按任意键关闭窗口"

# 激活 Oriching Conda 环境的脚本
Write-Host "激活 Oriching Conda 环境..." -ForegroundColor Yellow

# 初始化 conda (如果需要)
try {
    conda activate oriching 2>$null
} catch {
    Write-Host "正在初始化 conda..." -ForegroundColor Yellow
    conda init powershell
    Write-Host "请重新启动 PowerShell 后再运行此脚本" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit
}

Write-Host "Conda 环境 'oriching' 已激活" -ForegroundColor Green
Write-Host "你现在可以运行以下命令：" -ForegroundColor Cyan
Write-Host "  cd backend" -ForegroundColor Gray
Write-Host "  python main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "或者直接运行完整启动脚本：" -ForegroundColor Cyan
Write-Host "  .\start_conda.ps1" -ForegroundColor Gray

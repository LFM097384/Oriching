# 占卜网站启动脚本
Write-Host "占卜网站启动程序" -ForegroundColor Yellow

# 获取脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $scriptPath "backend"
$frontendPath = Join-Path $scriptPath "frontend"

Write-Host "后端路径: $backendPath"
Write-Host "前端路径: $frontendPath"

# 检查目录
if (!(Test-Path $backendPath)) {
    Write-Host "错误：后端目录不存在" -ForegroundColor Red
    exit
}

if (!(Test-Path $frontendPath)) {
    Write-Host "错误：前端目录不存在" -ForegroundColor Red
    exit
}

# 安装后端依赖
Write-Host "安装后端依赖..." -ForegroundColor Yellow
Set-Location $backendPath
pip install -r requirements.txt

# 安装前端依赖
Write-Host "安装前端依赖..." -ForegroundColor Yellow
Set-Location $frontendPath
if (!(Test-Path "node_modules")) {
    npm install
}

# 启动服务
Write-Host "启动后端服务..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; python main.py"

Start-Sleep -Seconds 3

Write-Host "启动前端服务..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; npm run dev"

Write-Host "启动完成！" -ForegroundColor Green
Write-Host "前端: http://localhost:5173" -ForegroundColor Cyan
Write-Host "后端: http://localhost:8000" -ForegroundColor Cyan

Read-Host "按任意键退出"

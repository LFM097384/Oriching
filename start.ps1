# 占卜网站启动脚本
# 设置编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取脚本所在目录作为项目根目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptPath

Write-Host "占卜网站启动程序" -ForegroundColor Yellow
Write-Host "项目根目录: $projectRoot" -ForegroundColor Gray

# 设置路径变量
$backendPath = Join-Path $projectRoot "backend"
$frontendPath = Join-Path $projectRoot "frontend"

Write-Host "后端路径: $backendPath" -ForegroundColor Gray
Write-Host "前端路径: $frontendPath" -ForegroundColor Gray

# 检查路径是否存在
if (-not (Test-Path $backendPath)) {
    Write-Host "错误：后端目录不存在: $backendPath" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit
}

if (-not (Test-Path $frontendPath)) {
    Write-Host "错误：前端目录不存在: $frontendPath" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit
}

# 检查并安装后端依赖
Push-Location $backendPath

Write-Host "检查后端依赖..." -ForegroundColor Yellow

# 检查 requirements.txt 是否存在
if (-not (Test-Path "requirements.txt")) {
    Write-Host "错误：未找到 requirements.txt 文件" -ForegroundColor Red
    Pop-Location
    Read-Host "按任意键退出"
    exit
}

# 尝试安装依赖
Write-Host "正在安装后端依赖..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "依赖安装失败，请检查网络连接或手动运行: pip install -r requirements.txt" -ForegroundColor Red
    Pop-Location
    Read-Host "按任意键退出"
    exit
}
Write-Host "后端依赖安装完成" -ForegroundColor Green

Pop-Location

# 检查前端依赖
Push-Location $frontendPath

Write-Host "检查前端依赖..." -ForegroundColor Yellow

if (-not (Test-Path "node_modules")) {
    Write-Host "正在安装前端依赖..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "前端依赖安装失败" -ForegroundColor Red
        Pop-Location
        Read-Host "按任意键退出"
        exit
    }
    Write-Host "前端依赖安装完成" -ForegroundColor Green
} 
else {
    Write-Host "前端依赖检查完成" -ForegroundColor Green
}

Pop-Location

Write-Host "正在启动服务..." -ForegroundColor Yellow

# 启动后端服务
Write-Host "启动后端服务 (端口 8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; python main.py"

# 等待2秒
Start-Sleep -Seconds 2

# 启动前端服务
Write-Host "启动前端服务 (端口 5173)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; npm run dev"

Write-Host "系统启动完成！" -ForegroundColor Green
Write-Host "前端地址: http://localhost:5173" -ForegroundColor Cyan
Write-Host "后端地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Blue

Read-Host "按任意键退出"

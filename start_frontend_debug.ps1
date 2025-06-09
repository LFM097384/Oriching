# 前端调试启动脚本
# 设置编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $scriptPath "frontend"

Write-Host "=== 易经占卜前端调试启动 ===" -ForegroundColor Yellow
Write-Host "前端路径: $frontendPath" -ForegroundColor Gray

# 检查 Node.js
$nodeExe = $null
$npmExe = $null

if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeExe = "node"
    $npmExe = "npm"
    Write-Host "从 PATH 中找到 Node.js" -ForegroundColor Green
} else {
    # 查找常见安装位置
    $commonPaths = @(
        "$env:ProgramFiles\nodejs",
        "$env:PROGRAMFILES(X86)\nodejs",
        "$env:LOCALAPPDATA\Programs\nodejs"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path "$path\node.exe") {
            $nodeExe = "$path\node.exe"
            $npmExe = "$path\npm.cmd"
            $env:PATH += ";$path"
            Write-Host "在 $path 找到 Node.js" -ForegroundColor Yellow
            break
        }
    }
}

if (-not ($nodeExe -and $npmExe)) {
    Write-Host "错误：未找到 Node.js" -ForegroundColor Red
    Write-Host "请从 https://nodejs.org 下载并安装 Node.js" -ForegroundColor Cyan
    Read-Host "按任意键退出"
    exit
}

# 显示版本信息
$nodeVersion = & $nodeExe --version
$npmVersion = & $npmExe --version
Write-Host "Node.js 版本: $nodeVersion" -ForegroundColor Green
Write-Host "npm 版本: $npmVersion" -ForegroundColor Green

# 切换到前端目录
Set-Location $frontendPath

# 检查依赖
if (-not (Test-Path "node_modules")) {
    Write-Host "未找到 node_modules，正在安装依赖..." -ForegroundColor Yellow
    & $npmExe install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "依赖安装失败" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit
    }
} else {
    Write-Host "依赖检查完成" -ForegroundColor Green
}

Write-Host "`n=== 启动前端开发服务器 ===" -ForegroundColor Yellow
Write-Host "启动地址: http://localhost:5173" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Yellow

# 启动前端开发服务器
try {
    & $npmExe run dev
} catch {
    Write-Host "`n错误：前端启动失败" -ForegroundColor Red
    Write-Host "错误详情: $_" -ForegroundColor Red
}

Write-Host "`n前端服务已停止" -ForegroundColor Yellow
Read-Host "按任意键关闭窗口"

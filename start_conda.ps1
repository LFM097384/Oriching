# 占卜网站启动脚本 (使用 Conda 环境)
# 设置编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取脚本所在目录作为项目根目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptPath

Write-Host "占卜网站启动程序 (Conda 环境)" -ForegroundColor Yellow
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

# 检查 conda 是否可用
try {
    $condaVersion = conda --version
    Write-Host "检测到 Conda: $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "错误：未找到 Conda，请先安装 Anaconda 或 Miniconda" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit
}

# 检查 Node.js 和 npm 是否可用
$nodeExe = $null
$npmExe = $null
$nodejsPath = $null

# 首先尝试从 PATH 中查找
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeExe = "node"
    $npmExe = "npm"
    Write-Host "从 PATH 中找到 Node.js" -ForegroundColor Green
} else {
    # 如果 PATH 中没有，尝试常见安装位置
    $commonPaths = @(
        "$env:ProgramFiles\nodejs",
        "$env:PROGRAMFILES(X86)\nodejs",
        "$env:LOCALAPPDATA\Programs\nodejs"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path "$path\node.exe") {
            $nodeExe = "$path\node.exe"
            $npmExe = "$path\npm.cmd"
            $nodejsPath = $path
            Write-Host "在 $path 找到 Node.js" -ForegroundColor Yellow
            Write-Host "正在将 Node.js 添加到当前会话的 PATH..." -ForegroundColor Yellow
            # 将 Node.js 路径添加到当前会话的 PATH
            $env:PATH += ";$path"
            break
        }
    }
}

if ($nodeExe -and $npmExe) {
    try {
        $nodeVersion = & $nodeExe --version
        $npmVersion = & $npmExe --version
        Write-Host "检测到 Node.js: $nodeVersion" -ForegroundColor Green
        Write-Host "检测到 npm: $npmVersion" -ForegroundColor Green
    } catch {
        Write-Host "错误：Node.js 或 npm 执行失败" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit
    }
} else {
    Write-Host "错误：未找到 Node.js 或 npm" -ForegroundColor Red
    Write-Host "下载地址: https://nodejs.org/" -ForegroundColor Cyan
    Write-Host "安装后请重启 PowerShell 或重新打开命令提示符" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit
}

# 检查 oriching 环境是否存在
$envExists = conda env list | Select-String "oriching"
if (-not $envExists) {
    Write-Host "正在创建 Conda 环境 'oriching'..." -ForegroundColor Yellow
    conda create -n oriching python=3.11 -y
    if ($LASTEXITCODE -ne 0) {
        Write-Host "创建 Conda 环境失败" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit
    }
    Write-Host "Conda 环境创建完成" -ForegroundColor Green
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

# 在 conda 环境中安装依赖
Write-Host "正在在 Conda 环境中安装后端依赖..." -ForegroundColor Yellow
conda run -n oriching pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "依赖安装失败，请检查网络连接或手动运行: conda run -n oriching pip install -r requirements.txt" -ForegroundColor Red
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
    try {
        & $npmExe install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "前端依赖安装失败" -ForegroundColor Red
            Pop-Location
            Read-Host "按任意键退出"
            exit
        }
        Write-Host "前端依赖安装完成" -ForegroundColor Green
    } catch {
        Write-Host "错误：npm 命令执行失败，请确保 Node.js 已正确安装" -ForegroundColor Red
        Write-Host "如果刚安装了 Node.js，请重启 PowerShell 后再试" -ForegroundColor Yellow
        Pop-Location
        Read-Host "按任意键退出"
        exit
    }
}
else {
    Write-Host "前端依赖检查完成" -ForegroundColor Green
}

Pop-Location

Write-Host "正在启动服务..." -ForegroundColor Yellow

# 启动后端服务 (使用 conda 环境)
Write-Host "启动后端服务 (端口 8000) - 使用 Conda 环境..." -ForegroundColor Green
$backendCmd = @"
Set-Location '$backendPath'
Write-Host '=== 后端服务启动日志 ===' -ForegroundColor Yellow
Write-Host '当前目录:' (Get-Location) -ForegroundColor Gray
Write-Host '激活 Conda 环境并启动服务...' -ForegroundColor Gray
conda run -n oriching python main.py
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

# 等待2秒
Start-Sleep -Seconds 2

# 启动前端服务
Write-Host "启动前端服务 (端口 5173)..." -ForegroundColor Green
if ($nodejsPath) {
    # 如果找到了 Node.js 路径但不在原始 PATH 中，需要在新进程中设置环境变量
    $frontendCmd = "Set-Location '$frontendPath'; `$env:PATH += ';$nodejsPath'; & '$npmExe' run dev"
} else {
    # 如果 Node.js 在 PATH 中，直接使用
    $frontendCmd = "Set-Location '$frontendPath'; & '$npmExe' run dev"
}
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-Host "系统启动完成！" -ForegroundColor Green
Write-Host "前端地址: http://localhost:5173" -ForegroundColor Cyan
Write-Host "后端地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Blue
Write-Host "使用的 Python 环境: Conda 环境 'oriching'" -ForegroundColor Magenta

Read-Host "按任意键退出"

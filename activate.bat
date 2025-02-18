@echo off

:: 获取脚本所在目录
SET SCRIPT_DIR=%~dp0

:: 切换到脚本目录
cd /d "%SCRIPT_DIR%"

:: 检查venv是否存在，如果不存在则创建
if not exist deepseek_qa\venv (
    echo Creating virtual environment...
    python -m venv deepseek_qa\venv
    call deepseek_qa\venv\Scripts\activate
    echo Installing required packages...
    pip install -r deepseek_qa\requirements.txt
) else (
    call deepseek_qa\venv\Scripts\activate
    
    :: 检查是否需要安装或更新依赖
    pip list --outdated > nul 2>&1
    if errorlevel 1 (
        echo Updating required packages...
        pip install -r deepseek_qa\requirements.txt
    )
)

:: 设置命令提示符
set PROMPT=(deepseek_qa) $P$G

:: 启动一个新的命令行窗口，保持在虚拟环境中
cmd /k 
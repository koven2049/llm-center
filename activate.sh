#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 检查venv是否存在，如果不存在则创建
if [ ! -d "deepseek-r1/venv" ]; then
    echo "Creating virtual environment..."
    python -m venv deepseek-r1/venv
    source deepseek-r1/venv/bin/activate
    echo "Installing required packages..."
    pip install -r deepseek-r1/requirements.txt
else
    source deepseek-r1/venv/bin/activate
    
    # 检查是否需要安装或更新依赖
    if [ deepseek-r1/requirements.txt -nt deepseek-r1/venv/pip-selfcheck.json ]; then
        echo "Updating required packages..."
        pip install -r deepseek-r1/requirements.txt
    fi
fi

# 设置PS1提示符，显示项目名称
export PS1="(deepseek-r1) $PS1"

# 启动一个新的shell，保持在虚拟环境中
exec $SHELL 
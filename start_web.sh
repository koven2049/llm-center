#!/bin/bash

# 默认端口
DEFAULT_PORT=8501

# 检查是否传入端口参数，如果传入则使用传入的端口，否则使用默认端口
if [ -n "$1" ]; then
    PORT=$1
else
    PORT=$DEFAULT_PORT
fi

# 切换到 web_app.py 所在的目录 (根据您的实际路径修改)
cd deepseek-r1

# 使用 nohup 在后台运行 streamlit 应用，并将日志输出到 /tmp/llm-web.log 文件
nohup streamlit run web_app.py --server.port $PORT > /tmp/llm-web.log 2>&1 &

echo "Web application started in the background on port $PORT. Logs are being written to /tmp/llm-web.log" 
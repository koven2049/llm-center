#!/bin/bash

# 精确查找包含 "streamlit run web_app.py" 命令的进程
PROCESS_ID=$(ps aux | grep "streamlit run web_app.py" | grep -v grep | awk '{print $2}')

if [ -z "$PROCESS_ID" ]; then
    echo "Web application is not running."
else
    echo "Stopping web application with PID: $PROCESS_ID"
    kill $PROCESS_ID
    echo "Web application stopped."
fi 
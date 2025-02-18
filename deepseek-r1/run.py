import os
import sys
import subprocess
import signal  # 导入 signal 模块

def ensure_venv():
    """确保在虚拟环境中运行"""
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
        if not os.path.exists(venv_path):
            print("Virtual environment not found. Please run 'source activate.sh' first")
            sys.exit(1)
        
        python_executable = os.path.join(venv_path, "bin", "python")
        os.execv(python_executable, [python_executable] + sys.argv)

def start_streamlit():
    web_app_path = os.path.join(os.path.dirname(__file__), "web_app.py")
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        web_app_path,
        # "--server.headless=true", # 移除 headless 参数
    ]

    # 移除重定向代码
    # if os.name == 'nt':
    #     stdout_redirect = open(os.devnull, 'w')
    # else:
    #     stdout_redirect = subprocess.DEVNULL
    # process = subprocess.Popen(command, stdout=stdout_redirect, stderr=stdout_redirect)

    process = subprocess.Popen(command) # 恢复原始的 Popen 调用
    return process

def signal_handler(sig, frame):
    print('\nGracefully shutting down...')
    sys.exit(0)

def main():
    ensure_venv()
    
    if len(sys.argv) < 2:
        print("Usage: python run.py [cli/web] [--port PORT]")
        return
    
    mode = sys.argv[1]
    
    if mode == "cli":
        # 移除 "cli" 参数并传递其余参数
        sys.argv.pop(1)
        from cli import main as cli_main
        cli_main()
    elif mode == "web":
        # 注册信号处理函数
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        print("Starting Streamlit web app...")
        web_process = start_streamlit()
        web_process.wait() # 等待 Web 应用进程结束 (但这部分可能需要根据实际情况调整)
    else:
        print("Invalid mode. Use 'cli' or 'web'")

if __name__ == "__main__":
    main() 
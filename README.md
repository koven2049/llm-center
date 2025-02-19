# LLM 本地系统

**Usage:**

**CLI:**
提问: `python cli.py -q "你的问题"`
交互模式: `python cli.py -i`
选择模式 (`-c` chat, `-r` reasoning): `python cli.py -r -q "问题"`
选择 Provider (`--provider` siliconflow, bailian, qwen, bytedance): `python cli.py --provider bailian -q "问题"`

**Web App:**
启动: `./start_web.sh [端口号]` (默认端口: 8501)
停止: `./stop_web.sh`
访问: `http://localhost:8501` (或指定端口)

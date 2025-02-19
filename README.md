# LLM 本地系统

这是一个使用 DeepSeek 模型或其他 LLM API 供应商（如 Bailian、Qwen、Bytedance）的本地 LLM 系统。它支持命令行界面 (CLI) 和 Web 应用程序界面，您可以根据需要选择使用。

## 功能

* 多 Provider 支持: 支持 SiliconFlow, Bailian, Qwen, Bytedance 等多个 API 服务提供商。
* 多种模式: 支持 Chat 模式 (速度快，准确度稍低) 和 Reasoning 模式 (速度慢，准确度更高)。
* 命令行界面 (CLI): 方便在终端中快速提问和交互。
* Web 应用程序界面: 提供更友好的用户界面，支持聊天历史记录和 Token 统计。
* Token 使用统计: 记录并显示每个 Provider 的 Token 使用情况。
* 聊天历史: Web 界面支持保存和查看聊天历史记录。

## 准备工作

1. **进入虚拟环境**:
   sh activate.sh

2. **配置 API 密钥**:

   * 复制 `.env.example` 文件并重命名为 `.env`。
   * 编辑 `.env` 文件，填写您选择的 API Provider 的 API 密钥和相关配置信息。

   ```bash
   cp .env.example .env
   # 然后编辑 .env 文件，填入您的 API 密钥
   ```

   **请不要将 `.env` 文件提交到代码仓库，以保护您的 API 密钥安全。**

   请根据您使用的 Provider 修改 `.env` 文件中的配置。

## 典型用法

### 1. 命令行界面 (CLI)

* **提问**:

   ```bash
   python cli.py -q "什么是大型语言模型？"
   ```

* **交互模式**:

   ```bash
   python cli.py -i
   ```

   启动后，您将看到欢迎信息和提示符，可以开始输入问题。

* **选择模式**:
   * 使用 Chat 模式 (默认): `-c` 或 `--chat`
   * 使用 Reasoning 模式: `-r` 或 `--reasoning` 或 `--inference`

* **选择 Provider**:

   使用 `--provider` 参数，可选值: `siliconflow`, `bailian`, `qwen`, `bytedance` (默认: `siliconflow`)

### 2. Web 应用程序界面

* **启动 Web 应用**:

   ```bash
   # 启动 Web 应用，使用默认端口 (8501)
   ./start_web.sh

   # 启动 Web 应用，指定端口为 8080
   ./start_web.sh 8080
   ```

   启动成功后，通过浏览器访问 `http://localhost:8501` (或指定端口)。

* **停止 Web 应用**:

   ```bash
   ./stop_web.sh
   ```

希望这份 README 文件能够帮助您更好地使用 LLM 本地系统！如有任何问题或建议，欢迎提出

import argparse
import sys
from model_handler import DeepseekHandler
import time  # 导入 time 模块

def main():
    parser = argparse.ArgumentParser(description="LLM Local System")
    parser.add_argument("--question", "-q", type=str, help="Input your question")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode")

    # 使用互斥组来选择 chat 或 reasoning 模式
    mode_group = parser.add_mutually_exclusive_group(required=False)
    mode_group.add_argument("--chat", "-c", action="store_true", help="Enable chat mode (faster, less accurate)")
    mode_group.add_argument("--reasoning", "-r", "--inference", action="store_true", help="Enable reasoning mode (slower, more accurate)")

    # 添加 API 提供商选择参数
    parser.add_argument("--provider", choices=["siliconflow", "bailian", "qwen", "bytedance"],
                       default="siliconflow",
                       help="Choose API service provider (default: siliconflow)")

    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        sys.argv.pop(1)

    args = parser.parse_args()

    # 确定选择的模式
    modes = []
    if args.chat:
        modes.append("chat")
    elif args.reasoning:
        modes.append("reasoning")
    else:
        modes.append("chat")

    # 创建 model_handler 时传入 api_provider
    model_handler = DeepseekHandler(modes=modes, api_provider=args.provider)

    if args.interactive:
        print(f"Welcome to LLM Local System - Modes: {', '.join(m.upper() for m in modes)} (Provider: {args.provider}) (Enter 'quit' to exit)")
        while True:
            question = input("\nEnter your question: ")
            if question.lower() == 'quit':
                break

            start_time = time.time()  # 记录开始时间
            response = model_handler.generate_response(question)
            elapsed_time = time.time() - start_time  # 计算耗时

            # 获取 token 使用情况
            usage = model_handler.last_usage
            prompt_tokens = usage.get('prompt_tokens', 'N/A')
            completion_tokens = usage.get('completion_tokens', 'N/A')

            print(f"\nAnswer: {response} (Time: {elapsed_time:.2f}s, Tokens: prompt[{prompt_tokens}], completion[{completion_tokens}])")

    elif args.question:
        start_time = time.time()  # 记录开始时间
        response = model_handler.generate_response(args.question)
        elapsed_time = time.time() - start_time  # 计算耗时

        # 获取 token 使用情况
        usage = model_handler.last_usage
        prompt_tokens = usage.get('prompt_tokens', 'N/A')
        completion_tokens = usage.get('completion_tokens', 'N/A')

        print(f"Answer: {response} (Time: {elapsed_time:.2f}s, Tokens: prompt[{prompt_tokens}], completion[{completion_tokens}])")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
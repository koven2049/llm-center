import streamlit as st
from model_handler import DeepseekHandler
from collections import defaultdict
import time

# 添加 CSS 样式
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5em;
        font-weight: bold;
        color: #64B5F6; /* 淡蓝色，更柔和 */
        text-align: center;
        margin-bottom: 0.5em;
    }
    .provider-select {
        margin-top: 0.5em; /* 减少上边距 */
        margin-bottom: 0.5em; /* 减少下边距 */
    }
    .mode-select {
        margin-bottom: 0.5em; /* 减少下边距 */
    }
    .token-stats {
        margin-top: 0.5em; /* 减少上边距 */
        margin-bottom: 0.5em; /* 减少下边距 */
    }
    .answer {
        margin-top: 0.5em; /* 减少上边距 */
        margin-bottom: 0.5em; /* 减少下边距 */
    }
    /* 调整侧边栏样式 */
    .stSidebar {
        padding-top: 1em;      /* 增加侧边栏顶部内边距 */
        padding-left: 1em;     /* 增加侧边栏左侧内边距 */
    }
    .stSidebar .st-expander {
        margin-bottom: 0.5em;  /* 减少 expander 之间的间距 */
    }
    .stSidebar .st-header {
        margin-bottom: 0.5em;  /* 减少侧边栏 header 下方间距 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def initialize_token_stats():
    if 'token_stats' not in st.session_state:
        st.session_state.token_stats = defaultdict(lambda: defaultdict(int))

def update_token_stats(provider, model, prompt_tokens, completion_tokens):
    stats = st.session_state.token_stats[provider]
    stats['prompt_tokens'] += prompt_tokens
    stats['completion_tokens'] += completion_tokens
    stats['total_tokens'] = stats['prompt_tokens'] + stats['completion_tokens']
    stats['model'] = model

def display_token_stats():
    if 'token_stats' in st.session_state:
        st.write("### Token Usage Statistics")
        for provider, stats in st.session_state.token_stats.items():
            if stats['total_tokens'] > 0:  # 只显示有使用量的服务
                st.write(f"**{provider.upper()} ({stats['model']}):**")
                st.write(f"- Total Prompt Tokens: {stats['prompt_tokens']}")
                st.write(f"- Total Completion Tokens: {stats['completion_tokens']}")
                st.write(f"- Total Tokens: {stats['total_tokens']}")
                st.write("---")

def initialize_chat_history():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def display_chat_history():
    st.sidebar.header("Chat History")
    if st.session_state.chat_history:
        for item in st.session_state.chat_history:
            with st.sidebar.expander(f"Turn {item['turn_num']} - {item['model_name']}", expanded=False):
                st.write(f"**Model:** {item['model_name']}")
                st.write(f"**Time:** {item['time']:.2f}s")
                st.write(f"**Tokens:** Prompt[{item['prompt_tokens']}], Completion[{item['completion_tokens']}]")
                st.write(f"**Question:** {item['question']}")
                st.write(f"**Answer:** {item['answer']}")
    else:
        st.sidebar.write("No chat history yet.")

def main():
    # 添加 CSS 样式 (放在 main 函数内部，确保样式生效)
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #64B5F6; /* 淡蓝色，更柔和 */
            text-align: center;
            margin-bottom: 0.5em;
        }
        .provider-select {
            margin-top: 1em;
            margin-bottom: 1em;
        }
        .mode-select {
            margin-bottom: 1em;
        }
        .token-stats {
            margin-top: 1em;
            margin-bottom: 1em;
        }
        .answer {
            margin-top: 1em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("LLM Local System")
    initialize_token_stats()
    initialize_chat_history()

    # 分栏布局：左侧主界面，右侧侧边栏
    main_col, sidebar_col = st.columns([3, 1]) # 调整宽度比例

    with main_col: # 主界面列
        # 添加 API 服务选择
        st.write("### Select Provider")
        api_provider = st.radio(
            "Choose Provider:",
            ["SiliconFlow", "Bailian", "Qwen"],
            index=0,
            help="Choose between SiliconFlow, Aliyun Bailian and Qwen services"
        ).lower()

        # 添加模式选择
        st.write("### Select Mode")
        mode_select = st.radio(
            "Choose Mode:",
            ["Chat Mode (Default)", "Reasoning Mode"],
            index=0,
            help="Choose between Chat (faster, less accurate) and Reasoning (slower, more accurate) modes."
        )

        # 确定当前选择的模式
        current_modes = []
        if mode_select == "Reasoning Mode":
            current_modes.append("reasoning")
        else:
            current_modes.append("chat")

        # Initialize model handler with api_provider
        if ('model_handler' not in st.session_state or
            st.session_state.current_modes != current_modes or
            st.session_state.api_provider != api_provider):
            st.session_state.model_handler = DeepseekHandler(modes=current_modes, api_provider=api_provider)
            st.session_state.current_modes = current_modes
            st.session_state.api_provider = api_provider
            # 清除之前的表单状态
            if 'form_submitted' in st.session_state:
                del st.session_state.form_submitted

        # 显示当前配置
        st.write(f"Active modes: {', '.join(m.upper() for m in current_modes)}")
        st.write(f"API Provider: {api_provider.upper()}")

        # 添加快捷键提示
        st.markdown("""
        <style>
            .shortcut-hint {
                font-size: 0.8em;
                color: #666;
                margin-top: -1em;
                margin-bottom: 0.5em;
            }
        </style>
        """, unsafe_allow_html=True)

        # 创建一个表单来捕获回车键
        with st.form(key='qa_form'):
            question = st.text_area(
                "Enter your question:",
                height=100,
                help="Press Ctrl+Enter (Windows) or ⌘+Enter (Mac) to submit"
            )

            col1, col2 = st.columns([6, 1])
            with col1:
                submit_button = st.form_submit_button("Get Answer")
            with col2:
                clear_stats = st.form_submit_button("Stop")

            if clear_stats:
                st.session_state.token_stats = defaultdict(lambda: defaultdict(int))
                st.rerun()

            # 只在用户主动提交时处理请求
            if submit_button:
                st.session_state.form_submitted = True
                if question:
                    is_reasoning = "reasoning" in current_modes
                    response_placeholder = st.empty()
                    time_placeholder = st.empty()  # 添加时间显示的占位符

                    start_time = time.time()  # 记录开始时间

                    with st.spinner(f"Generating response using {api_provider.upper()} API..."):
                        response = st.session_state.model_handler.generate_response(question)

                        # 计算并显示耗时
                        elapsed_time = time.time() - start_time
                        time_placeholder.write(f"Time elapsed: {elapsed_time:.2f}s") #  重新添加计时器显示

                        # 获取当前请求的 token 使用情况
                        if hasattr(st.session_state.model_handler, 'last_usage'):
                            usage = st.session_state.model_handler.last_usage
                            prompt_tokens = usage.get('prompt_tokens', 0)
                            completion_tokens = usage.get('completion_tokens', 0)

                            # 更新统计信息
                            update_token_stats(
                                api_provider,
                                st.session_state.model_handler._determine_model_name(current_modes),
                                prompt_tokens,
                                completion_tokens
                            )

                            # 显示当前请求的 token 使用情况
                            st.write(f"Current request tokens: prompt[{prompt_tokens}], completion[{completion_tokens}]")

                            # 添加到聊天历史
                            st.session_state.chat_history.append({
                                'turn_num': len(st.session_state.chat_history) + 1,
                                'model_name': st.session_state.model_handler._determine_model_name(current_modes),
                                'time': elapsed_time,
                                'prompt_tokens': prompt_tokens,
                                'completion_tokens': completion_tokens,
                                'question': question,
                                'answer': response
                            })

                        st.markdown("### Answer:")
                        if is_reasoning:
                            # 对于 reasoning 模式，使用 placeholder 来显示流式响应
                            response_placeholder.markdown(response)
                        else:
                            # 对于 chat 模式，直接显示完整响应
                            st.write(response)
                else:
                    st.warning("Please enter a question!")

    with sidebar_col: # 侧边栏列
        display_chat_history()
        display_token_stats()


if __name__ == "__main__":
    main() 
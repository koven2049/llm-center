import os
import requests
from dotenv import load_dotenv
from typing import List, Dict
import sys  # 导入 sys 模块

class DeepseekHandler:
    # 整合所有平台的配置
    PROVIDER_CONFIGS = {
        'siliconflow': {
            'models': {
                'chat': 'deepseek-ai/DeepSeek-V3',
                'reasoning': 'deepseek-ai/DeepSeek-R1'
            },
            'env_keys': {
                'api_key': 'SILICONFLOW_API_KEY',
                'base_url': 'API_BASE_URL',
                'chat_path': 'API_CHAT_PATH'
            },
            'auth_format': 'Bearer {api_key}'
        },
        'bailian': {
            'models': {
                'chat': 'deepseek-v3',
                'reasoning': 'deepseek-r1'
            },
            'env_keys': {
                'api_key': 'BAILIAN_API_KEY',
                'base_url': 'BAILIAN_API_BASE_URL',
                'chat_path': 'BAILIAN_API_CHAT_PATH'
            },
            'auth_format': '{api_key}'
        },
        'qwen': {
            'models': {
                'chat': 'qwen-turbo',
                'reasoning': 'qwen-plus'  
            },
            'env_keys': {
                'api_key': 'QWEN_API_KEY',
                'base_url': 'QWEN_API_BASE_URL',
                'chat_path': 'QWEN_API_CHAT_PATH'
            },
            'auth_format': '{api_key}'  # 根据 qwen 的认证方式调整
        },
        'bytedance': {
            'models': {
                'chat': 'deepseek-r1-distill-qwen-7b-250120',
                'reasoning': 'deepseek-r1-distill-qwen-32b-250120'
            },
            'env_keys': {
                'api_key': 'BYTEDANCE_API_KEY',
                'base_url': 'BYTEDANCE_API_BASE_URL',
                'chat_path': 'BYTEDANCE_API_CHAT_PATH'
            },
            'auth_format': 'Bearer {api_key}'
        }
    }

    def __init__(self, modes: List[str] = None, api_provider: str = 'siliconflow'):
        load_dotenv()
        
        if api_provider not in self.PROVIDER_CONFIGS:
            raise ValueError(f"Unsupported API provider: {api_provider}")
            
        self.api_provider = api_provider
        config = self.PROVIDER_CONFIGS[api_provider]
        
        # 从环境变量加载配置
        env_keys = config['env_keys']
        self.api_key = os.getenv(env_keys['api_key'])
        if not self.api_key:
            raise ValueError(f"Please set {env_keys['api_key']} in .env file")
            
        self.api_base_url = os.getenv(env_keys['base_url'])
        self.api_chat_path = os.getenv(env_keys['chat_path'])
        self.api_url = f"{self.api_base_url}{self.api_chat_path}"
        
        self.headers = {
            "Authorization": config['auth_format'].format(api_key=self.api_key),
            "Content-Type": "application/json"
        }
        
        self.modes = modes or ["chat"]

    def _determine_model_name(self, modes):
        """
        根据选择的模式和 API 提供商确定模型名称
        """
        mode = "reasoning" if "reasoning" in modes else "chat"
        try:
            return self.PROVIDER_CONFIGS[self.api_provider]['models'][mode]
        except KeyError:
            raise ValueError(f"No model configured for provider '{self.api_provider}' and mode '{mode}'")

    def generate_response(self, question):
        try:
            messages = [{"role": "user", "content": question}]
            model = self._determine_model_name(self.modes)
            is_reasoning = "reasoning" in self.modes
            
            payload = {
                "messages": messages,
                "model": model,
                "temperature": 0.3 if is_reasoning else 0.7,
                "max_tokens": 512 if "chat" in self.modes else 4096,
                "stream": False  # 暂时禁用 reasoning 模式的 stream
            }
            
            if is_reasoning:
                payload["top_p"] = 0.1
            
            print(f"API Provider: {self.api_provider}")
            print(f"Sending request to {self.api_url}")
            print(f"Payload: {payload}")
            print(f"Headers: {self.headers}")
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=90 if is_reasoning else 30
            )
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                return f"Error: {response.status_code} - {response.text}"
            
            result = response.json()
            # 保存 usage 信息
            self.last_usage = result.get('usage', {})
            
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {str(e)}")
            return f"Error calling {self.api_provider.upper()} API: {str(e)}"
        except Exception as e:
            print(f"General exception: {str(e)}")
            return f"Unexpected error: {str(e)}" 
import os
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

class DeepSeekAPI:
    """DeepSeek API客户端类
    
    该类封装了与DeepSeek API的所有交互，提供了一系列方法来处理数学教育相关的任务，
    包括解答数学问题、解释数学概念、批改作业和提供学习建议等功能。
    
    属性:
        api_key: DeepSeek API的访问密钥
        api_base_url: DeepSeek API的基础URL
        headers: 请求头信息，包含认证信息
    """
    def __init__(self):
        """初始化DeepSeekAPI实例
        
        从环境变量中读取API密钥和URL，设置请求头信息。
        如果未设置API密钥，将抛出ValueError异常。
        """
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_base_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

    def _make_request(self, endpoint: str, payload: Dict) -> Dict:
        """发送请求到DeepSeek API
        
        这是一个内部方法，用于处理与DeepSeek API的所有HTTP通信。
        
        参数:
            endpoint: API端点名称
            payload: 请求负载数据
            
        返回:
            Dict: API响应的内容部分
            
        异常:
            Exception: 当API请求失败时抛出，包含详细的错误信息
        """
        try:
            response = requests.post(
                self.api_base_url,
                headers=self.headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [{
                        "role": "system",
                        "content": "你是一个专业的数学教育助手，擅长解答数学问题并提供详细的解题步骤。"
                    }, {
                        "role": "user",
                        "content": payload.get("prompt", "")
                    }],
                    "temperature": 0.7,
                    "max_tokens": payload.get("max_tokens", 1000),
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            return {"content": result.get("choices", [{}])[0].get("message", {}).get("content", "")}
        except requests.exceptions.RequestException as e:
            error_msg = f"API请求失败: {str(e)}"
            if response := getattr(e, "response", None):
                error_msg += f" - 状态码: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - 详细信息: {error_detail}"
                except:
                    pass
            raise Exception(error_msg)

    def solve_math_problem(self, question: str, context: Optional[str] = None) -> Dict:
        """解答数学问题，提供详细的解题步骤
        
        参数:
            question: 需要解答的数学问题
            context: 可选的问题上下文信息
            
        返回:
            Dict: 包含问题解答和解题步骤的字典
        """
        payload = {
            "prompt": f"请解答以下数学问题，并提供详细的解题步骤：\n{question}",
            "context": context,
            "max_tokens": 1000
        }
        return self._make_request("solve", payload)

    def explain_math_concept(self, concept: str, detail_level: str = "basic") -> Dict:
        """解释数学概念，提供定义、公式和示例
        
        参数:
            concept: 需要解释的数学概念
            detail_level: 解释的详细程度，可选值：'basic'（基础）, 'intermediate'（中级）, 'advanced'（高级）
            
        返回:
            Dict: 包含概念解释的字典
        """
        detail_prompts = {
            "basic": "请简单解释这个概念的基本含义和应用",
            "intermediate": "请详细解释这个概念，包括定义、性质和常见应用",
            "advanced": "请深入解释这个概念，包括理论基础、推导过程和高级应用"
        }
        payload = {
            "prompt": f"请{detail_prompts.get(detail_level, detail_prompts['basic'])}：\n{concept}",
            "max_tokens": 800
        }
        return self._make_request("explain", payload)

    def grade_student_work(self, question: str, answer: str) -> Dict:
        """自动批改学生作业并提供反馈
        
        参数:
            question: 题目内容
            answer: 学生的答案
            
        返回:
            Dict: 包含评分和详细反馈的字典
        """
        payload = {
            "prompt": f"请评估以下数学题的答案并提供详细反馈：\n题目：{question}\n学生答案：{answer}",
            "max_tokens": 500
        }
        return self._make_request("grade", payload)

    def provide_learning_advice(self, problem_areas: List[str], performance_data: Optional[Dict] = None) -> Dict:
        """基于学生表现提供个性化学习建议
        
        参数:
            problem_areas: 学生需要改进的问题领域列表
            performance_data: 可选的学生表现数据
            
        返回:
            Dict: 包含个性化学习建议和推荐资源的字典
        """
        areas_text = "\n- ".join(problem_areas)
        payload = {
            "prompt": f"请根据以下问题领域提供个性化的学习建议：\n- {areas_text}",
            "context": str(performance_data) if performance_data else None,
            "max_tokens": 600
        }
        return self._make_request("advise", payload)

# 创建API客户端实例
deepseek_client = DeepSeekAPI()
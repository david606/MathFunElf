import os
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

class DeepSeekAPI:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_base_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

    def _make_request(self, endpoint: str, payload: Dict) -> Dict:
        """发送请求到DeepSeek API"""
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
        """解答数学问题，提供详细的解题步骤"""
        payload = {
            "prompt": f"请解答以下数学问题，并提供详细的解题步骤：\n{question}",
            "context": context,
            "max_tokens": 1000
        }
        return self._make_request("solve", payload)

    def explain_math_concept(self, concept: str, detail_level: str = "basic") -> Dict:
        """解释数学概念，提供定义、公式和示例"""
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
        """自动批改学生作业并提供反馈"""
        payload = {
            "prompt": f"请评估以下数学题的答案并提供详细反馈：\n题目：{question}\n学生答案：{answer}",
            "max_tokens": 500
        }
        return self._make_request("grade", payload)

    def provide_learning_advice(self, problem_areas: List[str], performance_data: Optional[Dict] = None) -> Dict:
        """基于学生表现提供个性化学习建议"""
        areas_text = "\n- ".join(problem_areas)
        payload = {
            "prompt": f"请根据以下问题领域提供个性化的学习建议：\n- {areas_text}",
            "context": str(performance_data) if performance_data else None,
            "max_tokens": 600
        }
        return self._make_request("advise", payload)

# 创建API客户端实例
deepseek_client = DeepSeekAPI()
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import httpx
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ProblemRequest(BaseModel):
    text: str

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

async def call_deepseek_api(prompt: str) -> Optional[str]:
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # 构建提示词，要求返回Markdown格式文本和LaTeX格式公式
    system_prompt = """你是一个专业的数学老师，请用以下格式回答数学问题：
    1. 使用Markdown格式输出文本说明
    2. 数学公式必须使用LaTeX格式，并用两个美元符号包裹，例如：$$\\frac{1}{2}$$
    3. 回答要包含：
       - 问题分析
       - 解题思路（包含公式推导过程）
       - 详细步骤（每个步骤的计算过程都要用LaTeX公式展示）
       - 答案说明（最终结果用LaTeX公式展示）
    """
    
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ]
    }
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                print(f'正在发送请求到DeepSeek API，请求数据: {data}')
                response = await client.post(DEEPSEEK_API_URL, json=data, headers=headers)
                print(f'收到DeepSeek API响应状态码: {response.status_code}')
                response.raise_for_status()
                result = response.json()
                print(f'DeepSeek API响应内容: {result}')
                return result['choices'][0]['message']['content']
        except httpx.TimeoutException as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f'DeepSeek API请求超时，正在进行第{retry_count}次重试...')
                await asyncio.sleep(1)
                continue
            print(f'DeepSeek API请求超时，已重试{max_retries}次: {str(e)}')
            return f'API请求超时: {str(e)}'
        except httpx.HTTPError as e:
            error_msg = f'DeepSeek API HTTP错误: {str(e)}\n状态码: {e.response.status_code if hasattr(e, "response") else "未知"}\n响应内容: {e.response.text if hasattr(e, "response") else "未知"}'
            print(error_msg)
            return f'API请求失败: {str(e)}'
        except httpx.RequestError as e:
            print(f'DeepSeek API网络错误: {str(e)}')
            return f'网络连接错误: {str(e)}'
        except KeyError as e:
            print(f'DeepSeek API响应格式错误: {str(e)}')
            return f'API响应格式错误: {str(e)}'
        except Exception as e:
            print(f'DeepSeek API未知错误: {str(e)}')
            return f'系统错误: {str(e)}'

@router.post('/analyze-problem')
async def analyze_problem(request: ProblemRequest):
    answer = await call_deepseek_api(request.text)
    if answer:
        if answer.startswith('API') or answer.startswith('网络') or answer.startswith('系统'):
            return {'error': answer}
        return {'answer': answer}
    return {'error': '无法获取答案'}

@router.post('/analyze-problem-image')
async def analyze_problem_image(file: UploadFile = File(...)):
    # TODO: 实现图片OCR功能，提取图片中的文字
    # 目前先返回错误信息
    return {'error': '图片分析功能正在开发中'}
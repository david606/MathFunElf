from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from deepseek import deepseek_client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MathFunElf - DeepSeek数学教育助手",
    description="基于DeepSeek V3的智能数学教育辅助系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600
)

class MathQuestion(BaseModel):
    """数学问题数据模型
    
    属性:
        question: 数学问题的具体内容
        context: 可选的问题上下文信息，帮助更好地理解和解答问题
    """
    question: str
    context: Optional[str] = None

class MathConcept(BaseModel):
    """数学概念数据模型
    
    属性:
        concept: 需要解释的数学概念名称
        detail_level: 解释的详细程度，可选值：'basic'（基础）, 'intermediate'（中级）, 'advanced'（高级）
    """
    concept: str
    detail_level: Optional[str] = "basic"

class StudentWork(BaseModel):
    """学生作业数据模型
    
    属性:
        question: 题目内容
        answer: 学生的答案
        student_id: 可选的学生ID，用于跟踪学生的作业记录
    """
    question: str
    answer: str
    student_id: Optional[str] = None

class LearningAnalysis(BaseModel):
    """学习分析数据模型
    
    属性:
        student_id: 学生ID，用于识别具体学生
        problem_areas: 学生需要改进的问题领域列表
        performance_data: 可选的学生表现数据，用于更精准的学习建议
    """
    student_id: str
    problem_areas: List[str]
    performance_data: Optional[dict] = None

@app.post("/solve-math")
async def solve_math_problem(question: MathQuestion):
    """解答数学问题，提供详细的解题步骤
    
    接收数学问题并返回详细的解题过程，包括步骤说明和最终答案。
    
    参数:
        question: MathQuestion对象，包含问题内容和可选的上下文信息
        
    返回:
        包含解题步骤和答案的JSON响应
        
    异常:
        HTTPException: 当API调用失败时抛出，状态码500
    """
    try:
        result = deepseek_client.solve_math_problem(question.question, question.context)
        return {"status": "success", "solution": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain-concept")
async def explain_math_concept(concept: MathConcept):
    """解释数学概念，提供定义、公式和示例"""
    try:
        result = deepseek_client.explain_math_concept(concept.concept, concept.detail_level)
        return {"status": "success", "explanation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grade-work")
async def grade_student_work(work: StudentWork):
    """自动批改学生作业并提供反馈"""
    try:
        result = deepseek_client.grade_student_work(work.question, work.answer)
        return {"status": "success", "grade": result.get("grade"), "feedback": result.get("feedback")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learning-advice")
async def provide_learning_advice(analysis: LearningAnalysis):
    """基于学生表现提供个性化学习建议"""
    try:
        result = deepseek_client.provide_learning_advice(analysis.problem_areas, analysis.performance_data)
        return {"status": "success", "advice": result.get("advice"), "resources": result.get("resources", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "欢迎使用MathFunElf - DeepSeek数学教育助手"}
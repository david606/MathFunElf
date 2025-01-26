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
    question: str
    context: Optional[str] = None

class MathConcept(BaseModel):
    concept: str
    detail_level: Optional[str] = "basic"

class StudentWork(BaseModel):
    question: str
    answer: str
    student_id: Optional[str] = None

class LearningAnalysis(BaseModel):
    student_id: str
    problem_areas: List[str]
    performance_data: Optional[dict] = None

@app.post("/solve-math")
async def solve_math_problem(question: MathQuestion):
    """解答数学问题，提供详细的解题步骤"""
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
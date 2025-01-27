# MathFunElf - DeepSeek数学教育助手

MathFunElf是一个基于DeepSeek大语言模型的智能数学教育助手，旨在帮助学生更好地理解和学习数学知识。

## 功能特点

- 智能题目解析：详细分析数学题目的解题思路和步骤
- 知识点讲解：针对性地解释相关数学概念和原理
- 个性化辅导：根据学生的学习水平提供适合的练习题
- 实时交互：支持自然语言对话式的学习辅导

## 技术架构

### 后端
- FastAPI：高性能的Python Web框架
- DeepSeek API：强大的大语言模型支持
- Pydantic：数据验证和序列化

### 前端
- React + TypeScript：现代化的前端开发框架
- Vite：下一代前端构建工具

## 环境要求

- Python 3.8+
- Node.js 16+
- npm 8+

## 安装部署

1. 克隆项目并安装后端依赖：
```bash
git clone <repository-url>
cd MathFunElf
pip install -r requirements.txt
```

2. 配置环境变量：
创建.env文件并设置以下变量：
```
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
```

3. 安装前端依赖：
```bash
cd frontend
npm install
```

## 启动服务

1. 启动后端服务：
```bash
python start.py
```
后端服务将在 http://localhost:8000 运行

2. 启动前端开发服务器：
```bash
cd frontend
npm run dev
```
前端服务将在 http://localhost:5173 运行

## API接口

### 数学问题解答
- 端点：`/api/solve`
- 方法：POST
- 请求体：
```json
{
    "question": "请解答这道数学题...",
    "level": "high_school"
}
```

### 知识点讲解
- 端点：`/api/explain`
- 方法：POST
- 请求体：
```json
{
    "topic": "三角函数",
    "detail_level": "basic"
}
```

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。在提交代码前，请确保：

1. 代码符合项目的编码规范
2. 添加必要的测试用例
3. 更新相关文档

## 开发计划

- [ ] 添加更多数学题型支持
- [ ] 优化解题推理过程
- [ ] 实现学习进度追踪
- [ ] 支持多语言界面

## 许可证

本项目采用 MIT 许可证
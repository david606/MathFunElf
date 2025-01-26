# MathFunElf - DeepSeek数学教育助手

基于DeepSeek大语言模型的智能数学教育辅助系统，旨在为学生和教师提供全方位的数学学习支持。

## 功能特点

- **智能解题**：提供详细的数学问题解题步骤和思路
- **概念讲解**：深入浅出地解释数学概念，包含定义、公式和示例
- **作业批改**：自动批改学生作业并提供个性化反馈
- **学习建议**：基于学生表现提供针对性的学习建议和资源推荐

## 技术架构

### 后端
- FastAPI：高性能的Python Web框架
- DeepSeek API：强大的大语言模型支持
- Pydantic：数据验证和序列化

### 前端
- React + TypeScript：现代化的前端开发框架
- Vite：下一代前端构建工具

## 安装部署

1. 克隆项目并安装后端依赖：
```bash
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
uvicorn app:app --reload
```

2. 启动前端开发服务器：
```bash
cd frontend
npm run dev
```

## API接口

### 1. 解答数学问题
- 端点：`POST /solve-math`
- 功能：提供详细的解题步骤

### 2. 解释数学概念
- 端点：`POST /explain-concept`
- 功能：提供概念解释，支持基础/中级/高级详细程度

### 3. 批改作业
- 端点：`POST /grade-work`
- 功能：自动评分并提供反馈

### 4. 学习建议
- 端点：`POST /learning-advice`
- 功能：提供个性化学习建议

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。在提交代码前，请确保：

1. 代码符合项目的编码规范
2. 添加必要的测试用例
3. 更新相关文档

## 许可证

MIT License
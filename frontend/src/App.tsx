import { useState } from 'react'
import { Layout, Menu, Card, Input, Button, Select, Typography, message } from 'antd'
import { QuestionCircleOutlined, BookOutlined, CheckCircleOutlined, UserOutlined } from '@ant-design/icons'
import axios from 'axios'
import './App.css'

const { Header, Content } = Layout
const { Title, Paragraph } = Typography
const { TextArea } = Input

/**
 * MathFunElf主应用组件
 * 提供数学问题解答、概念解释、作业批改和学习建议等功能
 */
function App() {
  // 状态管理
  /** 当前激活的功能标签 */
  const [activeTab, setActiveTab] = useState('solve')
  /** 加载状态 */
  const [loading, setLoading] = useState(false)
  /** 数学问题或作业题目 */
  const [question, setQuestion] = useState('')
  /** 数学概念 */
  const [concept, setConcept] = useState('')
  /** 概念解释的详细程度 */
  const [detailLevel, setDetailLevel] = useState('basic')
  /** API响应结果 */
  const [result, setResult] = useState('')
  /** 学生答案 */
  const [answer, setAnswer] = useState('')
  /** 需要改进的问题领域 */
  const [problemAreas, setProblemAreas] = useState<string[]>([])

  /**
   * 切换功能标签时重置所有状态
   * @param key - 目标标签的key
   */
  const handleTabChange = (key: string) => {
    setActiveTab(key)
    setQuestion('')
    setConcept('')
    setResult('')
    setDetailLevel('basic')
    setAnswer('')
    setProblemAreas([])
  }

  /**
   * 处理表单提交
   * 根据当前激活的标签调用相应的API接口
   */
  const handleSubmit = async () => {
    setLoading(true)
    try {
      let response
      switch (activeTab) {
        case 'solve':
          // 调用数学问题解答API
          response = await axios.post('http://localhost:8000/solve-math', {
            question,
            context: null
          })
          setResult(response.data.solution.content)
          break
        case 'explain':
          // 调用概念解释API
          response = await axios.post('http://localhost:8000/explain-concept', {
            concept,
            detail_level: detailLevel
          })
          setResult(response.data.explanation.content)
          break
        case 'grade':
          // 输入验证
          if (!question || !answer) {
            message.error('请输入题目和答案')
            return
          }
          // 调用作业批改API
          response = await axios.post('http://localhost:8000/grade-work', {
            question,
            answer
          })
          setResult(`评分结果：${response.data.grade}\n\n详细反馈：\n${response.data.feedback}`)
          break
        case 'advice':
          // 输入验证
          if (!problemAreas.length) {
            message.error('请至少输入一个需要改进的问题领域')
            return
          }
          // 调用学习建议API
          response = await axios.post('http://localhost:8000/learning-advice', {
            student_id: 'temp-user',
            problem_areas: problemAreas
          })
          setResult(`学习建议：\n${response.data.advice}\n\n推荐资源：\n${response.data.resources.join('\n')}`)
          break
        default:
          message.error('功能暂未实现')
      }
    } catch (error) {
      // 错误处理
      if (axios.isAxiosError(error)) {
        if (error.response) {
          message.error(`请求失败: ${error.response.data?.detail || error.response.statusText}`)
        } else if (error.request) {
          message.error('无法连接到服务器，请检查网络连接')
        } else {
          message.error(`请求出错: ${error.message}`)
        }
      } else {
        message.error('发生未知错误，请稍后重试')
      }
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout className="app-container">
      <Header className="header">
        <div className="logo">MathFunElf</div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[activeTab]}
          onSelect={({ key }) => handleTabChange(key)}
        >
          <Menu.Item key="solve" icon={<QuestionCircleOutlined />}>解答问题</Menu.Item>
          <Menu.Item key="explain" icon={<BookOutlined />}>概念解释</Menu.Item>
          <Menu.Item key="grade" icon={<CheckCircleOutlined />}>作业批改</Menu.Item>
          <Menu.Item key="advice" icon={<UserOutlined />}>学习建议</Menu.Item>
        </Menu>
      </Header>
      <Content className="content">
        <Card>
          {activeTab === 'solve' && (
            <div>
              <Title level={4}>数学问题解答</Title>
              <Paragraph>请输入您的数学问题，我们将为您提供详细的解题步骤。</Paragraph>
              <TextArea
                rows={4}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="请输入您的数学问题..."
              />
            </div>
          )}
          {activeTab === 'explain' && (
            <div>
              <Title level={4}>数学概念解释</Title>
              <Paragraph>请输入您想了解的数学概念。</Paragraph>
              <Input
                value={concept}
                onChange={(e) => setConcept(e.target.value)}
                placeholder="请输入数学概念..."
                style={{ marginBottom: 16 }}
              />
              <Select
                value={detailLevel}
                onChange={setDetailLevel}
                style={{ width: 200, marginBottom: 16 }}
              >
                <Select.Option value="basic">基础解释</Select.Option>
                <Select.Option value="intermediate">进阶解释</Select.Option>
                <Select.Option value="advanced">深入解释</Select.Option>
              </Select>
            </div>
          )}
          {activeTab === 'grade' && (
            <div>
              <Title level={4}>作业批改</Title>
              <Paragraph>请输入题目和您的答案，我们将为您提供详细的评分和反馈。</Paragraph>
              <TextArea
                rows={3}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="请输入题目..."
                style={{ marginBottom: 16 }}
              />
              <TextArea
                rows={4}
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="请输入您的答案..."
              />
            </div>
          )}
          {activeTab === 'advice' && (
            <div>
              <Title level={4}>学习建议</Title>
              <Paragraph>请输入您需要改进的问题领域，我们将为您提供个性化的学习建议。</Paragraph>
              <Select
                mode="tags"
                style={{ width: '100%', marginBottom: 16 }}
                placeholder="请输入需要改进的问题领域（回车分隔）"
                onChange={setProblemAreas}
                tokenSeparators={[',']}
              />
            </div>
          )}
          <Button
            type="primary"
            onClick={handleSubmit}
            loading={loading}
            style={{ marginTop: 16 }}
          >
            提交
          </Button>
          {result && (
            <Card style={{ marginTop: 16 }}>
              <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                {result}
              </pre>
            </Card>
          )}
        </Card>
      </Content>
    </Layout>
  )
}

export default App

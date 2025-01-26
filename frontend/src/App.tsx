import { useState } from 'react'
import { Layout, Menu, Card, Input, Button, Select, Typography, message } from 'antd'
import { QuestionCircleOutlined, BookOutlined, CheckCircleOutlined, UserOutlined } from '@ant-design/icons'
import axios from 'axios'
import './App.css'

const { Header, Content } = Layout
const { Title, Paragraph } = Typography
const { TextArea } = Input

function App() {
  const [activeTab, setActiveTab] = useState('solve')
  const [loading, setLoading] = useState(false)
  const [question, setQuestion] = useState('')
  const [concept, setConcept] = useState('')
  const [detailLevel, setDetailLevel] = useState('basic')
  const [result, setResult] = useState('')

  const handleSubmit = async () => {
    setLoading(true)
    try {
      let response
      switch (activeTab) {
        case 'solve':
          response = await axios.post('http://localhost:8000/solve-math', {
            question,
            context: null
          })
          setResult(response.data.solution.content)
          break
        case 'explain':
          response = await axios.post('http://localhost:8000/explain-concept', {
            concept,
            detail_level: detailLevel
          })
          setResult(response.data.explanation.content)
          break
        default:
          message.error('功能暂未实现')
      }
    } catch (error) {
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
          onSelect={({ key }) => setActiveTab(key)}
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

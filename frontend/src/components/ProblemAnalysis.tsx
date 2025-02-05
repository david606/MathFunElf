import React, { useState } from 'react';
import { Input, Upload, Button, Card, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { RcFile } from 'antd/es/upload';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

const { TextArea } = Input;

interface ProblemAnalysisProps {}

const ProblemAnalysis: React.FC<ProblemAnalysisProps> = () => {
  const [textInput, setTextInput] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTextSubmit = async () => {
    if (!textInput.trim()) {
      message.warning('请输入数学问题');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/analyze-problem', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
      });

      const data = await response.json();
      if (data.answer) {
        setAnswer(data.answer);
      } else if (data.error) {
        message.error(data.error);
        setAnswer('');
      } else {
        message.error('获取答案失败');
        setAnswer('');
      }
    } catch (error) {
      message.error('请求失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const uploadProps = {
    name: 'file',
    action: 'http://localhost:8000/api/analyze-problem-image',
    beforeUpload: (file: RcFile) => {
      const isImage = file.type.startsWith('image/');
      if (!isImage) {
        message.error('只能上传图片文件！');
      }
      return isImage;
    },
    onChange: (info: any) => {
      if (info.file.status === 'done') {
        if (info.file.response.answer) {
          setAnswer(info.file.response.answer);
          message.success('图片上传成功');
        } else {
          message.error('解析图片失败');
        }
      } else if (info.file.status === 'error') {
        message.error('图片上传失败');
      }
    },
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <Card 
        title="问题解析" 
        style={{ 
          marginBottom: '24px',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}
      >
        <TextArea
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          placeholder="请输入您的数学问题"
          autoSize={{ minRows: 4, maxRows: 8 }}
          style={{ 
            marginBottom: '20px',
            fontSize: '16px',
            borderRadius: '4px',
            resize: 'none'
          }}
        />
        <div style={{ marginBottom: '16px' }}>
          <Button
            type="primary"
            onClick={handleTextSubmit}
            loading={loading}
            style={{ marginRight: '16px' }}
          >
            提交问题
          </Button>
          <Upload {...uploadProps}>
            <Button icon={<UploadOutlined />}>上传题目图片</Button>
          </Upload>
        </div>
      </Card>

      {answer && (
        <Card title="解答结果">
          <ReactMarkdown
            remarkPlugins={[remarkMath]}
            rehypePlugins={[rehypeKatex]}
            children={answer}
          />
        </Card>
      )}
    </div>
  );
};

export default ProblemAnalysis;
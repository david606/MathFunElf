import React from 'react';
import { Layout, Menu } from 'antd';
import { BookOutlined, BulbOutlined, CheckSquareOutlined, NodeIndexOutlined } from '@ant-design/icons';
import { useNavigate, useLocation, Routes, Route } from 'react-router-dom';
import ProblemAnalysis from '../ProblemAnalysis';
import './MainLayout.css';

const { Header, Sider, Content } = Layout;

const MainLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleMenuClick = (key: string) => {
    navigate(`/${key}`);
  };

  const menuItems = [
    {
      key: 'problem',
      icon: <BookOutlined />,
      label: '问题解析',
    },
    {
      key: 'concept',
      icon: <BulbOutlined />,
      label: '概念解析',
    },
    {
      key: 'homework',
      icon: <CheckSquareOutlined />,
      label: '批改作业',
    },
    {
      key: 'learning',
      icon: <NodeIndexOutlined />,
      label: '学习图谱',
    },
  ];

  return (
    <Layout className="main-layout">
      <Sider className="main-sider">
        <div className="logo">
          <h1>数学精灵</h1>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname.substring(1) || 'problem']}
          items={menuItems}
          className="main-menu"
          onClick={({ key }) => handleMenuClick(key as string)}
        />
      </Sider>
      <Layout className="site-layout">
        <Content className="main-content">
          <div className="content-container">
            <Routes>
              <Route path="/" element={<ProblemAnalysis />} />
              <Route path="/problem" element={<ProblemAnalysis />} />
              <Route path="/concept" element={<div>概念解析功能开发中...</div>} />
              <Route path="/homework" element={<div>批改作业功能开发中...</div>} />
              <Route path="/learning" element={<div>学习图谱功能开发中...</div>} />
            </Routes>
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
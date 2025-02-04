import React from 'react';
import { Layout, Menu } from 'antd';
import { BookOutlined, BulbOutlined, CheckSquareOutlined, NodeIndexOutlined } from '@ant-design/icons';
import './MainLayout.css';

const { Header, Sider, Content } = Layout;

const MainLayout: React.FC = () => {
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
          defaultSelectedKeys={['problem']}
          items={menuItems}
          className="main-menu"
        />
      </Sider>
      <Layout className="site-layout">
        <Content className="main-content">
          <div className="content-container">
            <h2>欢迎使用数学精灵！</h2>
            <p>请从左侧选择功能开始使用</p>
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
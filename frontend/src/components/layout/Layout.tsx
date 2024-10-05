import React, {Component} from 'react';

import LeftBar from './LeftBar'
import { Layout, Menu } from 'antd';
import './Layout.css'
import {inject, observer} from "mobx-react";

const { Header, Content, Footer, Sider } = Layout;

@inject('userStore')
@observer
class ILayout extends Component<any, any> {
    state = {
        collapsed: true,
      };

    onCollapse = (collapsed: boolean) => {
        // console.log(collapsed);
        this.setState({ collapsed });
    };

    render() {
        return (
            <Layout>
                <Sider
                    collapsible
                    collapsed={this.state.collapsed}
                    onCollapse={this.onCollapse}
                    style={{
                        overflow: 'auto',
                        height: '100vh',
                        left: 0,
                    }}
                >
                  <div className="logo"
                       onClick={()=>{window.location.href = '/'}}
                  />
                  <LeftBar/>
                </Sider>
                <Layout className="site-layout">
                    <Header className="site-layout-background" style={{ padding: 0 }} />
                    <Content style={{ margin: '0 16px' }}>
                      <div className="site-layout-background" style={{ padding: 24, minHeight: 360, textAlign: 'center' }}>
                        {this.props.children}
                      </div>
                    </Content>
                    <Footer style={{ textAlign: 'center' }}>{this.props.userStore.username}</Footer>
                </Layout>
            </Layout>
        );
    }
}

export default ILayout;
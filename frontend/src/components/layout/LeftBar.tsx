import React, {Component} from 'react';
import {RouteComponentProps, withRouter, matchPath, Link} from 'react-router-dom'
import {IRouter, authrouter} from "../../router/Router";

import {Menu} from "antd";
const { SubMenu } = Menu;

interface LeftBarProps extends RouteComponentProps{

}
interface LeftBarState {
    defaultOpenKeys:     string[]
    defaultSelectedKeys: string[]
}

class LeftBar extends Component<LeftBarProps, LeftBarState> {
    state = {
        defaultOpenKeys:     [],
        defaultSelectedKeys: []
    }

    componentDidMount(): void {
        this.highlightMenu(authrouter);
    }

    // 根据 this.props.location.pathname展开和高亮显示对应标签
    highlightMenu = (leftRoutes: IRouter[]) => {
        const path = this.props.location.pathname;
        //console.log(path);
        //console.log(leftRoutes);
        for (let r of leftRoutes){
            let match=matchPath(path, {path: r.path})
            if (match) {
                if(match.isExact){
                    this.setState({
                        defaultSelectedKeys: [r.id]
                    })
                } else {
                    this.setState({
                        defaultOpenKeys : [r.id]
                    })
                }
            }
            if (r.children) {
                this.highlightMenu(r.children)
            }
        }
    }

    // 根据IRouter目前的全部路由进行渲染，得到LeftBar的Menu
    generateMenu = (routerList?: IRouter[]) => {
        return (
                routerList?.map( r=>{
                if(r.children){
                    return (
                        <SubMenu key={r.id} icon={r.icon} title={r.title} >
                            {this.generateMenu(r.children)}
                        </SubMenu>
                        )
                    }
                return  (
                        <Menu.Item key={r.id} icon={r.icon}>
                            <Link to={r.path}>{r.title}</Link>
                        </Menu.Item>
                    )
                })
        )
    }

    render() {
        return (
             <>
                {this.state.defaultSelectedKeys.length>0
                    ?
                 <Menu theme="dark"
                    defaultOpenKeys={this.state.defaultOpenKeys}
                    defaultSelectedKeys={this.state.defaultSelectedKeys}
                    triggerSubMenuAction={'click'}
                    mode="inline">
                       {this.generateMenu(authrouter)}
                 </Menu>
                    :
                 <></>
                }
             </>
        );
    }
}

export default withRouter(LeftBar);
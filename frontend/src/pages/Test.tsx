import React, {Component} from 'react';
import {inject, observer} from "mobx-react";

import Player from 'griffith'
//'https://zhstatic.zhihu.com/cfe/griffith/zhihu2018_sd.mp4',
//'http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4'

class Son extends Component<any, any> {
    state = {
        sonname: this.props.sonname
    }

    render() {
        const sonname = this.props.sonname
        return (
            <div>
                This is Son: {sonname}
            </div>

        )
    }
}

class Father extends Component<any, any> {
    state = {
        sonname: '123',
        play_url: 'https://zhstatic.zhihu.com/cfe/griffith/zhihu2018_sd.mp4'
    }

    handle_Son_Onclick = ()=>{
        this.setState({
            sonname: '234',
            play_url: 'http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4'
        })
    }

    render() {
        const sources = {
                  sd: {play_url:  this.state.play_url,},
                 }
        return (
            <div>
                This is Father
                <button onClick={this.handle_Son_Onclick}>change son name</button>

                <Son
                    sonname ={this.state.sonname}
                    key = {this.state.sonname}
                />
                <Player
                    id = {this.state.play_url}
                    sources = {sources}
                />
            </div>
        )
    }
}

@inject('userStore')
@observer
class Test extends Component {
    state = {
        Html1: '<div>HTML</div>'
    }

    render() {
        return (
            <div>
                This is Page Test!
                <div dangerouslySetInnerHTML={{__html:this.state.Html1}}></div>

                <div className="layui-tab">
                    <ul className="layui-tab-title">
                        <li className="layui-this">网站设置</li>
                        <li>用户管理</li>
                        <li>权限分配</li>
                        <li>商品管理</li>
                        <li>订单管理</li>
                    </ul>
                    <div className="layui-tab-content">
                        <div className="layui-tab-item layui-show">
                        </div>
                        <div className="layui-tab-item">内容2</div>
                        <div className="layui-tab-item">内容3</div>
                        <div className="layui-tab-item">内容4</div>
                        <div className="layui-tab-item">内容5</div>
                    </div>
                </div>

                <button onClick={()=>{
                    /* global layer */
                    // @ts-ignore
                    layer.msg('hello');
                }}>click me!</button>

                <script>
                    layer.msg('hello');
                </script>
            </div>
        );
    }
}

export default Test;




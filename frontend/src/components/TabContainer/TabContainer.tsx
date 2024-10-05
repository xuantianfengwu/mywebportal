import React, {Component} from "react";
import {Divider} from "antd";

import './TabContainer.css';

interface Itab {
    id: number
    tabName: string
    tabCont: any
}

interface ITabContainerProps {
    tabs: Itab[]
    curr_index?: number
}

export default class TabContainer extends Component <ITabContainerProps, any> {
    state = {
        currentIndex: this.props.curr_index?this.props.curr_index:1,
    }

    componentDidMount() {

    }

    tabChoiced=(id:number)=>{
        //tab切换到方法
        this.setState({
            currentIndex:id
        });
    }

    generateTabContent = (id:number) => {
        let currentContent = this.props.tabs.map(
                (tabinfo)=>{
                    let display_style = tabinfo.id===id?'block':'none';
                    return (
                        <div className={'TabContent-Item'} style={{'display':display_style}}>
                            {tabinfo.tabCont}
                        </div>
                    )
                }
            )
        return currentContent
    }

    generateTabList = (curr_index: number) => {
        let tabList = this.props.tabs.map(
            (tabinfo: { id: any; tabName: any;}, index:number) => {
                // 遍历标签页，如果标签的id等于tabid，那么该标签就加多一个active的className
                var tabStyle=tabinfo.id==curr_index ? 'TabList-Item active' : 'TabList-Item';
                return <div key={index}
                           onClick={this.tabChoiced.bind(this, tabinfo.id)}
                           className={tabStyle}>
                           {tabinfo.tabName}
                       </div>
        });
        return tabList
    }

    render() {
        const curr_index = this.state.currentIndex;
        const tabList= this.generateTabList(curr_index);
        const tabCont = this.generateTabContent(curr_index);
        return (
            <div className="TabContainer">
                <div className="TabList">
                    {tabList}
                </div>
                <Divider/>
                <div className="TabContent">
                    <div>
                        {tabCont}
                    </div>
                </div>
            </div>
        )
    }
}

import React, {Component} from "react";
import {getFundamentalEventData} from "../../../api/cloudhands";
import {message} from "antd";

interface IFundamentalEvent {
    title: string
    content: string
}
export interface IFundamentalEventBackend {
    Item: string
    Content: string
}

class FundamentalEventSummary extends Component<any, any> {
    state = {
        fundamental_events: [
                {title:'', content: ''},
                {title:'', content: ''},
                {title:'', content: ''}
            ]
    }

    componentDidMount () {
    	// 调用父组件方法把当前实例传给父组件
        this.props.onRef('FundamentalEventSummary', this);
    }

    generateEventEditPanels = (events: IFundamentalEvent[]) => {
        const event_panels = events.map((e,i)=>{
            return (
                <div className={'input_area'}>
                    <input
                        name ={i.toString()}
                        value={e.title}
                        className={'event_title left'}
                        placeholder={'标题'+i}
                        onChange={this.handle_EventTitle_onChange}
                    >
                    </input>
                    <textarea
                        name ={i.toString()}
                        className={'event_content right'}
                        placeholder={'内容'+i}
                        onChange={this.handle_EventContent_onChange}
                        value = {e.content}
                    >
                    </textarea>
                </div>
            )
        })
        return event_panels;
    }

    handle_EventTitle_onChange = (e:any)=> {
        let { fundamental_events } = this.state;
        const i = e.currentTarget.name;
        fundamental_events[i].title = e.currentTarget.value;
        //console.log(fundamental_events);
        this.setState({fundamental_events: fundamental_events});
    }

    handle_EventContent_onChange = (e:any)=> {
        let { fundamental_events } = this.state;
        const i = e.currentTarget.name;
        fundamental_events[i].content = e.currentTarget.value;
        //console.log(fundamental_events);
        this.setState({fundamental_events: fundamental_events});
    }

    render_EventTitleContent():void {
        console.log('FundamentalEventSummary => render_EventTitleContent()');
        // 调用api获取已经爬取好的数据，进行渲染
        getFundamentalEventData(this.props.week_start).then((response)=>{
            if (response.data.code ==200) {
                message.success(response.data.message);
                // 从data_lst中选取前三个符合条件的item，生成新的 fundamental_events
                let { fundamental_events } = this.state;
                console.log(fundamental_events);
                const data_lst = response.data.data.data_lst;
                let i = 0;
                data_lst.map((elem: IFundamentalEventBackend, n:number)=>{
                    if(elem.Item!=='title' && elem.Item!=='summary' && i<3) {
                        fundamental_events[i].title = elem.Item;
                        fundamental_events[i].content = elem.Content;
                        i++;
                    }
                })
                this.setState({fundamental_events: fundamental_events});
            }
            else {
                message.warn(response.data.message);
            }
        });
    }

    render() {
        const { fundamental_events } = this.state;
        return (
            <>
                {this.generateEventEditPanels(fundamental_events)}
            </>
        )
    }
}

export default FundamentalEventSummary;
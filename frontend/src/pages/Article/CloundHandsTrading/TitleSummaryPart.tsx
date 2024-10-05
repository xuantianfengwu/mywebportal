import React, {Component} from 'react';
import {getFundamentalEventData} from "../../../api/cloudhands";
import {message} from "antd";
import {IFundamentalEventBackend} from "./FundamentalEventSummary";

class TitleSummaryPart extends Component<any, any> {
    state = {
        report_title: '',
        report_summary: ''
    }

    componentDidMount () {
    	// 调用父组件方法把当前实例传给父组件
        this.props.onRef('TitleSummaryPart', this);
    }

    generateReportTitle = (report_title: string) => {
        return <input placeholder={'周报标题'}
                      value={report_title}
                      id = 'report_title'
                      onChange={this.handleTitleSummaryonChange}
            >
            </input>
    }

    generateReportSummary = (report_summary: string) => {
        return <textarea placeholder={'周报摘要'}
                         value={report_summary}
                         id = 'report_summary'
                         onChange={this.handleTitleSummaryonChange}
                >
                </textarea>
    }

    handleTitleSummaryonChange = (e: any) => {
        //console.log('handleTitleSummaryonChange', e.currentTarget.value);
        const btn_id = e.currentTarget.id;
        const value = e.currentTarget.value;
        this.setState({
            [btn_id] : value
        })
    }

    render_TitleSummary():void {
        console.log('TitleSummaryPart => render_TitleSummary()');
        // 调用api获取已经爬取好的数据，进行渲染
        getFundamentalEventData(this.props.week_start).then((response)=>{
            if (response.data.code ==200) {
                message.success(response.data.message);
                // 从data_lst中选取 title 和 summary，更新state
                let OldState = this.state;
                const data_lst = response.data.data.data_lst;
                data_lst.map((elem: IFundamentalEventBackend, n:number)=>{
                    if(elem.Item==='title') {
                        OldState.report_title = elem.Content;
                    } else if(elem.Item==='summary') {
                        OldState.report_summary = elem.Content;
                    }
                })
                this.setState(OldState);
            }
            else {
                message.warn(response.data.message);
            }
        });
    }

    render() {
        const { report_title, report_summary } = this.state;
        return (
            <>
                {this.generateReportTitle(report_title)}
                {this.generateReportSummary(report_summary)}
            </>
        )
    }
}

export default TitleSummaryPart;
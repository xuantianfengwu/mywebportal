import React, {Component} from "react";

import {Image, message, Table} from 'antd';
import { getForexFutureDataEvent } from "../../../api/cloudhands";

class FutureDataEvent extends Component<any, any> {
    state = {
        data_table_cols :  [
            {title: '日期',    dataIndex: 'date', key: 'date',},
            {title: '时间',    dataIndex: 'time', key: 'time',},
            {title: '国家',    dataIndex: 'country', key: 'country',},
            {title: '数据区间', dataIndex: 'time_period', key: 'time_period',},
            {title: '数据类型', dataIndex: 'name', key: 'name',},
       ],
        data_table_values: [],
        data_image_src: '',

        event_table_cols:  [
            {title: '日期',    dataIndex: 'date', key: 'date',},
            {title: '时间',    dataIndex: 'time', key: 'time',},
            {title: '国家',    dataIndex: 'country', key: 'country',},
            {title: '人物',    dataIndex: 'people', key: 'people',},
            {title: '事件内容', dataIndex: 'event_content', key: 'event_content',},
        ],
        event_table_values:[],
        event_image_src: '',
    }

    componentDidMount () {
    	// 调用父组件方法把当前实例传给父组件
        this.props.onRef('FutureDataEvent', this);
    }

    render_ForexFutureDataEvent(): void {
        console.log('render_ForexFutureDataEvent');
        getForexFutureDataEvent(this.props.week_start, 'DATA').then((response)=>{
            if (response.data.code==200) {
                message.success(response.data.message);
                this.setState({
                    data_table_values: response.data.data.data_json_lst,
                    data_image_src: response.data.data.image_name,
                });
            }
        });
        getForexFutureDataEvent(this.props.week_start, 'EVENT').then((response)=>{
            if (response.data.code ==200) {
                message.success(response.data.message);
                this.setState({
                    event_table_values: response.data.data.data_json_lst,
                    event_image_src: response.data.data.image_name,
                });
            }
        });
    }

    generateDataTable = (columns:any, dataSource:any) => {
        return <Table
            columns={columns}
            dataSource={dataSource}
            size={'small'}
            pagination={false}
        />
    }

    generateEventTable = (columns:any, dataSource:any) => {
        return <Table
            columns={columns}
            dataSource={dataSource}
            size={'small'}
            pagination={false}
            />
    }

    generateDataPicture = (data_image_src: string) => {
        const t = Date.parse(new Date().toString());
        const image = <Image
                            width={'100%'}
                            height={200}
                            src={data_image_src==''?'':'http://localhost/api/trading/cloudhands/file?week_start='+this.props.week_start+'&file_name='+data_image_src+'&t='+t}
                            placeholder={true}
                       />
        return image
    }

    generateEventPicture = (event_image_src: string) => {
        const t = Date.parse(new Date().toString());
        const image = <Image
                            width={'100%'}
                            height={200}
                            src={event_image_src==''?'':'http://localhost/api/trading/cloudhands/file?week_start='+this.props.week_start+'&file_name='+event_image_src+'&t='+t}
                            placeholder={true}
                       />
        return image
    }

    render() {
        const { data_table_cols, data_table_values, event_table_cols, event_table_values,
                data_image_src, event_image_src } = this.state;
        //{this.generateDataTable(data_table_cols, data_table_values)}
        //{this.generateEventTable(event_table_cols, event_table_values)}
        return (
            <>
                <div style={{width:'50%', 'display': 'inline-block'}}>
                    <div>财经数据:</div>
                    {this.generateDataPicture(data_image_src)}
                </div>
                <div style={{width:'50%', 'display': 'inline-block'}}>
                    <div>财经事件:</div>
                    {this.generateEventPicture(event_image_src)}
                </div>
            </>
        )
    }
}

export default FutureDataEvent;

import React, {Component} from "react";

import {Image, Button, message} from "antd";
import { DownloadOutlined } from '@ant-design/icons';
import { getForexPositionData } from "../../../api/cloudhands";

class ForexPositionSummary extends Component<any, any> {
    state = {
        position_summary_data: {
            data_lst:     [],
            picture_name: '',
            text: ''
        },
    }

    componentDidMount () {
    	// 调用父组件方法把当前实例传给父组件
        this.props.onRef('ForexPositionSummary', this);
    }

    render_ForexPositionData(): void {
        console.log('render_ForexPositionData');
        getForexPositionData(this.props.week_start).then((response)=>{
            if (response.data.code ==200) {
                message.success(response.data.message);
                const data = response.data.data;
                //console.log(data);
                this.setState({position_summary_data: data});
            }
            else {
                message.warn(response.data.message);
            }
        })
    }

    generatePicture = (image_name: string) => {
        const t = Date.parse(new Date().toString());
        return  <Image
                    width={400}
                    height={200}
                    //src={image_src}
                    src={image_name==''?'':'http://localhost/api/trading/cloudhands/file?week_start='+this.props.week_start+'&file_name='+image_name+'&t='+t}
                    placeholder={true}
                />
    }

    generateText = (text: string) => {
        return text
    }

    generateFileDownloadBtn = () => {
        return <Button type="primary"
                       shape="circle"
                       icon={<DownloadOutlined />}
                       size={'small'} />
    }

    render() {
        const { position_summary_data } = this.state;
        const { data_lst, picture_name, text } = position_summary_data;
        return (
            <>
                <div className={'picture left'} >
                    {this.generatePicture(picture_name)}
                </div>
                <div className={'text center'} >
                    {this.generateText(text)}
                </div>
                <div className={'file right'} >
                    {this.generateFileDownloadBtn()}
                </div>
            </>
        )
    }
}

export default ForexPositionSummary;
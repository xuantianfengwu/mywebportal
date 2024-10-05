import React, {Component} from 'react';
import { Button, message } from "antd";
import { DownloadOutlined } from "@ant-design/icons";
import { getFile } from "../../../api/cloudhands";

class ResultArea extends Component<any, any> {

    handleDownloadBtnonClick = (e: any) => {
        const btn_name =  e.currentTarget.name
        getFile(this.props.week_start, btn_name).then((response)=>{
            const data = response.data;
            if (typeof data == 'object'){
                message.warn(response.data.message);
            }
            else {
                // 浏览器预览
                let url = (response.request.responseURL);
                window.open(url);
            }
        })
    }

    generateDownloadBtns = () => {
        return <>
            <div>
                <Button key = {'docx-jt'} value={'docx-jt'} name='docx-jt'
                        size={'small'} type="primary" shape="round"
                        icon={<DownloadOutlined />}
                        onClick={this.handleDownloadBtnonClick}>
                    （简体）CME版本 云核变量策略周报.docx
               </Button>
            </div>
            <div>
                <Button key = {'docx-ft'} value={'docx-ft'} name='docx-ft'
                        size={'small'} type="primary" shape="round"
                        icon={<DownloadOutlined />}
                        onClick={this.handleDownloadBtnonClick}>
                    （繁体）CME版本 云核变量策略周报.docx
               </Button>
            </div>
            <div>
                <Button key = {'pdf-jt'} value={'pdf-jt'} name='pdf-jt'
                        size={'small'} type="primary" shape="round"
                        icon={<DownloadOutlined />}
                        onClick={this.handleDownloadBtnonClick}>
                    （简体）CME版本 云核变量策略周报.pdf
               </Button>
            </div>
            <div>
                <Button key = {'pdf-ft'} value={'pdf-ft'} name='pdf-ft'
                        size={'small'} type="primary" shape="round"
                        icon={<DownloadOutlined />}
                        onClick={this.handleDownloadBtnonClick}>
                    （繁体）CME版本 云核变量策略周报.pdf
               </Button>
            </div>
        </>
    }

    render() {
        return (
            <div className={'result_area'}>
                生成结果：
                {this.generateDownloadBtns()}
            </div>
        );
    }
}

export default ResultArea;
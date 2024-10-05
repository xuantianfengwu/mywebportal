import React, {Component} from "react";
import "./PictureTools.css"

import { Upload, message, Input, Button, Radio } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import { getPictureLetterRecRes } from "../../../api/picturetools"

const { Dragger } = Upload;
const { TextArea } = Input;

export default class PictureLetterRecTool extends Component<any, any> {
    state = {
        upload_file: '',
        model_type: '',
        rec_result: ''
    }

    PictureUploadArea_onUpload = (upload_file: string) => {
        this.setState({
            upload_file: upload_file,
        })
    }

    SubmitArea_onClick = (e: any) => {
        if(this.state.model_type=='' || this.state.upload_file=='') {
            message.warn('upload_file, model_type, rec_result存在空值，无法提交服务端');
        }
        else {
            const file_name = this.state.upload_file;
            const model_type = this.state.model_type;
            getPictureLetterRecRes(file_name, model_type).then((response)=>{
                if(response.data.code==200){
                    this.setState({
                        rec_result: response.data.data.rec_text,
                    })
                }
                else {
                    message.warn(response.data.message);
                }
            })
        }
    }

    ParamSelectionArea_onChange = (e: any) => {
        this.setState({
            model_type: e.target.value
        })
    }

    render() {
        return (
            <div className={'letter_rec_tool'}>
                <div className={'upload_area'}>
                    这里是Picture上传区域
                    <PictureUploadArea
                        onUpload ={this.PictureUploadArea_onUpload}
                    />
                </div>
                <div className={'display_area'}>
                    这里是文件比对结果展示区，可以直接粘贴文字出来
                    <RecResultDisplayArea
                        rec_result = {this.state.rec_result}
                    />
                </div>
                <div className={'option_area'}>
                    <p>这里是参数配置区，选择需要转换所使用的如 模型类型 等</p>
                    <ParamSelectionArea
                        onChange = {this.ParamSelectionArea_onChange}
                    />
                </div>
                <div className={'submit_area'}>
                    <SubmitArea
                        onClick = {this.SubmitArea_onClick}
                    />
                </div>
                {this.state.upload_file}
                {this.state.model_type}
            </div>
        )
    }
}

class PictureUploadArea extends Component<any, any> {
    render() {
        const {onUpload} = this.props;
        const upload_props = {
            name: 'file',
            multiple: false,
            maxCount: 1,
            action: process.env.REACT_APP_URL + '/upload/picturetools/picture',
            accept: '.jpg,.png',
            headers: {
                from: 'PictureLetterRecTool',
            },
            onChange(info:any) {
                const { status } = info.file;
                if (status !== 'uploading') {
                    console.log(info.file, info.fileList);
                }
                if (status === 'done') {
                    message.success(`${info.file.name} file uploaded successfully.`);
                    onUpload(`PictureLetterRecTool_${info.file.name}`);
                }
                else if (status === 'error') {
                    message.error(`${info.file.name} file upload failed.`);
                    onUpload(``);
                }
            },
            onDrop(e: any) {
                console.log('Dropped files', e.dataTransfer.files);
            },
        };

        return (
            <Dragger {...upload_props}>
                <p className="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p className="ant-upload-text">请上传或拖入图片</p>
                <p className="ant-upload-hint">
                   只能对1张图片进行识别，多次上传会覆盖
                </p>
          </Dragger>
        )
    }
}

class ParamSelectionArea extends Component<any, any> {
    onChange = (e: any) => {
        console.log('radio checked', e.target.value);
        this.props.onChange(e);
    };

    render() {
        return (
            <Radio.Group onChange={this.onChange}>
                <Radio value={'baidu'}>百度</Radio>
                <Radio value={'kdxf'}>科大讯飞</Radio>
                <Radio value={'ali'}>阿里</Radio>
            </Radio.Group>
        )
    }
}

class RecResultDisplayArea extends Component<any, any> {
    status = {

    }

    render() {
        const {rec_result} = this.props;

        return (
            <TextArea
              placeholder="请选择模型并点击”一键识别“"
              autoSize={{ minRows: 10, maxRows:10}}
              value = {rec_result}
            />
        )
    }
}

class SubmitArea extends Component<any, any> {
    onClick = (e: any) => {
        console.log('PictureLetterRecTool - Picture Submit!');
        this.props.onClick(e);
    }

    render() {
        return (
            <Button type={'primary'} onClick={this.onClick}>一键识别</Button>
        )
    }
}
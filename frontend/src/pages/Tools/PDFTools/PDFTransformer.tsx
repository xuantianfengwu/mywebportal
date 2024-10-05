import React, {Component, ReactDOM} from "react";

import {Space, Radio, Input, Upload, Button, message} from 'antd';
import { UploadOutlined, DownloadOutlined } from '@ant-design/icons';

import "./PDFTransformer.css"
import { PDFDelSpecificPage, PreviewPDFRes, DownloadPDFRes } from "../../../api/pdftools";

interface IoperateRes {
    is_success: boolean
    operate_type: string
    operate_files: string[]
}

class PDFTransformer extends Component<any, any> {
    state = {
        operate_type: 1,             // 选择的转换类型
        operate_params: {},          // 选择的转换类型的相关参数

        upload_pdfList: [],          // 已完成上传的pdf_files

        is_succ_submit:  false,      // 是否已经提交操作
        result_files:   []
    }

    handle_OptionArea_onClick = (operate_type:number) => {
        this.setState({
            operate_type: operate_type,
            is_succ_submit: false,
        });
    }

    handle_OptionArea_onInput = (operate_params: any) => {
        this.setState({operate_params: operate_params});
    }

    handle_UploadArea_onUpload = (filelist: any[]) => {
        this.setState({upload_pdfList: filelist});
    }

    handle_SubmitArea_onSubmit = (oper_res: IoperateRes) => {
        console.log('handle_SubmitArea_onSubmit', oper_res);
        console.log(oper_res['is_success'])
        if(oper_res['is_success']){
            console.log(oper_res['is_success'])
            this.setState({
                is_succ_submit: true,
                result_files: oper_res['operate_files']
            })
        }
        else {
            this.setState({is_succ_submit: false,})
        }
    }

    render() {
        const {is_succ_submit} = this.state;
        return(
            <div className={'PDFTransformer'}>
                <OptionArea
                    handle_OptionArea_onClick = {this.handle_OptionArea_onClick}
                    handle_OptionArea_onInput = {this.handle_OptionArea_onInput}
                />

                <UploadArea
                    handle_UploadArea_onUpload = {this.handle_UploadArea_onUpload}
                />

                <SubmitArea
                    operate_type ={this.state.operate_type}
                    upload_pdfList = {this.state.upload_pdfList}
                    operate_params = {this.state.operate_params}
                    handle_SubmitArea_onSubmit = {this.handle_SubmitArea_onSubmit}
                />

                <ResultArea
                    upload_pdfList = {this.state.upload_pdfList}
                    is_succ_submit = {this.state.is_succ_submit}
                    operate_type = {this.state.operate_type}
                    result_files = {this.state.result_files}
                />
            </div>
        )
    }
}

class OptionArea extends Component<any, any> {
    state = {
        operate_type: 1, // PDF批量删除页码
        operate_params: {}
    }

    handleOperateTypeonChange = (e:any) => {
        this.setState({
            operate_type: e.target.value
        })
        this.props.handle_OptionArea_onClick(e.target.value)
    }

    handleInputonChange = (e:any) => {
        const operate_type = e.currentTarget.name;
        if (operate_type=='1'){
            const operate_params = {
                'to_del_page': e.currentTarget.value,
            }
            this.setState({operate_params: operate_params})
            this.props.handle_OptionArea_onInput(operate_params)
        }

    }

    generateOperateTypeRadioGroup = () => {
        const operate_type = this.state.operate_type;
        return(
            <Radio.Group onChange={this.handleOperateTypeonChange} value={operate_type}>
                <Space direction={'vertical'}>
                  <Radio value={1}>PDF批量删除页码
                    {operate_type === 1 ?
                        <Input name='1'
                               placeholder={'请输入需要删除的页码，多个页码以/分割'}
                               onChange = {this.handleInputonChange}
                        />
                        : null
                    }
                  </Radio>
                  <Radio value={2}>More...
                    {operate_type === 2 ?
                        <Input style={{ width: 100, marginLeft: 10 }} />
                        : null}
                  </Radio>
                </Space>
            </Radio.Group>
            )
    }

    render() {
        return (
            <div className={'option_area'}>
                <p>选择转换类型:</p>
                {this.generateOperateTypeRadioGroup()}
            </div>
        )
    }
}

class UploadArea extends Component<any, any> {
    state = {
        upload_fileList: [],
    }

    generateUploadBtn = () => {
        const props = {     name: 'file',
                            action: process.env.REACT_APP_URL+'/upload/pdf/transformer',
                            maxCount: 10,
                            accept: '.pdf',
                            multiple: true,
                            headers: {
                                authorization: 'authorization-text',
                            },
                    };
        return <Upload {...props}
                    onChange = {this.handleUploadBtnonChange}
                    beforeUpload = {this.handleUploadBtnbeforeUpload}
                >
                    <Button icon={<UploadOutlined />}>Click to Upload（Max:10）</Button>
               </Upload>
    }

        handleUploadBtnonChange = (info:any) => {
            if (info.file.status !== 'uploading') {
                this.setState({
                    'upload_fileList': info.fileList
                })
            }
            if (info.file.status === 'done') {
                message.success(`${info.file.name} file uploaded successfully`);
                this.props.handle_UploadArea_onUpload(info.fileList);
            } else if (info.file.status === 'error') {
                message.error(`${info.file.name} file upload failed.`);
            }
        }

        handleUploadBtnbeforeUpload = (file:any, fileList:any) => {
            if (file.type !== 'application/pdf') {
                message.error(`${file.name} 不是一个 PDF 文件`);
                return Upload.LIST_IGNORE;
            }
            const uploaded_files = this.state.upload_fileList.map((f:any)=>{return f.name});
            if (uploaded_files.indexOf(file.name)>-1) {
                message.error(`${file.name} 已有同名文件，请勿重复上传`);
                return Upload.LIST_IGNORE;
            }
            return true;
        }

    render() {
        return (
            <div className={'upload_area'}>
                {this.generateUploadBtn()}
            </div>
        )
    }
}

class SubmitArea extends Component<any, any> {
     generateSubmitBtn = (operate_type: number, upload_pdfList: any[]) => {
         const file_amt = upload_pdfList.length;
         const SubmitBtn = (
            file_amt > 0 ?
                <p>
                    <Button type={'primary'}
                            onClick={this.handleSubmitBtnonClick}
                            value={operate_type}
                    >一键处理
                    </Button>
                    待转换的{file_amt}个文件
                </p>
                :
                <p>请上传待转换PDF（最多10个文件）</p>
        )
        return SubmitBtn;
    }

        handleSubmitBtnonClick = (e: any) => {
            const operate_type = e.currentTarget.value;
            if(operate_type==1){
                console.log(this.props.upload_pdfList);
                const {upload_pdfList, operate_params} = this.props;
                if (operate_params['to_del_page']==undefined || operate_params['to_del_page'].length==0){
                    message.warn('请先补全转换参数再进行处理~');
                }
                else {
                    PDFDelSpecificPage(upload_pdfList, operate_params).then((response)=>{
                        if(response.data.code==200) {
                            message.success(response.data.message);
                            this.props.handle_SubmitArea_onSubmit(response.data.data.operate_res);
                        }
                        else {message.warn(response.data.message);}
                    })
                }
            }
        }

    render() {
        return (
            <div className={'submit_area'}>
                {this.generateSubmitBtn(this.props.operate_type, this.props.upload_pdfList)}
            </div>
        )
    }
}

class ResultArea extends Component<any, any> {
    generateDownloadBtn = (is_succ_submit: boolean, result_files: string[]) => {
        const PreviewBtns = <div className={'PreviewBtns'}>
                                <div>文件预览：</div>
                                {result_files.map((res_f)=>{
                                    return <Button key = {res_f} value={res_f}
                                                   name='preview' size={'small'}
                                                   type="primary" shape="round" icon={<DownloadOutlined />}
                                                   onClick={this.handleDownloadBtnonClick}>
                                            {res_f}
                                           </Button>
                                })}
                            </div>
        const DownloadBtns = <div className={'DownloadBtns'}>
                                <div>文件下载：</div>
                                <Button key='download_all' name='download_all' size='middle'
                                        onClick={this.handleDownloadBtnonClick}>
                                    打包下载全部文件
                                </Button>
                            </div>
        return (
            is_succ_submit ?
                    <>
                        {PreviewBtns}
                        {DownloadBtns}
                    </>
                :
                    <></>
        )
    }

    handleDownloadBtnonClick = (e: any) => {
        const { operate_type, result_files } = this.props;
        const btn_name = e.currentTarget.name;
        console.log('Click Btn:', btn_name);
        if(btn_name=='preview'){
            const prev_file = e.currentTarget.value;
            console.log('Preview File Name:', prev_file);
            PreviewPDFRes(operate_type, prev_file).then((response)=>{
                // 浏览器预览逻辑
                let url = (response.request.responseURL);
                window.open(url);
            });
        }
        else if(btn_name=='download_all'){
            const download_type = 'zip';
            DownloadPDFRes(operate_type, download_type, result_files).then((response)=> {
                console.log(response);
                if (response.data.code==undefined || response.data.code==200) {
                    // 下载逻辑
                    // const { download_f, download_f_name, download_f_type } = response.data.data;
                    // console.log(download_f);
                    // console.log(download_f_name);
                    // console.log(download_f_type);
                    const download_f = response.data;
                    const download_f_name = operate_type+'.'+download_type;
                    const download_f_type = 'application/zip';
                    let url = window.URL.createObjectURL(new Blob([download_f],
                                                                    {type: download_f_type}));
                    let aElem = document.createElement('a');
                    aElem.href = url;
                    aElem.download = download_f_name;
                    aElem.click();
                    window.URL.revokeObjectURL(url);
                }
                else {
                    message.warn(response.data.message);
                }
            })
        }
    }

    render() {
        const { is_succ_submit, result_files } = this.props;
        return (
            <div className={'result_area'}>
                {this.generateDownloadBtn(is_succ_submit, result_files)}
            </div>

        )
    }
}

export default PDFTransformer;
import React, {Component} from 'react';
import { Radio, message } from 'antd';

import { initializeDB, importUploadFile } from "../../../api/trading";

class DataImport extends Component {
    state = {
         upload_file: '',
         upload_file_type: ''
    }

    generateInitializeBtn = () => {
        return <button onClick={this.handleInitializeBtnonClick}>初始化数据库</button>
    }

        handleInitializeBtnonClick = () => {
            initializeDB().then((response)=>{
                if (response.data.code==200){
                    message.success(response.data.message);
                }
                else {
                    console.log(response.data.message);
                    message.warn(response.data.message);
                }
            })
        }

    generateUploadBtn = () => {
        const UploadBtn =
            <input type = "file"
                   id = "forex_tester"
                   accept = ".txt"
                   onChange={this.handleUploadBtnonChange}
                >
            </input>
        return UploadBtn
    }

        handleUploadBtnonChange= (e:any) => {
            console.log('handleUploadBtnonChange');
            const filelist = e.currentTarget.files;
            if(filelist.length>0){
                const upload_file = filelist[0];
                console.log(upload_file);
                this.setState({
                    upload_file: upload_file,
                })
            }
        }

    generateRadioGroup = () => {
        const options = [
              { label: 'Forex Tester', value: 'forex_tester' },
            ];
        const RadioGroup = (
            <Radio.Group
              options={options}
              onChange={this.handleRadioGrouponChange}
              value={this.state.upload_file_type}
            />
        )
        return RadioGroup
    }

        handleRadioGrouponChange = (e:any) =>{
            this.setState({
                upload_file_type: e.target.value
            })
        }

    generateSubmitBtn = () => {
        return <button onClick={this.handleSubmitBtnonClick}>
            导入数据库
        </button>
    }

        handleSubmitBtnonClick= () => {
            console.log('handleSubmitBtnonClick');
            const { upload_file, upload_file_type } = this.state;
            importUploadFile(upload_file, upload_file_type).then((response)=>{
                if (response.data.code==200){
                    message.success(response.data.message);
                }
                else {
                    console.log(response.data.message);
                    message.warn(response.data.message);
                }
            })
        }

    render() {
        return (
            <div className={'DataImport'}>
                <div>
                    <h4>数据初始化</h4>
                    {this.generateInitializeBtn()}
                </div>
                <br/>
                <div>
                    <h4>历史数据上传</h4>
                    <div>
                        {this.generateUploadBtn()}
                        {this.generateRadioGroup()}
                    </div>
                    {this.generateSubmitBtn()}
                </div>
                <br/>
                <div>
                    <h4>缺失数据填充</h4>
                </div>
                <div>
                    <h4>高周期数据生成</h4>
                </div>
            </div>
        );
    }
}

export default DataImport;
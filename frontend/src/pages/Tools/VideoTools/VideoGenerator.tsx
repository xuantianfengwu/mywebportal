import React, {Component} from 'react';
import { Input, Radio } from 'antd';

const { TextArea } = Input;

class VideoGenerator extends Component {
    state = {
        textaudio_sources : [
            {label: 'baidu', value: 'baidu'},
        ],
        pic_sources : [
            {label: 'colorhub', value: 'colorhub'}
        ]
    }

    render() {
        return (
            <div>
                <p>原始文本</p>
                <div style={{maxWidth: '30em'}}>
                    <TextArea
                        autoSize={{ minRows: 5, maxRows: 15 }}
                        showCount
                    />
                </div>

                <p>文本配音来源</p>
                <Radio.Group
                    options={this.state.textaudio_sources}
                    optionType="button"
                />

                <p>配图来源</p>
                <Radio.Group
                    options={this.state.pic_sources}
                    optionType='button'
                />

                <hr/>
                <p><button>一键下载</button></p>
                <p><button>一键生成</button></p>
                <p>视频下载</p>
            </div>
        );
    }
}

export default VideoGenerator;
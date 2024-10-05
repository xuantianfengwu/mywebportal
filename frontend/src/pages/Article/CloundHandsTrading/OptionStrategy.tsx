import React, {Component} from 'react';
import { Input, Image } from "antd";

class OptionStrategy extends Component<any, any> {
    state = {
        strategy_info: {
            strategy_title: '',
            strategy_content: '',
            strategy_img_src: '',
        },
    }

    componentDidMount () {
    	// 调用父组件方法把当前实例传给父组件
        this.props.onRef('OptionStrategy', this);
    }

    generateStrategy = (strategy_info: any) => {
        const title_input = <Input
            id = 'strategy_title'
            value={strategy_info.strategy_title}
            onChange = {this.handleStrategyonChange}
            placeholder = '策略名称'
        />
        const content_textarea = <Input.TextArea
            id = 'strategy_content'
            value={strategy_info.strategy_content}
            onChange = {this.handleStrategyonChange}
            placeholder = '策略具体内容'
        />
        return <>
            {title_input}
            {content_textarea}
        </>
    }

    handleStrategyonChange = (e: any) => {
        const btn_id = e.currentTarget.id;
        let new_strategy_info = this.state.strategy_info;
        (new_strategy_info as any)[btn_id] = e.currentTarget.value;
        this.setState({strategy_info: new_strategy_info})
    }

    generateStrategyPicture = (img_src: string) => {
        const t = Date.parse(new Date().toString());
        const image = <Image
                            width = {'100%'}
                            height={'100%'}
                            src={img_src==''?'':'http://localhost/api/trading/cloudhands/file?week_start='+this.props.week_start+'&file_name='+img_src+'&t='+t}
                            placeholder={true}
                       />
        return image;
    }

    render() {
        const { strategy_info } = this.state;
        return (
            <>
                <div className={'left'}>
                    {this.generateStrategy(strategy_info)}
                </div>
                <div className={'right'}>
                    {this.generateStrategyPicture(strategy_info.strategy_img_src)}
                </div>
            </>
        );
    }
}

export default OptionStrategy;
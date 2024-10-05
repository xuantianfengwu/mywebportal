import React, {Component} from "react";
import {message} from "antd";
import {getMajorCurrForecast} from "../../../api/cloudhands";

class MajorCurrencyForecast extends Component<any, any> {
    state = {
       curr_forecasts: [
                {name:'欧元/美元', forecast: ''},
                {name:'英镑/美元', forecast: ''},
                {name:'澳元/美元', forecast: ''},
                {name:'美元/日元', forecast: ''},
                //{name:'美元/加元', forecast: ''},
            ]
    }

    componentDidMount () {
    	// 调用父组件方法把当前实例传给父组件
        this.props.onRef('MajorCurrencyForecast', this);
    }

    generateInputArea = (curr_forecasts: any) => {
        const input_area = curr_forecasts.map((curr:any, i:number)=>{
            return (
                <div className={'input_area'}>
                    <label className={'left name'}>{curr.name}</label>
                    <textarea
                        className={'center forecast'}
                        id ={i.toString()}
                        onChange={this.handle_curr_forecast_onChange}
                        value = {curr.forecast}
                    >
                    </textarea>
                    <div className={'right picture'}></div>
                </div>
            )
        })
        return input_area;
    }

    handle_curr_forecast_onChange = (e:any) => {
        const btn_id = e.currentTarget.id;
        let new_curr_forecasts = this.state.curr_forecasts.map((curr, i)=>{
            if (i==btn_id){ // 正在修改的货币文本框
                const new_curr = {name: curr.name, forecast: e.currentTarget.value}
                return new_curr
            } else{ // 未修改的货币文本框
                return curr
            }
        })
        //console.log(new_curr_forecasts);
        this.setState({ curr_forecasts: new_curr_forecasts, })
    }

    render_CurrencyForecast() {
        console.log('render_CurrencyForecast');
        getMajorCurrForecast(this.props.week_start).then((response)=>{
            if (response.data.code ==200) {
                message.success(response.data.message);
                const data = response.data.data;
                console.log(data);
                // 根据获取到的analysis_dict，对state.curr_forecasts 重新赋值
                let new_curr_forecasts = this.state.curr_forecasts.map((curr, i)=>{
                    const new_curr = {name: curr.name, forecast: data.analysis_dict[curr.name]}
                    return new_curr
                })
                //console.log(new_curr_forecasts);
                this.setState({ curr_forecasts: new_curr_forecasts, })
            }
            else {
                message.warn(response.data.message);
            }
        })
    }

    render() {
        const { curr_forecasts } = this.state;
        return (
            <div>
                {this.generateInputArea(curr_forecasts)}
            </div>
        )
    }
}

export default MajorCurrencyForecast;

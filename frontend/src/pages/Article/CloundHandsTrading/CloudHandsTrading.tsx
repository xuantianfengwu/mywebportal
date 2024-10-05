import React, {Component} from 'react';
import "./CloudHandsTrading.css";

import TitleSummaryPart from "./TitleSummaryPart";
import FundamentalEventSummary from "./FundamentalEventSummary";
import ForexTrendSummary from "./ForexTrendSummary" ;
import ForexPositionSummary from "./ForexPositionSummary";
import MajorCurrencyForecast from './MajorCurrencyForecast';
import OptionStrategy from "./OptionStrategy";
import FutureDataEvent from "./FutureDataEvent";
import ResultArea from "./ResultArea";

import { crawlData } from "../../../api/cloudhands";
import { generateOutputReport } from "../../../api/cloudhands";

import { Select, message } from 'antd';

const { Option } = Select;

class CloudHandsTrading extends Component {
    state = {
        week_type: 'next_week',
        week_start: '',
        week_end: ''
    }

    // 获取子组件
    private TitleSummaryPart: any;
    private FundamentalEventSummary: any;
    private ForexTrendSummary: any;
    private ForexPositionSummary: any;
    private MajorCurrencyForecast: any;
    private OptionStrategy: any;
    private FutureDataEvent: any;
    onRef (name:string, ref:any) {
        switch (name) {
             case 'TitleSummaryPart':
                this.TitleSummaryPart = ref; break
            case 'FundamentalEventSummary':
                this.FundamentalEventSummary = ref; break
            case 'ForexTrendSummary':
                this.ForexTrendSummary = ref; break
            case 'ForexPositionSummary':
                this.ForexPositionSummary = ref; break
            case 'MajorCurrencyForecast':
                this.MajorCurrencyForecast =ref; break
            case 'OptionStrategy':
                this.OptionStrategy = ref; break
            case 'FutureDataEvent':
                this.FutureDataEvent = ref; break
           default: break
        }
    }

    componentDidMount(): void {
        this.getWeekDays(this.state.week_type);
    }

    getWeekDays = (week_type:string) => {
        var today = new Date();
        var today_weekday = today.getDay(); // 0-6，Sunday是0
        if(today_weekday==0) {today_weekday=7} // 1-7, Sunday是7
        // 生成 this_week, 或 next_week 的时间区间
        let WeekDays = new Array(7)
        if (week_type == 'this_week') {
            WeekDays = Array.from(new Array(7), function(val, index){
                const tmp_date = new Date(today.getTime() - (today_weekday-index-1) * 24 * 60 * 60 * 1000)
                return tmp_date.getFullYear() + '-' + (tmp_date.getMonth() + 1) + '-' + tmp_date.getDate()
            });
        } else if (week_type == 'next_week') {
            WeekDays = Array.from(new Array(7), function(val, index){
                const tmp_date = new Date(today.getTime() - (today_weekday-index-1-7) * 24 * 60 * 60 * 1000)
                return tmp_date.getFullYear() + '-' + (tmp_date.getMonth() + 1) + '-' + tmp_date.getDate()
            });
        }
        console.log(week_type, WeekDays);
        this.setState({
            week_start: WeekDays[0],
            week_end:  WeekDays[6],
        })
    };

    generateWeekPriodSelect = (week_type:string, week_start:string, week_end:string) => {
        const WeekPeriodH1 =
        <>  时间区间：
            <Select defaultValue={week_type}
                    style={{ width: 120, margin:'0 5px'}}
                    onChange={this.handleWeekPriodSelectonChange}
                    value = {week_type}
            >
              <Option value="next_week">下周</Option>
              <Option value="this_week">本周</Option>
            </Select>
            <span>{week_start} - {week_end}</span>
        </>
        return WeekPeriodH1;
    }

    handleWeekPriodSelectonChange = (value:string) => {
        this.setState({week_type: value});
        this.getWeekDays(value);
    }

    UpdateRender = (render_part:string) => {
        // 手动点击 【周报渲染】 按钮后的逻辑，根据render_part调用不同子组件中的函数
        console.log('render_part：', render_part);
        if (render_part == 'fundamental_event_summary') { this.FundamentalEventSummary.render_EventTitleContent();
                                                          this.TitleSummaryPart.render_TitleSummary();
                                                        }
        else if (render_part == 'forex_trend_summary') { this.ForexTrendSummary.render_ForexTrendSummary() }
        else if (render_part == 'forex_position_data') { this.ForexPositionSummary.render_ForexPositionData() }
        else if (render_part == 'major_currency_forecast') {this.MajorCurrencyForecast.render_CurrencyForecast() }
        else if (render_part == 'forex_future_data_event') { this.FutureDataEvent.render_ForexFutureDataEvent() }
    }

    handle_OutputReportBtn_onClick = () => {
        const { report_title, report_summary } = this.TitleSummaryPart.state;
        const { fundamental_events } = this.FundamentalEventSummary.state;
        const { trend_image_src } = this.ForexTrendSummary.state;
        const { position_summary_data } = this.ForexPositionSummary.state;
        const { curr_forecasts } = this.MajorCurrencyForecast.state;
        const { strategy_info } = this.OptionStrategy.state;
        const { data_image_src, event_image_src } = this.FutureDataEvent.state;

        generateOutputReport(this.state.week_start,
                             report_title, report_summary,
                             fundamental_events, trend_image_src,
                             position_summary_data, curr_forecasts,
                             strategy_info,
                             data_image_src, event_image_src).then((response)=>{
                                 if(response.data.code==200) {
                                     message.success(response.data.message);
                                 }
                                 else {
                                     message.warn(response.data.message);
                                 }
        })
    }

    render() {
        const { week_type, week_start, week_end } = this.state;
        return (
            <div>
                <div className={'operate_area'}>
                    <span className={'operate_btns'}>
                        <OperateBtnArea
                            UpdateRender ={this.UpdateRender}
                            handle_OutputReportBtn_onClick = {this.handle_OutputReportBtn_onClick}

                            week_type = {this.state.week_type}
                            week_start = {this.state.week_start}
                            week_end = {this.state.week_end}
                            handleWeekPriodSelectonChange = {this.handleWeekPriodSelectonChange}
                        />
                    </span>
                </div>
                    <div className={'intro_area'}>
                        <div>欢迎来到云核变量周报编辑页！</div>
                    </div>
                <hr/>
                    <div className={'edit_area'}>
                        <h1 className={'title L1'}>Part 0: 周报标题 & 周报摘要
                                <div className={'title_summary_part sub_edit_area'}>
                                    <TitleSummaryPart
                                        onRef={this.onRef.bind(this)}
                                        week_start = {this.state.week_start}
                                    />
                                </div>
                        </h1>
                        <h1 className={'title L1'}>Part I: 全球外汇焦点回顾与基本面摘要</h1>
                                <div className={'fundamental_event_summary sub_edit_area'}>
                                    <FundamentalEventSummary
                                        onRef={this.onRef.bind(this)}
                                        week_start = {this.state.week_start}
                                    />
                                </div>
                        <h1 className={'title L1'}>Part II: 外汇期货与期权走势分析</h1>
                            <h2 className={'title L2'}>2.1、重要外汇期货合约走势（图）</h2>
                                <div className={'forex_trend_summary sub_edit_area'}>
                                    <ForexTrendSummary
                                        onRef={this.onRef.bind(this)}
                                        week_start = {this.state.week_start}
                                    />
                                </div>
                            <h2 className={'title L2'}>2.2、期货市场头寸分析</h2>
                                <div className={'forex_position_summary sub_edit_area'}>
                                    <ForexPositionSummary
                                        onRef={this.onRef.bind(this)}
                                        week_start = {this.state.week_start}
                                    />
                                </div>
                            <h2 className={'title L2'}>2.3、重点货币对展望</h2>
                                <div className={'major_currency_forecast sub_edit_area'}>
                                    <MajorCurrencyForecast
                                        onRef={this.onRef.bind(this)}
                                        week_start = {this.state.week_start}
                                    />
                                </div>
                            <h2 className={'title L2'}>2.4、人民币套期保值案例</h2>
                                <div className={'option_strategy sub_edit_area'}>
                                    <OptionStrategy
                                        onRef={this.onRef.bind(this)}
                                    />
                                </div>
                        <h1 className={'title L1'}>Part III: 后市重要观察指标</h1>
                                <div className={'future_data_event sub_edit_area'}>
                                    <FutureDataEvent
                                        onRef={this.onRef.bind(this)}
                                        week_start = {this.state.week_start}
                                    />
                                </div>
                        <h1 className={'title L1'}>Part IV: 免责声明</h1>
                    </div>
                <hr/>
                    <ResultArea
                        week_start = {this.state.week_start}
                    />
            </div>
        );
    }
}

class OperateBtnArea extends Component<any, any> {
    state = {

    }

    handle_Update_Btn_onClick = (e: any) => {
        const btn_id = e.currentTarget.id;
        crawlData(this.props.week_start, btn_id).then((response)=>{
            if(response.data.code==200) {
                message.success(response.data.message);
                //this.props.UpdateRender(btn_id);
            }
            else {
                message.warn(response.data.message);
            }
        })
    }

    handle_Render_Btn_onClick = (e: any) => {
        const btn_id = e.currentTarget.id;
        this.props.UpdateRender(btn_id);
    }

    handle_Output_Btn_onClick = (e: any) => {
        this.props.handle_OutputReportBtn_onClick();
    }

    generateWeekPriodSelect = (week_type: string, week_start: string, week_end: string) => {
        const WeekPriodSelect =
        <>  时间区间：
            <Select defaultValue={week_type}
                    style={{ width: 120, margin:'0 5px'}}
                    onChange={this.props.handleWeekPriodSelectonChange}
                    value = {week_type}
            >
              <Option value="next_week">下周</Option>
              <Option value="this_week">本周</Option>
            </Select>
            <span>{week_start} - {week_end}</span>
        </>
        return WeekPriodSelect;
    }

    render() {
        const { week_type, week_start, week_end } = this.props;
        return (
            <>
                <div>
                    {this.generateWeekPriodSelect(week_type, week_start, week_end)}
                </div>
                <div>
                    数据爬取：
                    <button className={'operate_btn'}
                            id={'fundamental_event_summary'}
                            onClick={this.handle_Update_Btn_onClick}
                    >周报标题 & 基本面摘要</button>
                    <button className={'operate_btn'}
                            id={'forex_trend_summary'}
                            onClick={this.handle_Update_Btn_onClick}
                    >外汇期货合约走势</button>
                    <button className={'operate_btn'}
                            id={'forex_position_data'}
                            onClick={this.handle_Update_Btn_onClick}
                    >期货市场头寸分析</button>
                    <button className={'operate_btn'}
                            id={'major_currency_forecast'}
                            onClick={this.handle_Update_Btn_onClick}
                    >重点货币对展望</button>
                    <button className={'operate_btn'}
                            id={'option_strategy'}
                            onClick={this.handle_Update_Btn_onClick}
                    >人民币套期保值</button>
                    <button className={'operate_btn'}
                            id={'forex_future_data_event'}
                            onClick={this.handle_Update_Btn_onClick}
                    >后市观察指标</button>
                </div>
                <div>
                    周报渲染：
                    <button className={'operate_btn'}
                            id={'fundamental_event_summary'}
                            onClick={this.handle_Render_Btn_onClick}
                    >周报标题 & 基本面摘要</button>
                    <button className={'operate_btn'}
                            id={'forex_trend_summary'}
                            onClick={this.handle_Render_Btn_onClick}
                    >外汇期货合约走势</button>
                    <button className={'operate_btn'}
                            id={'forex_position_data'}
                            onClick={this.handle_Render_Btn_onClick}
                    >期货市场头寸分析</button>
                    <button className={'operate_btn'}
                            id={'major_currency_forecast'}
                            onClick={this.handle_Render_Btn_onClick}
                    >重点货币对展望</button>
                    <button className={'operate_btn'}
                            id={'option_strategy'}
                            onClick={this.handle_Render_Btn_onClick}
                    >人民币套期保值</button>
                    <button className={'operate_btn'}
                            id={'forex_future_data_event'}
                            onClick={this.handle_Render_Btn_onClick}
                    >后市观察指标</button>
                </div>
                <div> 周报生成：
                    <button className={'operate_btn'}
                        onClick = {this.handle_Output_Btn_onClick}
                    >一键生成</button>
                </div>
            </>
        )
    }
}

export default CloudHandsTrading;
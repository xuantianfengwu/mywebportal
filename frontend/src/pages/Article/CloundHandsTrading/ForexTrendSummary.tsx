import React, {Component} from "react";
import { Image, message } from "antd";
import { getForexTrendSummary } from "../../../api/cloudhands";

class ForexTrendSummary extends Component<any, any> {
    state = {
        columns: [
            '期货', '代码', '合约到期月', '最新价', '周变动', '月变动',
        ],
        data: [
            ['EUR', ],
            ['JPY', ],
            ['GBP', ],
            ['AUD', ],
            ['CAD', ],
            ['CHF', ],
            ['NZD', ],
            ['CNY', ],
        ],
        trend_image_src: '',
    }

    componentDidMount () {
    	// 调用父组件方法把当前实例传给父组件
        this.props.onRef('ForexTrendSummary', this);
    }

    render_ForexTrendSummary(): void {
        console.log('render_ForexTrendSummary');
        // 调用api获取已经爬取好的数据，进行渲染
        getForexTrendSummary(this.props.week_start).then((response)=>{
            if (response.data.code ==200) {
                message.success(response.data.message);
                this.setState({
                    trend_image_src: response.data.data.image_name,
                });
            }
            else {
                message.warn(response.data.message);
            }
        });
    }

    generateTrendTable = (columns: any, data: any) => {
        const thead = <tr>{
                columns.map((col: string)=>{
                return <th>{col}</th>
            })
        }</tr>
        const tbody = data.map((values: any)=>{
            const tds = values.map((v: string)=>{
                            return <td>{v}</td>
                        })
            return <tr>{tds}</tr>

        })
        const table = <table className={'forex_trend_summary'}>
                        <thead>
                            {thead}
                        </thead>
                        <tbody>
                            {tbody}
                        </tbody>
                    </table>
        return table;
    }

    generateTrendPicture = (trend_image_src: string) => {
        const t = Date.parse(new Date().toString());
        const image = <Image
                            width = {400}
                            height={200}
                            src={trend_image_src==''?'':'http://localhost/api/trading/cloudhands/file?week_start='+this.props.week_start+'&file_name='+trend_image_src+'&t='+t}
                            placeholder={true}
                       />
        return image
    }

    render() {
        const { columns, data, trend_image_src } = this.state;
        return (
            <div>
                {this.generateTrendPicture(trend_image_src)}
            </div>
        )
    }
}

export default ForexTrendSummary;
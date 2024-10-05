import React, { PureComponent } from 'react';

import ReactEcharts from 'echarts-for-react';
import echarts from 'echarts';

class ReactEChartsTest extends PureComponent {
    getOption = () => {
        return {
            title: {

            },
            tooltip: {},
            legend: {
                data:['销量']
            },
            xAxis: {
                data: ['衬衫', '羊毛衫', '雪纺纱', '裤子', '高跟鞋', '袜子']
            },
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                data: [5,20,36,10,10,20]
            }]
        }
    }

    render() {
        return (
            <ReactEcharts
                option={this.getOption()}
                notMerge={true}
                lazyUpdate={true}
            />
        )
    }
}

export default ReactEChartsTest;

import React, {Component} from 'react';
import {Statistic, Card} from 'antd';

const { Countdown } = Statistic;


class HomePgae extends Component {
    state = {
        cele_day : '2020-12-21 00:00:00',
        ms_from_cele_day: 0,
    }

    componentDidMount(): void {
        this.timeTransition();
    }

    timeTransition = () => {
        this.getStaticValue();
        setTimeout(this.timeTransition,1000);
    }

    getStaticValue() {
        // 1. 在一起到现在已经
        var oldDate = new Date(this.state.cele_day);
        var nowDate = new Date();
        //console.log(oldDate, nowDate);
        const ms_from_cele_day = nowDate.getTime()-oldDate.getTime();
        this.setState({ms_from_cele_day: ms_from_cele_day});
    };

    generateCountDown = (ms_from_cele_day: number) => {
        function formatDuring(mss: number) {
            var days = parseInt((mss / (1000 * 60 * 60 * 24)).toString());
            var hours = parseInt(((mss % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toString());
            var minutes = parseInt(((mss % (1000 * 60 * 60)) / (1000 * 60)).toString());
            var seconds = parseInt(((mss % (1000 * 60)) / 1000).toString());
            return days + " 天 " + hours + " 小时 " + minutes + " 分钟 " + seconds + " 秒 ";
        }
        const static_value = formatDuring(ms_from_cele_day);
        return (
            <>
                <Statistic
                    title="我们在一起已经"
                    value={static_value}
                    valueStyle={{color: '#3f8600'}}
                />
            </>
        );
    }

    render() {
        let ms_from_cele_day = this.state.ms_from_cele_day;
        return (
            <div>
                Welcome to Home!
                <div className={'statics'}>
                    <Card>
                        {this.generateCountDown(ms_from_cele_day)}
                    </Card>
                </div>
            </div>
        );
    }
}

export default HomePgae;
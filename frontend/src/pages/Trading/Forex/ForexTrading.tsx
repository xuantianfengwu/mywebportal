import React, {Component} from 'react';

import TabContainer from "../../../components/TabContainer/TabContainer";
import DataImport from "./DataImport";
import DataDisplay from "./DataDisplay";
import DataPredict from "./DataPredict";

import "./ForexTrading.css";

class ForexTrading extends Component {
    state = {
        tabs : [
            {id:1, tabName: '数据导入', tabCont: <DataImport/>},
            {id:2, tabName: '行情展示', tabCont: <DataDisplay/>},
            {id:3, tabName: '走势预测', tabCont: <DataPredict/>}
        ]
    }

    render() {
        return (
            <div className={'ForexTrading'}>
                <div className={'intro'}>
                    Welcome to Forex Trading!
                </div>
                <div className={'content'}>
                    <TabContainer
                        tabs = {this.state.tabs}
                    />
                </div>
            </div>
        );
    }
}

export default ForexTrading;
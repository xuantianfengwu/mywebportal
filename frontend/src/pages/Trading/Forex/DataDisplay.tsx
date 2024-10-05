import React, {Component} from 'react';

import {Card} from 'antd';
import EchartsTest from "../../../components/ECharts";
import ReactEChartsTest from '../../../components/EchartsForReact';

class DataDisplay extends React.Component<any, any> {
    render(){
        return(
          <div>
              <Card>
                 <ReactEChartsTest />
              </Card>
          </div>
        )
    }
}

export default DataDisplay;
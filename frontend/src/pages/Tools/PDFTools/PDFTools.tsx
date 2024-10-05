import React, {Component} from 'react';

import TabContainer from "../../../components/TabContainer/TabContainer";
import PDFTransformer from "./PDFTransformer"

import "./PDFTools.css"

class PDFTools extends Component {
    state = {
        tabs : [
            {id: 1, tabName: 'PDF转换', tabCont: <PDFTransformer/>},
        ]
    }

    render() {
        return (
            <div className={'PDFTools'}>
                This is PDF Tools!
                <TabContainer
                    tabs = {this.state.tabs}
                />
            </div>
        );
    }
}

export default PDFTools;
import React, {Component} from 'react';
import VideoGenerator from "./VideoGenerator";
import TabContainer from "../../../components/TabContainer/TabContainer";

import "./VideoTools.css";

class PDFTools extends Component {
    state = {
        tabs : [
            {id: 1, tabName: 'Video生成', tabCont: <VideoGenerator/>},
        ]
    }

    render() {
        return (
            <div className={'VideoTools'}>
                This is Video Tools!
                <TabContainer
                    tabs = {this.state.tabs}
                />
            </div>
        );
    }
}

export default PDFTools;
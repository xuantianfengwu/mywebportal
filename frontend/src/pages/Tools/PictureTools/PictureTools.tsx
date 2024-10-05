import React, {Component} from 'react';

import TabContainer from "../../../components/TabContainer/TabContainer"
import PictureLetterRecTool from "./PictureLetterRecTool"
import "./PictureTools.css"

class PictureTools extends Component {
    state = {
        tabs : [
            {id: 1, tabName: '图像文字识别', tabCont: <PictureLetterRecTool/>},
            {id: 2, tabName: '图像头像识别', tabCont: <></>},
            {id: 3, tabName: '图像头像比对', tabCont: <></>},
            {id: 4, tabName: '图像换头',    tabCont: <></>},
        ]
    }

    render() {
        return (
            <div className={'picturetools'}>
                This is Picture Tools!
                <TabContainer
                    tabs = {this.state.tabs}
                />
            </div>
        );
    }
}


export default PictureTools;
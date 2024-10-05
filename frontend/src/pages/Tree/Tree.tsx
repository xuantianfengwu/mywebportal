import React, {Component} from 'react';


import TreeDisplayer from "../../components/TreeDisplayer/TreeDisplayer";
import '../../components/TreeDisplayer/TreeDisplayer.css';

class IndicatorTreeDisplay extends Component<any, any> {
    renderContent = function(data:any) {
            return data.label;
        }

    render(){
        const data = {
            id: 0,
            label: 'XXX股份有限公司',
            children: [
                        {
                            id: 1,
                            label: '技术部',
                            children: [{
                                id: 4,
                                label: '后端工程师'
                            }, {
                                id: 5,
                                label: '前端工程师'
                            }, {
                                id: 6,
                                label: '运维工程师'
                            }]
                        },
                        {
                            id: 2,
                            label: '人事部'
                        },
                        {
                            id: 3,
                            label: '销售部'
                        }]
            }
        const horizontal = true; // true：横向  false：纵向
        const collapsable = true; // true：可折叠 false：不可折叠
        const expandAll = true; // true: 全部展开 false：全部折叠

        const node = {
                label: 'label',
                expand: 'expand',
                children: 'children'
            }

        return (
            <div>
                <TreeDisplayer
                    data={data}
                    horizontal={horizontal}
                    collapsable={collapsable}
                    expandAll={expandAll}
                    renderContent = {this.renderContent}
                />
            </div>
        )
    }
}

class Tree extends Component {
    render() {
        return (
            <div>
                <p>This is tree displayer!</p>
                <IndicatorTreeDisplay/>
            </div>
        );
    }
}

export default Tree;
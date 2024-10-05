import React, {Component, ReactNode} from 'react';
import classnames from 'classnames';

import './TreeDisplayer.css';

class TreeNode extends Component<any, any> {
    isLeaf = (data:any, prop:any) => {
        const node = prop.node;
        return !(Array.isArray(data[node.children]) && data[node.children].length > 0);
    };

    // 创建展开折叠按钮
    renderBtn = (data:any, prop:any ) => {
        const { onExpand } = prop;
        const node = prop.node;

        let cls = ['org-tree-node-btn'];

        if (data[node.expand]) {
            cls.push('expanded');
        }

        return React.createElement('span', {
            key: data.id,
            className: cls.join(' '),
            onClick: (e) => {
                e.stopPropagation();
                typeof onExpand === 'function' && onExpand(e, data);
            }
        });
    };

    // 创建 label 节点
    renderLabel = (data:any, prop:any) => {
        const node = prop.node;
        const label = data[node.label];
        const renderContent = prop.renderContent;
        const onClick = prop.onClick;
        const childNodes = [];

        if (typeof renderContent === 'function') {
            let vnode = renderContent(data);

            vnode && childNodes.push(vnode);
        } else {
            childNodes.push(label);
        }

        if (prop.collapsable && !this.isLeaf(data, prop)) {
            childNodes.push(this.renderBtn(data, prop));
        }

        const cls = ['org-tree-node-label-inner'];

        let { labelWidth, labelClassName } = prop;
        if (typeof labelWidth === 'number') {
            labelWidth = labelWidth.toString() + 'px';
        }

        labelClassName && cls.push(labelClassName);

        //labelWidth = '10px';
        const result =  React.createElement('div',
                                   {
                                            key: `label_${data.id}`,
                                            className: 'org-tree-node-label',
                                            onClick: (e) => typeof onClick === 'function' && onClick(e, data)
                                           },
                                   [React.createElement('div',
                                                                {
                                                                        key: `label_inner_${data.id}`,
                                                                        className: cls.join(' '),
                                                                        style: { width: labelWidth }
                                                                       },
                                                                childNodes)
                                            ]
                                   );
        //console.log('renderLabel result:', result);
        return result;
    };

    // 创建 node 子节点
    // @ts-ignore
    renderChildren = (list:any, prop:any) => {
        if (Array.isArray(list) && list.length) {
            // @ts-ignore
            const children = list.map(item => {
                return this.renderNode(item, prop);
            });
            return React.createElement('div', {
                key: `children_${children[0].key}`,
                className: 'org-tree-node-children'
            }, children);
        }
        return '';
    };

    // 创建 node 节点
    // @ts-ignore
    renderNode = (data:any, prop:any) => {
        const node = prop.node;
        const cls = ['org-tree-node'];
        const childNodes = [];

        // 是否叶子节点，决定className的格式
        if (this.isLeaf(data, prop)) {
            cls.push('is-leaf');
        } else if (prop.collapsable && !data[node.expand]) {
            cls.push('collapsed');
        }

        // 把自身推进childNodes
        childNodes.push(this.renderLabel(data, prop));

        // 如果不可折叠，直接全部渲染出来 data[node.expand]不太清楚
        if (!prop.collapsable || data[node.expand]) {
            childNodes.push(this.renderChildren(data.children, prop));
        }

        const result:ReactNode = React.createElement('div',
                                           {
                                                    key: data.id,
                                                    className: cls.join(' ')
                                                  },
                                            childNodes);
        //console.log('renderNode result:', result);
        return result;
    };

    render() {
        const data = this.props.data;
        const prop = this.props;
        const render_res = this.renderNode(data, prop);
        return (
            render_res
        )
    }
}

export default class TreeDisplayer extends Component<any, any> {

    componentDidMount() {
        console.log('TreeDisplayer componentDidMount');
        const { expandAll, data } = this.props;
        if(expandAll) this.toggleExpand(data, true);
    }

    componentWillUnmount() {
    }

    handleExpand(e:any, nodeData:any) {
        if ('expand' in nodeData) {
            nodeData.expand = !nodeData.expand;
            if (!nodeData.expand && nodeData.children) {
                this.collapse(nodeData.children);
            }
            this.forceUpdate();
        }else {
            nodeData.expand = true;
            this.forceUpdate();
        }
    }

    collapse(list:any) {
        let _this = this;
        list.forEach(function(child:any) {
            if (child.expand) {
                child.expand = false;
            }
            child.children && _this.collapse(child.children);
        });
    }

    toggleExpand(data:any, val:any) {
        let _this = this;
        if (Array.isArray(data)) {
            data.forEach(function(item) {
                item.expand = val;
                if (item.children) {
                    _this.toggleExpand(item.children, val);
                }
            });
        } else {
            data.expand = val;
            if (data.children) {
                _this.toggleExpand(data.children, val);
            }
        }
        this.forceUpdate();
    }

    render() {
        const { horizontal, onClick } = this.props;
        //console.log('Input Props:', this.props);
        const node = {
                label: 'label',
                expand: 'expand',
                children: 'children'
            }

        return  (
            <div className="org-tree-container">
                <div className={classnames('org-tree', { 'horizontal': horizontal })}>
                    <TreeNode
                        node = {node}
                        onExpand={(e:any, nodeData:any)=> this.handleExpand(e, nodeData)}
                        onClick={(e:any, nodeData:any)=> onClick && onClick(e, nodeData)}
                        {...this.props}
                    />
                </div>
            </div>
        )
    }
}


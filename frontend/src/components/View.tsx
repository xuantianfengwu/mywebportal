// 将 authrouter 渲染成 带Layout的格式
import {BrowserRouter as Router, Redirect, Route, Switch} from "react-router-dom";
import ILayout from "./layout/Layout";
import {router, IRouter} from "../router/Router";
import React, {Suspense, Component, ReactNode, lazy, } from "react";

export default class View extends Component<any, any> {
    generateRoute = (routerList?: IRouter[]): ReactNode => {
        let routenodes = (routerList?.map(r => {
                                if (r.children) {
                                    return (
                                        this.generateRoute(r.children)
                                    )
                                }
                                return (
                                    <Route exact={r.exact}  path={r.path} key={r.id}>
                                        <ILayout>{r.component}</ILayout>
                                    </Route>
                                )
                            })
                        )
        return routenodes
    }

    render() {
        // 若是authrouter中路由，则LeftBar会展示所有authrouter按钮
        // 若是unauthrouter中路由，则LeftBar不会展示任何按钮，且兜底进404页面
        return (
                    <Suspense fallback={<div>Loading...</div>}>
                         <Router>
                             <Switch>
                                 <Redirect exact from={'/'} to={'/homepage'}/>
                                 {this.generateRoute(router)}
                            </Switch>
                        </Router>
                    </Suspense>

        )
    }
}
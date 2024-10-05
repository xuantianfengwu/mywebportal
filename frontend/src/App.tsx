import React, {Component} from 'react';
import View from './components/View'

import './App.css';

import {inject, observer} from "mobx-react";
import {getUserInfo} from "./api/userinfo";

@inject('userStore')
class WebApp extends Component<any, any> {
    // 访问api获取登录用户姓名，更新userStore
    getUserName = () => {
        getUserInfo().then( (response: { data: {user_name: string;};}) => {
            //console.log(response);
            const username = response.data.user_name;
            this.props.userStore?.changeName(username);
        })
    }

    render() {
        // this.getUserName();
        return (
            <View/>
        )}
}

export default WebApp;

import React, {Component, createRef, RefObject} from 'react';
import {RouteComponentProps, withRouter} from "react-router-dom";

import {Button, Form, FormInstance, Input, message, Space} from "antd";
import {login} from "../api/login";
import './Login.css'

const layout = {
    labelCol: {span: 4},
    wrapperCol: {span: 16},
};
const tailLayout = {
    wrapperCol: {offset: 8, span: 16},
};

interface LoginProps extends RouteComponentProps{

}

class Login extends Component<LoginProps, any> {
    formRef: RefObject<FormInstance>

    constructor(props: any, context: any) {
        super(props, context);
        this.formRef = createRef<FormInstance>()
    }

    login = (form: any) => {
        login(form.userid, form.password).then(response => {
            const {code, msg, data} = response.data;

            const reg = new RegExp("(^|&)" + 'url' + "=([^&]*)(&|$)");
            const params = this.props.location.search.substr(1).match(reg);
            const origin_url = params?params[2]:'/';
            console.log('Origin Url:', origin_url);

            if (code === 200) {
                message.success(msg)
                window.location.href = origin_url
            } else {
                message.error(msg)
            }
        })
    }

    render() {
        return (
            <div id='login'>
                <Form
                    id='login-form'
                    {...layout}
                    ref={this.formRef}
                    onFinish={this.login}
                >
                    <Form.Item  label='用户名' name='userid'
                                rules={[{   type: 'string',
                                            required: true
                                        }
                                    ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item  label='密码' name='password'
                                rules={[{ type: 'string',
                                          required: true
                                        }
                                    ]}
                    >
                        <Input.Password />
                    </Form.Item>

                    <Form.Item {...tailLayout}>
                        <Space>
                            <Button type="primary" htmlType="submit"> 登录 </Button>
                            <Button type="primary" htmlType="reset">  重置 </Button>
                        </Space>
                    </Form.Item>

                </Form>
            </div>
        );
    }
}

export default withRouter(Login);
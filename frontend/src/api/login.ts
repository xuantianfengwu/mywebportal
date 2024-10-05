import request from "../utils/request";

export const login = (userid: string, password: string) => {
    return request({
        url:    '/login/login',
        method: 'post',
        data:   {userid: userid,
                 password: password
                }
    })
}

import request from "../utils/request";

export const getTodosTask = () => {
    return request({
        url:    '/todos/task',
    })
}

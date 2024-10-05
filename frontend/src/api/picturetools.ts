import request from "../utils/request";

export const getPictureLetterRecRes = (file_name: string, model_type: string) => {
    const data = new FormData();
    data.append('file_name', file_name);
    data.append('model_type', model_type);
    return request({
        url:    '/picture/letterrec',
        method: 'post',
        headers: {'Content-Type': 'multipart/form-data'},
        data:    data
    })
}
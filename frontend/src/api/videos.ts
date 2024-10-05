import request from "../utils/request";

export const getVideoUrl = (videoname: string) => {
    return request({
        url:    '/video/get/'+videoname,
        method: 'get',
    })
}

export const getVideoList = () => {
    return request({
        url:    '/video/videolist/get',
        method: 'get',
    })
}


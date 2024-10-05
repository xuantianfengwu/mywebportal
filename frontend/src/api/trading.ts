import request from "../utils/request";

export const importUploadFile = (f: any, f_type: string) => {
    const data = new FormData();
    data.append('file', f, f.name);
    data.append("file_type", f_type);
    return request ({
        url:     'trading/forex/file/upload',
        method:  'post',
        headers: {'Content-Type': 'multipart/form-data'},
        data:    data,
    })
}

export const initializeDB = () => {
    return request ({
        url:     'trading/forex/db/initialize',
    })
}

import request from "../utils/request";

export const PDFDelSpecificPage = (upload_files: any, operate_params: any) => {
    const data = new FormData();
    data.append('operate_type', '1');
    data.append('upload_files', JSON.stringify(upload_files));
    data.append('operate_params', JSON.stringify(operate_params));
    return request({
        url:    '/pdf/transformer/delpage',
        method: 'post',
        headers: {'Content-Type': 'multipart/form-data'},
        data:    data
    })
}

export const PreviewPDFRes = (oper_type: string, prev_file: string) => {
    return request({
        url:    '/pdf/transformer/res/preview',
        //responseType: 'blob',
        headers: {'Cache-Control': 'no-cache'},
        params: {
            oper_type: oper_type,
            prev_file: prev_file,
        }
    })
    // const url = '/pdf/transformer/res/preview' + '?oper_type=' + oper_type + '&prev_file=' + prev_file
    // window.open(process.env.REACT_APP_URL + url)
}

export const DownloadPDFRes = (oper_type: string, download_type: string, download_files: []) => {
    const data = new FormData();
    data.append('oper_type', oper_type);
    data.append('download_type', download_type);
    data.append('download_files', JSON.stringify(download_files));
    return request({
        url:    '/pdf/transformer/res/download',
        method: 'post',
        responseType: 'blob',
        headers: {'Content-Type': 'multipart/form-data'},
        data:    data
    })
}


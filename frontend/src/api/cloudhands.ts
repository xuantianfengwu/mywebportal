import request from "../utils/request";

export const crawlData = (week_start: string, data_type: string) => {
    return request({
        url:    '/trading/cloudhands/crawl',
        params: {
            data_type: data_type,
            week_start: week_start
        }
    })
}

export const getFundamentalEventData = (week_start: string) => {
    // 获取 基本面摘要 & 周报摘要 数据
    return request({
        url:'/trading/cloudhands/forex/fund_event',
        params: {week_start: week_start}
    })
}

export const getForexTrendSummary = (week_start: string) => {
    // 获取 外汇期货合约走势 数据
    return request({
        url: '/trading/cloudhands/forex/trend_summary',
        params: {week_start: week_start}
    })
}

export const getForexPositionData = (week_start:string) => {
    // 获取 外汇期货头寸分析 数据
    return request({
        url:    '/trading/cloudhands/forex/position_data',
        params: { week_start: week_start }
    })
}

export const getMajorCurrForecast = (week_start:string) => {
    // 获取 重点货币对展望 数据
    return request({
        url:    '/trading/cloudhands/forex/major_currency_forecast',
        params: { week_start: week_start }
    })
}

export const getForexFutureDataEvent = (week_start: string, data_type: string) => {
    // 获取 财经数据&财经事件 数据
    return request({
        url:    '/trading/cloudhands/forex/future_data_event',
        params: {
            data_type: data_type,
            week_start: week_start
        }
    })
}

export const generateOutputReport = (week_start: string,
                                     report_title: string,
                                     report_summary: string,
                                     fundamental_events: any,
                                     trend_image_src: string,
                                     position_summary_data: any,
                                     curr_forecasts: any,
                                     strategy_info: any,
                                     data_image_src: string,
                                     event_image_src: string) => {
    const data = new FormData();
    data.append('week_start', week_start);
    data.append('report_title', report_title);
    data.append('report_summary', report_summary);
    data.append('fundamental_events', JSON.stringify(fundamental_events));
    data.append('trend_image_src', trend_image_src);
    data.append('position_summary_data', JSON.stringify(position_summary_data))
    data.append('curr_forecasts', JSON.stringify(curr_forecasts));
    data.append('strategy_info', JSON.stringify(strategy_info));
    data.append('data_image_src', data_image_src);
    data.append('event_image_src', event_image_src);

    return request({
        url:    '/trading/cloudhands/forex/output_report',
        method: 'post',
        headers: {'Content-Type': 'multipart/form-data'},
        data:    data
    })
}

export const getFile = (week_start: string, file_name: string) => {
    return request({
        url: '/trading/cloudhands/file',
        headers: {'Cache-Control': 'no-cache'},
        params: {
            week_start: week_start,
            file_name: file_name
        }
    })
}
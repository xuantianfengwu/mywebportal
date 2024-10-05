
from flask import Blueprint, request
minip_bp = Blueprint('minip', __name__)

from ..service.miniprogram_tools import MiniProgramTools
m_tools = MiniProgramTools()

from ..utils.web_response import WebResponse

@minip_bp.route("get/q_series_list")
def get_q_series_list():
    data = m_tools.generate_q_series_list()
    resp = WebResponse.success('获取数据成功！', data=data)
    return resp

@minip_bp.route("get/q_series_reports")
def get_q_series_reports():
    s_code, series_code = request.args['s_code'], request.args['series_code']
    data = m_tools.generate_q_series_reports(s_code, series_code)
    resp = WebResponse.success('获取数据成功！', data=data)
    return resp
from flask import Blueprint, request
import os
import flask

from backend.service.picture_tools import PictureTools
from backend.utils.web_response import WebResponse

picture_bp = Blueprint('picture', __name__)

@picture_bp.route('/letterrec', methods=['POST'])
def picture_letter_rec_tool():
    model_type = request.form['model_type']
    file_name = request.form['file_name']

    file_path = os.path.join('backend', 'static', 'upload', 'picture_tools', file_name)
    rec_text = PictureTools.picture_letter_rec(file_path, model_type)
    data = {'rec_text': rec_text}
    return WebResponse.success('图片文字识别成功！', data=data)

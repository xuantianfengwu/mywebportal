
from flask import Blueprint, send_from_directory
import os

video_bp = Blueprint('video', __name__)

@video_bp.route("/get/<videoname>")
def get_video(videoname):
    print('videoname', videoname)
    return send_from_directory('./backend/static/videos', filename=videoname, as_attachment=True)

@video_bp.route("/videolist/get")
def get_video_list():
    backend_video_path = 'backend/static/videos'
    frontend_video_path = 'frontend/src/static/videos'
    for path in [backend_video_path, frontend_video_path]:
        if not os.path.exists(path):
            os.makedirs(path)
    backend_videolist  = ['B_{}'.format(f) for f in os.listdir(backend_video_path) if f!='.keep']
    frontend_videolist = ['F_{}'.format(f) for f in os.listdir(frontend_video_path) if f!='.keep']
    resp = {
        'frontend':{
            'videolist': frontend_videolist
        },
        'backend':{
            'videolist': backend_videolist
        }
    }
    return resp
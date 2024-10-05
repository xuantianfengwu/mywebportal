import React, {Component, ReactNode} from 'react';

import Player from 'griffith' //https://github.com/zhihu/griffith/blob/master/README-zh-Hans.md

import {getVideoList, getVideoUrl} from '../../../api/videos'
import "./VideoPlayer.css"

class GriffithPlayer extends Component<any, any> {

    generateSources = () => {
        const sd_url = this.props.sd_url;
        const hd_url = this.props.hd_url;
        return {
            sd: {
                play_url: sd_url
            },
            hd: {
                play_url: hd_url
            }
        }
    }

    render() {
        const play_id = this.props.play_id
        const sources = this.generateSources()
        return (
            <Player
                id={play_id}
                sources={sources}
            />
        )
    }
}

class VideoPlayer extends Component<any, any> {
    state = {
        frontend_videos: [],
        backend_videos: [],

        playing_id: '0',
        playing_hd_url: '',
        playing_sd_url: ''
    }

    componentDidMount(): void {
        getVideoList().then((response)=>{
            const frontend_videos = response.data.frontend.videolist;
            const backend_videos = response.data.backend.videolist;
            console.log('getVideoList():', response.data)

            this.setState({
                frontend_videos:   frontend_videos,
                backend_videos:    backend_videos,
            })
        })
    }

    handle_GriffithPlayer_onClick = (e:any) => {
        const video_type = e.target.name.substring(0,1)
        const video_name = e.target.name.substring(2);
        console.log('button click:', video_name);
        console.log('video type:', video_type);

        let hd_url = '';
        let sd_url = '';
        if(video_type=='F'){
            // 文件夹作为变量传入require不行，必须在require()中写死，且build时文件夹下全部文件将被打包
            hd_url = require('../../../static/videos/'+video_name).default
            sd_url = require('../../../static/videos/'+video_name).default
        }
        else if (video_type=='B'){
            hd_url = process.env.REACT_APP_URL+'/video/get/'+video_name;
            sd_url = process.env.REACT_APP_URL+'/video/get/'+video_name;
        }

        this.setState({
            playing_id :     video_name,
            playing_hd_url : hd_url,
            playing_sd_url : sd_url
        })
    }

    generateVideoButtons = (videos?: string[]) : ReactNode => {
        let video_buttons = (videos?.map(
                (video?:string)=>{
                    return (
                            //console.log(video);
                            <button name={video}
                                    onClick={this.handle_GriffithPlayer_onClick}
                            >
                                {video?.substring(2)}
                            </button>
                        )
                }
            ))
        console.log('video_buttons:', video_buttons)
        return video_buttons
    }

    render() {

        const frontend_video_buttons = this.generateVideoButtons(this.state.frontend_videos);
        const backend_video_buttons = this.generateVideoButtons(this.state.backend_videos);

        const playing_id = this.state.playing_id;
        const playing_hd_url = this.state.playing_hd_url;
        const playing_sd_url = this.state.playing_sd_url;

        return (
            <div>
                <p> This is VideoPlayer! </p>
                <div className={'GriffithPlayer'} >

                    <GriffithPlayer
                        play_id = {playing_id}
                        hd_url = {playing_hd_url}
                        sd_url = {playing_sd_url}
                    />

                    <p> Frontend Local Videos：{frontend_video_buttons} </p>
                    <p> Backend Local Videos:  {backend_video_buttons} </p>

                </div>
            </div>
        );
    }
}

export default VideoPlayer;
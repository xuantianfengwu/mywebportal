import React, {Component} from 'react';

import "./reset.css";
import "./Movies.css";

class Movies extends Component {
    render() {
        return (
            <div>
                This is Movies!
                <div className={'main'}>
                    {/*菜单*/}
                    <nav className={'nav'}>
                        <a className={'select'}>正在热映</a>
                        <a>即将上映</a>
                        <a>经典影片</a>
                    </nav>
                    {/*主区域*/}
                    <div className={'container'}>
                        <div className={'choose-area'}>
                            <div className={'choose-item clearfix'}>
                                <div className={'left'}> 类型：</div>
                                <div className={'right'}>
                                    <ul>
                                        <li className={'select'}><a>abcde</a></li>
                                        <li><a>asdsada</a></li>
                                        <li><a>sadsada</a></li>
                                        <li><a>acvfv</a></li>
                                        <li><a>bghnra</a></li>
                                        <li><a>dsefrwfa</a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    {/*主区域*/}
                </div>
            </div>
        );
    }
}

export default Movies;
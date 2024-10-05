import React, {Component} from 'react';

import "./Article.css"

class Article extends Component {
    render() {
        return (
            <div className={'body'}>
                <article className={'article-container'}>
                    <header>
                        <h1>常规流</h1>
                        <div className={'origin-link'}>
                            原文地址：<a href={'www.baidu.com'}>www.baidu.com</a>
                        </div>
                    </header>
                    <section>
                        <p>This is Article!</p>
                        <h2>Chapter1</h2>
                        <p>P1</p>
                        <p>P2</p>
                        <h2>Chapter2</h2>
                        <p>P1</p>
                        <p>P2</p>
                    </section>
                </article>
            </div>
        );
    }
}

export default Article;
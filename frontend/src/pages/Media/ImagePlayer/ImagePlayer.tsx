import React, {Component} from 'react';

class ImagePlayer extends Component {
    createMarkup() {
      return {__html: '<a>test</a>'};
    }

    render() {
        return (
            <div>
                This is ImagePlayer!
                <div dangerouslySetInnerHTML={this.createMarkup()}></div>
            </div>
        );
    }
}

export default ImagePlayer;
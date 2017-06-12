import os
import picamera
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap


camera = picamera.PiCamera()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/takepicture')
def take_picture():
    camera.capture('static/image.png')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0')

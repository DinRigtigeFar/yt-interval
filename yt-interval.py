import multiprocessing
import os
import zipfile
from pathlib import Path

from flask import (Flask, make_response, redirect, render_template, request,
                   send_file, session, url_for)

from ParseInput import (download_interval, download_pics, download_whole,
                        make_time, parser)


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def index():
    if len(os.listdir('./content')) > 0:
        [f.unlink() for f in Path('./content').glob('*') if f.is_file()]
    if os.path.exists('media.zip'):
        Path('./media.zip').unlink()

    return render_template('index.html', cpu_cores=multiprocessing.cpu_count())


@app.route('/downloading', methods=['POST', 'GET'])
def downloading():
    if request.method == 'POST':
        # Get the value from inputs
        session['download_playlist'] = request.form.get('down_play')
        session['cores'] = request.form.get('core_amount')
        # Get the links
        comments = request.form['comments']
        comments_2 = [comment.strip() for comment in comments.split('\n')]
        # parsed[0] are videos, parsed[1] are pictures. made_time[0] are intervals, made_time[1] are whole videos.)
        parsed = parser(comments_2)
        made_time = make_time(parsed[0])
        session['intervals'] = made_time[0]
        session['whole_clip'] = made_time[1]
        session['pics'] = parsed[1]

        if len(session['whole_clip']) + len(session['intervals']) + len(session['pics']) == 0:
            return render_template('index.html', cpu_cores=multiprocessing.cpu_count(), message='Please input a valid link: youtube.com/blabla, youtu.be/blabla some.thing/jpg')
        else:
            return render_template('success.html')


@app.route('/waiting', methods=['POST'])
def waiting():
    cores = int(session.get('cores'))
    # Downloads the media to content using multiprocessing
    if cores > (num_workers := multiprocessing.cpu_count()):
        num_workers = num_workers
    elif cores < 1:
        num_workers = 1
    else:
        num_workers = cores
    if session.get('download_playlist') == None:
        playlist = False
    else:
        playlist = True
        
    if len(session.get('whole_clip')) > 0:
        args = [(i, playlist) for i in session.get('whole_clip')]
        with multiprocessing.Pool(processes=num_workers) as pool:
            pool.starmap(download_whole, args)
    if len(session.get('intervals')) > 0:
        with multiprocessing.Pool(processes=num_workers) as pool:
            pool.map(download_interval, session.get('intervals'))
    if len(session.get('pics')) > 0:
        with multiprocessing.Pool(processes=num_workers) as pool:
            pool.map(download_pics, session.get('pics'))
    return render_template('waiting.html', message=f'Done downloading all of your data.')


@app.route('/waiting/wait', methods=['GET'])
def wait():
    return f"This is the content of the content directory: {os.listdir('content/')}."


@app.route('/waiting/done', methods=['GET'])
def done():
    # Returns the content of the media directory
    with zipfile.ZipFile('media.zip', 'w', zipfile.ZIP_DEFLATED) as zF:
        for video in os.listdir('content/'):
            if video == '.keep':
                continue
            zF.write('content/'+video)
    return send_file('media.zip',
                     mimetype='zip',
                     download_name='media.zip',
                     as_attachment=True)


if __name__ == '__main__':
    app.run()

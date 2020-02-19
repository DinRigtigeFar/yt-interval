from flask import Flask, render_template, request, make_response, session, redirect, url_for, send_file
from ParseInput import parser, make_time, download_whole, download_interval, download_pics
import os
import zipfile
from rq import Queue
from rq.job import Job
from worker import conn
from time import sleep

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/downloading', methods=['POST', 'GET'])
def downloading():
    if request.method == 'POST':
        comments = request.form['comments']
        comments_2 = [comment.strip() for comment in comments.split('\n')]
        # Only get the video part of the parsed file ([0])
        parsed = parser(comments_2)
        made_time = make_time(parsed[0])
        session["intervals"] = made_time[0]
        session["whole_clip"] = made_time[1]
        session["pics"] = parsed[1]

        if len(session["whole_clip"]) == 0 and len(session["intervals"]) == 0 and len(session["pics"]) == 0:
            return render_template('index.html', message="Please input a valid link: youtube.com/blabla, youtu.be/blabla some.thing/jpg")
        return render_template('success.html')

@app.route('/waiting', methods=['POST'])
def waiting():
    # Make a queue for the lengthy ffmpeg process (and others to make sure)
    q = Queue(connection=conn)

    # Downloads the media (no need to call if empty)
    if len(session.get("intervals")) > 0:
        interval = q.enqueue(download_interval, session.get("intervals"))
        session["interval_id"] = interval.id
    if len(session.get("whole_clip")) > 0:
        whole_clip = q.enqueue(download_whole, session.get("whole_clip"))
        session["whole_clip_id"] = whole_clip.id
    if len(session.get("pics")) > 0:
        pics = q.enqueue(download_pics, session.get("pics"))
        session["pics_id"] = pics.id
    sleep(20)
    return render_template("waiting.html", message=f"{Job.fetch(session.get('interval_id'), connection=conn)}")

def check_content():
    if len(os.listdir('media/')) == len(session.get("interval_id")) + 1:
        return
    else:
        sleep(15)
        check_content()

@app.route('/waiting/done', methods=['GET'])
def done():
    check_content()
    # Returns the content of the media directory
    with zipfile.ZipFile('media.zip','w', zipfile.ZIP_DEFLATED) as zF:
            for video in os.listdir('media/'):
                zF.write('media/'+video)
    return send_file('media.zip',
            mimetype = 'zip',
            attachment_filename= 'media.zip',
            as_attachment = True)

    # TODO: Find out how to wait for the worker to get done before returning the contents of the media directory!!!!


if __name__ == '__main__':
    app.run()

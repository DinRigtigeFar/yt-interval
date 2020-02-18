from flask import Flask, render_template, request, make_response, session, redirect, url_for, send_file
from ParseInput import parser, make_time, download_whole, download_interval
import os
import zipfile

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
        made_time = make_time(parser(comments_2)[0])
        session["whole_clip"] = made_time[1]
        session["intervals"] = made_time[0]
        return render_template('success.html')

@app.route('/waiting', methods=['POST'])
def waiting():
    # Downloads the videos
    download_interval(session.get("intervals"))
    download_whole(session.get("whole_clip"))
    # Packages content of media directory into a zip file that is sent to the user
    with zipfile.ZipFile('videos.zip','w', zipfile.ZIP_DEFLATED) as zF:
        for video in os.listdir('media/'):
            zF.write('media/'+video)
    return send_file('videos.zip',
            mimetype = 'zip',
            attachment_filename= 'videos.zip',
            as_attachment = True)

if __name__ == '__main__':
    app.run()
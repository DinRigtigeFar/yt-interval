# yt-interval
Flask app to download YT videos in intervals. Eg. from start to 30 seconds: start-30
The format is tabdelimited: youtube.com/blablabla  2:00-end
The above will (attempt to) download from 2 minutes into the video until the end.

You can supply as many videos as you want, just seperate them by \n.
And it also downloads full length videos. Just don't have any numbers in the second tab:
youtube.com/blablabla  this is fucking awesome
The above text will download the whole video.

It can also donwload pictures if you supply a link with 'jpg' in it somwhere.

The program requires ffmpeg to be installed on your machine.

## Installation
```
git clone https://github.com/DinRigtigeFar/yt-interval.git
cd yt-interval
python3 -m venv venv_yt
. venv_yt/bin/activate
pip install -r requirements.txt
python app.py
```


app.py is the frontend, but ParseInput.py is where all the magic happens.

I hope you enjoy this program.

Future wants could be to implemet workers so you won't have to wait for the long ffmpeg process to finish.

# yt-interval
Flask app to download YT videos in intervals. Eg. from start to 30 seconds: start-30
The format is tabdelimited: youtube.com/blablabla  2:00-end
The above will (attempt to) download from 2 minutes into the video until the end.
You can also download specific intervals: 10:45-11:11

You can supply as many videos as you want, just seperate them by newline.
It also downloads full length videos. To do so leave out the second tab or omit numbers from it:
```
youtube.com/blablabla  this is fucking awesome
```

It can also donwload pictures if you supply a link with 'jpg' in it somwhere.

The program requires ffmpeg which you can install using e.g. homebrew on Mac:
```
brew install ffmpeg
```

## Installation
Use a virtual environment in order to avoid package clashes:
```
git clone https://github.com/DinRigtigeFar/yt-interval.git
cd yt-interval
python3 -m venv venv_yt
. venv_yt/bin/activate
pip install -r requirements.txt
python yt-interval.py
```

Downloading the whole video is significantly faster than downloading intervals. The reason behind this is in order to download intervals ffmpeg is used for transcoding the video stream. ffmpeg will use all the cores you have on your machine, so waiting times could be shorter for higher core count machines.


I hope you enjoy this program and feel free to leave a comment or request features.
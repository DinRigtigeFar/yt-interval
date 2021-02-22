# yt-interval
![landing_page](demo/landing_page.png)
## Description
Flask app to download YT videos in intervals or the whole video. The app will detect which you want and it is also possible to download a whole playlist (only for whole videos at the moment). It uses multiprocessing for increased speed.<br>

## Input formats
The app accepts different formats, but only one link per line. The intervals has to specified on the same line as the link and has to be separated by a space.<br>
Examples:
````
youtube.com/blablabla 2:00-11:49
youtube.com/blablabla 1:28-end
youtube.com/blablabla start-4:02
youtube.com/blablabla start-end
youtube.com/blablabla
````
The two latter examples will download the whole video as no interval is specified.

You can supply as many videos as you want, just seperate them by newline.
It will also donwload pictures if you supply a link with '**jpg**' somewhere in it.

When the download has finished you can either press the "**Download here**" button or locate your files in `yt-interval/content`. <br>
Pressing the "**Back to the frontpage**" button will empty the content folder.

## Prerequisite
The program requires ffmpeg which you can install using e.g. homebrew on Mac:
```
brew install ffmpeg
```

## Installation
Use a virtual environment:
```
git clone https://github.com/DinRigtigeFar/yt-interval.git
cd yt-interval
python3 -m venv venv_yt
. venv_yt/bin/activate
pip install -r requirements.txt
python yt-interval.py
```

An environment variable called `SECRET_KEY` is required in order to get the flask app to run. You can put the key (a string) in your bash_profile or export one before launching the program.

Downloading the whole video is significantly faster than downloading intervals.

I hope you enjoy this program and feel free to leave a comment or request features.
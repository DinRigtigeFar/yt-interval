# yt-interval
![landing_page](demo/landing_page.png)
## Description
Flask app to download YT videos in intervals or the whole video, or both at the same time.
It is also possible to download a playlist (only for whole videos at the moment).<br>
It uses multiprocessing for increased speed with the option for you to specify how many threads to use. Default is all threads.<br>

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
The two last examples will download the whole video as no interval is specified.

You can supply as many videos as you want, just seperate them by newline.
It will also donwload pictures if you supply a link with '**jpg**' somewhere in it.

When the download has finished you can either press the "**Download here**" button or locate your files in `yt-interval/content`. <br>
Pressing the "**Back to the frontpage**" button will empty the content folder as a means to cleanup after use.

## Prerequisite
The program requires ffmpeg with AV1 support. [See how to compile it in this link](https://trac.ffmpeg.org/wiki/Encode/AV1).
For ubuntu you can use this [script](https://gist.github.com/sparrc/026ed9958502072dda749ba4e5879ee3).

## Installation
Use a virtual environment:
```
git clone https://github.com/DinRigtigeFar/yt-interval.git
cd yt-interval
conda env create --file env.yml
conda activate yt_down
pip install -e git+git://github.com/mohamed-challal/pafy.git@develop#egg=pafy
python yt-interval.py
```

An environment variable called `SECRET_KEY` is required in order to get the flask app to run. You can put the key (a string) in your bash_profile or export one before launching the program.

Downloading the whole video is significantly faster than downloading intervals.

I hope you enjoy this program and feel free to leave a comment or request features.

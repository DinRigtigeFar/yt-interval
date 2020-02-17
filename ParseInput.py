#!/usr/local/bin/python

import re
import os
import youtube_dl
import datetime
#import PySimpleGUI as sg
import ffmpeg
import pafy
import sys
import requests

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    Need it for path of ffmpeg
    Pass the relative path to ffmpeg (ffmpeg/ffmpeg) in the download interval function
    """
    try:
        # This is the path to the script
        base_path = sys.argv[0]
        # Avoid the last 14 characters as these are the name of the program 'AutoYTDownload'
        # ffmpeg folder is located in the same folder as the program (not in the program) therefore,
        # the path is path to the parent folder
        base_path = base_path[:-14]
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def parser(list_of_text):
    """
    Open a tab delimited file and return links and time
    """

    # Youtube link regex
    yt_link = re.compile(r"http(s)?:\/\/www\.youtu.*")
    pic_link = re.compile(r"^http(s)?:\/\/.*jpg.*")

    pics = [link.split() for link in list_of_text if re.match(pic_link, link)]

    found_yt_links = [line.split() for line in list_of_text if re.match(yt_link, line)]

    return found_yt_links, pics

def hasNumbers(inputString):
    """
    Function that returns true if a string contains a number
    """
    return any(char.isdigit() for char in inputString)

def tedoius_time(time_string):
    """
    Small function to change time format.
    Used for make_time func
    """

    if time_string.lower() == "start":
        time_string = "00:00:00"
    # We need this exact string for later
    elif time_string.lower() == "slut":
        return time_string
    elif len(time_string) == 4:
        time_string = f"00:0{time_string}"
    elif len(time_string) == 5:
        time_string = f"00:{time_string}"
    elif len(time_string) == 6:
        time_string = f"00{time_string}"
    elif len(time_string) == 7:
        time_string = f"0{time_string}"
    return time_string

def make_time(parsed_file):
    """
    Function that makes sure the time format is in 00:00:00
    Else changes the time format into that
    Takes the output from the parser(filename) func
    """

    whole_clip = []

    holder_list = parsed_file
    
    for line in holder_list[:]:
        try:
            if not hasNumbers(line[1]):
                whole_clip.append(line[0])
                holder_list.remove(line)
        except IndexError:
            whole_clip.append(line[0])
            holder_list.remove(line)

    # Split time based on dash character
    split_times = [line[1].split("-") for line in holder_list]
    links = [line[0] for line in holder_list]

    # Replace . with :
    for time in split_times:
        try:
            time[0] = time[0].replace(".", ":")
            time[1] = time[1].replace(".", ":")
        except IndexError:
            pass

        # Change the time into the correct format by tedious if else statements. Assumes at least 4 characters always.
        # Checks the start time. If time is "start" change it to 00:00:00.
        time[0] = tedoius_time(time[0])
        time[1] = tedoius_time(time[1])

    # Add or subtract one second for good key frame
    add_sub = datetime.timedelta(seconds=1)

    # Subtract one second at the start of the interval (if possible) and add one at the end.
    # To get the perfect keyframe
    for time in split_times:
        # Split the times into hh, mm, ss
        first = time[0].split(":")
        if not time[1].lower() == "slut":
            last = time[1].split(":")
        # Make a datetime object so we can perform calculations (date is irrelevant)
        start = datetime.datetime(2019, 1, 1, int(first[0]), int(first[1]), int(first[2]))
        if not time[1].lower() == "slut":
            end = datetime.datetime(2019, 1, 1, int(last[0]), int(last[1]), int(last[2]))
        # Perform calculations and if start is already at 00:00:00 do nothing
        start -= add_sub
        start_delta = str(start).split()[1]
        start_delta = start_delta.split(":")
        # For ffmpeg you give start time and then run time (not end time)
        offset = datetime.timedelta(hours=int(start_delta[0]), minutes=int(start_delta[1]), seconds=int(start_delta[2]))
        if not time[1].lower() == "slut":
            end += add_sub
            # This is how long the clip should be
            end -= offset
        # Assign new intervals
            time[1] = str(end).split()[1]
        start = str(start).split()
        if start[1] != "23:59:59":
            time[0] = start[1]

    # Zip the two lists together. But return a list of this, since a zip object can only be used once.
    zipped = zip(links, split_times)

    return list(zipped), whole_clip


def save_link_time(return_list, path_to_download):
    """
    Function that saves the return_list from make_time to a file called yt_vids.txt
    Optional, default False
    """

    # Opens a new file and writes lines to it and saves it at the spot provided
    with open(os.path.join(path_to_download, "yt_vids.txt"), "w") as w:
        w.write('\n'.join('{} {} {}'.format(x[0], x[1][0], x[1][1]) for x in return_list))


def download_whole(no_interval):
    """
    Function that downloads a whole video when no interval is supplied
    Downloaded to the same place where yt_vids is saved to (from save_link_time func)
    """
    print(os.getcwd())
    ydl_opts = {"nocheckcertificate": True, "noplaylist": True, "outtmpl": "media"}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for video in range(len(no_interval)):
            #sg.OneLineProgressMeter("Download progress", video+1, len(no_interval), "key", "Whole video download progress")
            try:
                ydl.download([no_interval[video]])
            except youtube_dl.utils.ExtractorError or youtube_dl.utils.DownloadError:
                print(f"Couldn't download {no_interval[video]}")
                pass


def download_interval(interval_list):
    """
    Function to download videos in specified intervals
    Takes a list (interval_list) and a path as inputs
    """
    # Iterate over the zip object
    for link in range(len(interval_list)):
        try:
            video = pafy.new(interval_list[link][0], ydl_opts={'nocheckcertificate': True, "noplaylist": True})
            #sg.OneLineProgressMeter("Download progress", link + 1, len(interval_list), "key", "Interval video download progress")
            # Only downloads the video if the video hasn't been downloaded before
            if not os.path.exists(os.path.join("media", f"{video.title}.mp4")):
                video_s = video.getbestvideo()
                # TODO: add a way to get the second best stream (third etc.) when an error occurs using Pafy.videostreams and going through the list
                video_a = video.getbestaudio()

                # Checks if the end point is a string
                if interval_list[link][1][1].lower() == "slut":
                    # Where is the stream, where should we start, how long should it run
                    mp4_vid = ffmpeg.input(video_s.url, ss=interval_list[link][1][0], t=video.duration)
                    mp4_aud = ffmpeg.input(video_a.url, ss=interval_list[link][1][0], t=video.duration)
                else:
                    # Where is the stream, where should we start, how long should it run
                    mp4_vid = ffmpeg.input(video_s.url, ss=interval_list[link][1][0], t=interval_list[link][1][1])
                    mp4_aud = ffmpeg.input(video_a.url, ss=interval_list[link][1][0], t=interval_list[link][1][1])

                # Do the processing
                try:
                    (
                        ffmpeg
                        .concat(
                            # Specify what you want from the streams (v for video and a for audio)
                            mp4_vid['v'],
                            mp4_aud['a'],
                            # One video stream and one audio stream
                            v=1,
                            a=1
                        )
                        # Output is title of video with mp4 ending
                        .output(os.path.join("media", f'{video.title}.mp4'))
                        .run()
                    )
                except TypeError as e:
                    print(f"An error occurred e 0: {e}")
                except ffmpeg._run.Error as e:
                    print(f"An error occurred e 1: {e}")
        except Exception:
            with open(os.path.join("Not downloaded", "kunne_ikke_downloade.txt"), 'a') as f:
                f.write(f"I couldn't download {interval_list[link]}")

# Use this in the ffmpeg.run() command when compiling using pyinstaller. It's the path to ffmpeg.
# cmd=resource_path('ffmpeg/ffmpeg')


def download_pics(pics_links, path_to_download):
    """
    Function to download pictures from the input sequence
    """

    for link in range(len(pics_links)):
        sg.OneLineProgressMeter("Download progress", link + 1, len(pics_links), "key", "Picture download progress")
        r = requests.get(pics_links[link][0])

        with open(os.path.join(path_to_download, f"{link}.jpg"), "wb") as dl:
            dl.write(r.content)








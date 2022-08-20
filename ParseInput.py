import datetime
import os
import re

import ffmpeg
import pafy
import requests
import yt_dlp


def parser(list_of_text):
    """
    Read input from raw text and return the links and time
    """

    # Youtube link regex
    yt_link = re.compile(r"http(s)?:\/\/(www\.)?youtu.*")
    pron_link = re.compile(r".*pornhub.*")
    pic_link = re.compile(r"^http(s)?:\/\/.*jpg.*")

    pics = [link.split() for link in list_of_text if re.match(pic_link, link)]

    found_yt_links = [line.split()
                      for line in list_of_text if re.match(yt_link, line)]
    found_pron = [line.split()
                  for line in list_of_text if re.match(pron_link, line)]

    joined_links = found_yt_links + found_pron

    return joined_links, pics


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
    start = ['start', 'begin', 'beginning', 'head', 'first']
    end = ['slut', 'end', 'tail', 'finish',
           'finito', 'fin', 'done', 'finished']

    if time_string.lower() in start:
        time_string = "00:00:00"
    # We need this exact string for later
    elif time_string.lower() in end:
        return time_string
    elif len(time_string) == 1:
        time_string = f"00:00:0{time_string}"
    elif len(time_string) == 2:
        time_string = f"00:00:{time_string}"
    elif len(time_string) == 3:
        time_string = f"00:00{time_string}"
    elif len(time_string) == 4:
        time_string = f"00:0{time_string}"
    elif len(time_string) == 5:
        time_string = f"00:{time_string}"
    elif len(time_string) == 6:
        time_string = f"00{time_string}"
    elif len(time_string) == 7:
        time_string = f"0{time_string}"
    elif len(time_string) > 8:
        raise('Time string too long!')
    return time_string


def make_time(parsed_file):
    """
    Function that makes sure the time format is in 00:00:00
    Else changes the time format into that
    Takes the output from the parser(filename) func
    """

    # Different ways to say end
    end = ['slut', 'end', 'tail', 'finish',
           'finito', 'fin', 'done', 'finished']

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

    # Replace . with : for datetime calculations
    for time in split_times:
        time[0] = time[0].replace(".", ":")
        time[1] = time[1].replace(".", ":")

        # Change the time into the correct format by tedious if else statements. Assumes at least 1 character that is a second.
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
        if not time[1].lower() in end:
            last = time[1].split(":")
        # Make a datetime object so we can perform calculations (date is irrelevant)
        starts = datetime.datetime(2019, 1, 1, int(
            first[0]), int(first[1]), int(first[2]))
        if last:
            ends = datetime.datetime(2019, 1, 1, int(
                last[0]), int(last[1]), int(last[2]))
        # Perform calculations and if start is already at 00:00:00 do nothing
        starts -= add_sub
        start_delta = str(starts).split()[1]
        start_delta = start_delta.split(":")
        # For ffmpeg you give start time and then run time (not end time)
        offset = datetime.timedelta(hours=int(start_delta[0]), minutes=int(
            start_delta[1]), seconds=int(start_delta[2]))
        if last:
            ends += add_sub
            # This is how long the clip should be
            ends -= offset
        # Assign new intervals
            time[1] = str(ends).split()[1]
        starts = str(starts).split()
        if starts[1] != "23:59:59":
            time[0] = starts[1]

    # Zip the two lists together. But return a list of this, since a zip object can only be used once.
    zipped = zip(links, split_times)

    return list(zipped), whole_clip


def download_whole(link, playlist):
    """
    Function that downloads a whole video when no interval is supplied
    Downloaded to the same place where yt_vids is saved to (from save_link_time func)
    """

    SAVE_PATH = 'content'
    if playlist:
        ydl_opts = {"nocheckcertificate": True, "noplaylist": False, "ignoreerrors": True,
                'outtmpl': f'{SAVE_PATH}/%(title)s.%(ext)s',
                'format': 'bestvideo[ext=mp4][vcodec!*=av01]+bestaudio[ext=m4a]'}
    else:
        ydl_opts = {"nocheckcertificate": True, "noplaylist": True,
                'outtmpl': f'{SAVE_PATH}/%(title)s.%(ext)s',
                'format': 'bestvideo[ext=mp4][vcodec!*=av01]+bestaudio[ext=m4a]'}
                
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except yt_dlp.utils.ExtractorError or yt_dlp.utils.DownloadError:
            print(f"Couldn't download {link}")


def download_interval(link):
    """
    Function to download videos in specified intervals
    Takes a list (link) and a path as inputs
    """

    end = ['slut', 'end', 'tail', 'finish',
           'finito', 'fin', 'done', 'finished']

    try:
        video = pafy.new(link[0], ydl_opts={
            'nocheckcertificate': True, "noplaylist": True})
        # Only downloads the video if the video hasn't been downloaded before
        if not os.path.exists(os.path.join("content", f"{video.title}.mp4")):
            video_s = video.getbestvideo()
            # TODO: add a way to get the second best stream (third etc.) when an error occurs using Pafy.videostreams and going through the list
            video_a = video.getbestaudio()

            # Checks if the end point is a string
            if link[1][1].lower() in end:
                # Where is the stream, where should we start, how long should it run
                mp4_vid = ffmpeg.input(
                    video_s.url, ss=link[1][0], t=video.duration)
                mp4_aud = ffmpeg.input(
                    video_a.url, ss=link[1][0], t=video.duration)
            else:
                # Where is the stream, where should we start, how long should it run
                mp4_vid = ffmpeg.input(
                    video_s.url, ss=link[1][0], t=link[1][1])
                mp4_aud = ffmpeg.input(
                    video_a.url, ss=link[1][0], t=link[1][1])

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
                    .output(os.path.join("content", f'{video.title}.mp4'))
                    .run()
                )
            except TypeError as e:
                print(f"An error occurred e 0: {e}")
            except ffmpeg._run.Error as e:
                print(f"An error occurred e 1: {e}")
    except Exception as e:
        print(f"I couldn't download {link} due to: {e}")


def download_pics(pics_link):
    """
    Function to download pictures from the input sequence
    """

    r = requests.get(pics_link[0])
    name = pics_link[0].split('/')[-1]
    with open(os.path.join("content", f"{name}"), "wb") as dl:
        dl.write(r.content)

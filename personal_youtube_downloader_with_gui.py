# cd C:\Users\Bryan Leung\Desktop\youtube_downloaders\personal_youtube_downloader_with_gui

import requests
import math
import os
import sys
import subprocess
import json
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from pathlib import Path

"""
    Lots of code taken from youtube downloader and converter for levi project
    This is my own personal one

    By default:
    1. Downloads videos into .mp4 format, into raw_downloads folder

    Features and options:
    1. Convert to mp3
    2a. Download a playlist
    2b. Download a playlist, and convert all videos to audio
    3. Can queue up multiple ones



    Python GUI stuff
    https://realpython.com/python-gui-tkinter/
    https://blog.resellerclub.com/the-6-best-python-gui-frameworks-for-developers/
    https://dev.to/codesharedot/best-python-framework-for-building-a-desktop-application-and-gui-58n5
    https://medium.com/teamresellerclub/the-6-best-python-gui-frameworks-for-developers-7a3f1a41ac73

    Reddit links:
    https://www.reddit.com/r/Python/comments/a9t69r/what_is_your_goto_fast_and_quick_python_gui/
    https://www.reddit.com/r/learnpython/comments/8v3d0d/what_is_the_best_gui_for_python/
    https://www.reddit.com/r/learnpython/comments/5s9al6/creating_a_gui_in_python/

    GUI Builders:
    https://softwarerecs.stackexchange.com/questions/32612/gui-drag-drop-style-gui-builder-for-python-tkinter
    https://www.reddit.com/r/Python/comments/acm67i/best_gui_builder_for_2019/

    Using:
    Qt Designer

    Install:
    https://build-system.fman.io/qt-designer-download

    Tutorial:
    https://www.learnpyqt.com/courses/qt-creator/first-steps-qt-creator/

    Turn pyqt script (.py) --> executable
    https://stackoverflow.com/questions/5888870/how-do-i-compile-a-pyqt-script-py-to-a-single-standalone-executable-file-for
    
"""



#Directories
root_dir = "C:\\Users\\Bryan Leung\\Desktop\\youtube_downloaders\\personal_youtube_downloader_with_gui\\"
raw_downloads_folder = "raw_downloads\\"
converted_folder = "converted\\"


def convert_file_to_mp3(videoname, downloaded_filepath, converted_filepath):
    print("Converting: ", videoname)
    print("downloaded_filepath: ", downloaded_filepath)
    print("converted_filepath: ", converted_filepath)
    subprocess.run(["ffmpeg", "-i", downloaded_filepath, "-f", "mp3", converted_filepath])



def get_yt_title(url):
    """
        https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
        https://stackoverflow.com/questions/32754229/python-and-beautifulsoup-opening-pages
        https://stackoverflow.com/questions/51233/how-can-i-retrieve-the-page-title-of-a-webpage-using-python
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features="lxml")
        title = str(soup.title.string)
        title = title.split(" - YouTube")[0]
        return title
    except Exception as e:
        print(e)


def get_title_of_youtube_video_bs4(url):
    title = None
    found_title = False
    while not found_title:
        title = get_yt_title(url)
        print("Found title %s for url %s" % (title, url))
        found_title = (title != "YouTube")      #If title of Youtube video == "Youtube", then there was an error, so try again

    return title


def get_filenames_of_files_in_directory(directory_filepath):
    return [str(f) for f in listdir(directory_filepath) if isfile(join(directory_filepath, f))]


def get_filenames_of_mp4_files_in_directory(directory_filepath):
    return [f[:f.find(".mp4")] for f in get_filenames_of_files_in_directory(directory_filepath)]




def download_youtube_video(url, convert_to_mp3=False):
    #Find title
    title = get_title_of_youtube_video_bs4(url)


    #Download using Youtube-dl
    relative_dl_path = raw_downloads_folder + title + ".%(ext)s"

    video_has_downloaded = False
    while not video_has_downloaded:
        video_has_downloaded = download_video_using_youtube_dl(title, url, relative_dl_path)

    #Convert to mp3 if option specified
    if convert_to_mp3:
        downloaded_filepath = root_dir + raw_downloads_folder + title + ".mp4"
        converted_filepath = root_dir + converted_folder + title + ".mp3"
        convert_file_to_mp3(title, downloaded_filepath, converted_filepath)

    return video_has_downloaded


def download_video_using_youtube_dl(title, url, path):
    print("Downloading video with title %s with url %s" % (title, url))
    download_successful = True
    try:
        subprocess.run(["youtube-dl", "--verbose", "-f", 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', url, "-o", path])
    except Exception as e:
        print(e)
        print("\n\nFAIL: Downloading video %s with url %s" % (title, url))
        download_successful = False

    return download_successful



def download_youtube_playlist(playlist_url, convert_all_to_mp3=False):
    #Find title
    title = get_title_of_youtube_video_bs4(playlist_url)

    #Download playlist using Youtube-dl
    #https://askubuntu.com/questions/694848/how-to-download-a-youtube-playlist-with-numbered-prefix-via-youtube-dl
    playlist_folder_path = title + "\\"
    raw_downloads_playlist_folder_path = raw_downloads_folder + playlist_folder_path

    relative_dl_path = raw_downloads_playlist_folder_path + "%(playlist_index)s-%(title)s.%(ext)s"
    print("Folder to download playlist into: ", relative_dl_path)

    video_has_downloaded = False
    while not video_has_downloaded:
        video_has_downloaded = download_playlist_using_youtube_dl(title, playlist_url, relative_dl_path)


    #Convert all to mp3 if option specified
    if convert_all_to_mp3:
        #https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
        #Create folder inside converted folder, if it doesn't already exist
        converted_playlist_folder_path = converted_folder + playlist_folder_path
        Path(converted_playlist_folder_path).mkdir(parents=True, exist_ok=True)

        #Get titles of all videos in playlist folder inside raw_downloads
        filenames = get_filenames_of_mp4_files_in_directory(raw_downloads_playlist_folder_path)

        #Convert each mp4 from raw_downloads/<playlist_name> --> to an mp3 in converted/<playlist_name>
        for filename in filenames:
            downloaded_filepath = root_dir + raw_downloads_playlist_folder_path + filename + ".mp4"
            converted_filepath = root_dir + converted_playlist_folder_path + filename + ".mp3"
            convert_file_to_mp3(title, downloaded_filepath, converted_filepath)


    return video_has_downloaded

def download_playlist_using_youtube_dl(title, playlist_url, youtube_dl_path):
    """
        https://stackoverflow.com/questions/48422377/youtube-downloading-a-playlist-youtube-dl
    """
    print("Downloading youtube playlist with title %s with url %s" % (title, playlist_url))
    download_successful = True
    try:
        subprocess.run(["youtube-dl", "--verbose", "-i", "-f", 'mp4', "--yes-playlist", playlist_url, "-o", youtube_dl_path])
    except Exception as e:
        print(e)
        print("\n\nFAIL: Downloading playlist %s with url %s" % (title, playlist_url))
        download_successful = False

    return download_successful




def download(url, is_playlist=False, convert_to_mp3=False):
    if is_playlist:
        download_youtube_playlist(url, convert_all_to_mp3=convert_to_mp3)
    else:
        download_youtube_video(url, convert_to_mp3=convert_to_mp3)



if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=2XGYr9_BiEU"     #ep 1
    #url = "https://www.youtube.com/watch?v=9EceEemWo0k"     #ep 3
    #url = "https://www.youtube.com/watch?v=Xy2L3dHWZkI"     #test
    #url = "https://www.youtube.com/watch?v=lRXDeMBfvMk"
    url = "https://www.youtube.com/watch?v=OZa3HyVLimQ"
    download_youtube_video(url, convert_to_mp3=True)

    #playlist_url = "https://www.youtube.com/playlist?list=PLv9iVPU7Da8pJveNqzttL-6VDFK1dg16-"
    #download_youtube_playlist(playlist_url, convert_all_to_mp3=True)

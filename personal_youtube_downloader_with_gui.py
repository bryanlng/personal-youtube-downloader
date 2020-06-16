# cd C:\Users\Bryan Leung\Desktop\youtube_downloaders\personal_youtube_downloader_with_gui

import requests
import math
import os
import sys
import subprocess
import json
from bs4 import BeautifulSoup

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
"""



#Directories
root_dir = "C:\\Users\\Bryan Leung\\Desktop\\youtube_downloaders\\personal_youtube_downloader_with_gui\\"
youtube_dl_path = root_dir
raw_downloads_folder = "raw_downloads\\"
converted_folder = "converted\\"


def convert_to_mp3(videoname, downloaded_filepath, converted_filepath):
    print("Converting: ", videoname)
    print("downloaded_filepath: ", downloaded_filepath)
    print("converted_filepath: ", converted_filepath)
    subprocess.run(["ffmpeg", "-i", downloaded_filepath, "-f", "mp3", converted_filepath])




def get_title_of_youtube_video_bs4(url):
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




def download_youtube_video(url):
    #Find title
    title = get_title_of_youtube_video_bs4(url)


    #Download using Youtube-dl
    youtube_dl_path = raw_downloads_folder + title + ".%(ext)s"

    video_has_downloaded = False
    while not video_has_downloaded:
        video_has_downloaded = download_video_using_youtube_dl(title, url, youtube_dl_path)

    downloaded_filepath = root_dir + raw_downloads_folder + videoname + ".mp4"
    converted_filepath = root_dir + converted_folder + videoname + ".mp3"

    convert_to_mp3(title, downloaded_filepath, converted_filepath)


def download_video_using_youtube_dl(title, url, path):
    print("Downloading video with title %s with url %s" % (title, url))
    download_successful = True
    try:
        subprocess.run(["youtube-dl", "--verbose", "-f", 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', url, "-o", path])
    except Exception as e:
        print(e)
        print("\n\nFAIL: Downloading song %s with url %s" % (songname, url))
        download_successful = False

    return download_successful



def download_youtube_playlist(playslist_url):
    #Find title
    title = get_title_of_youtube_video_bs4(playslist_url)


    #Download using Youtube-dl
    youtube_dl_path = raw_downloads_folder

    video_has_downloaded = False
    while not video_has_downloaded:
        video_has_downloaded = download_playlist_using_youtube_dl(title, playslist_url, youtube_dl_path)



def download_playlist_using_youtube_dl(playlist_url):
    """
        https://stackoverflow.com/questions/48422377/youtube-downloading-a-playlist-youtube-dl
    """
    print("Downloading youtube playlist with title %s with url %s" % (title, url))
    download_successful = True
    try:
        subprocess.run(["youtube-dl", "--verbose", "-i", "-f", 'mp4', "--yes-playlist", playlist_url, "-o", path])
    except Exception as e:
        print(e)
        print("\n\nFAIL: Downloading song %s with url %s" % (songname, url))
        download_successful = False

    return download_successful






if __name__ == "__main__":
    #url = "https://www.youtube.com/watch?v=2XGYr9_BiEU"     #ep 1
    #url = "https://www.youtube.com/watch?v=9EceEemWo0k"     #ep 3
    #url = "https://www.youtube.com/watch?v=Xy2L3dHWZkI"     #test
    url = "https://www.youtube.com/watch?v=lRXDeMBfvMk"
    download_youtube_video(url)

    #playlist_url =

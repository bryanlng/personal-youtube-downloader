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
        found_title = (title != "Youtube")      #If title of Youtube video == "Youtube", then there was an error, so try again

    return title



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



def download_youtube_playlist(playlist_url, convert_all_to_mp3=False):
    #Find title
    title = get_title_of_youtube_video_bs4(playlist_url)

    #Download using Youtube-dl
    relative_dl_path = raw_downloads_folder + title + "\\" + "%(playlist_index)s-%(title)s.%(ext)s"
    print("Folder to download playlist into: ", relative_dl_path)

    video_has_downloaded = False
    while not video_has_downloaded:
        video_has_downloaded = download_playlist_using_youtube_dl(title, playlist_url, relative_dl_path)


    #Convert all to mp3 if option specified
    """
    if convert_all_to_mp3:
        downloaded_filepath = root_dir + raw_downloads_folder + title + ".mp4"
        converted_filepath = root_dir + converted_folder + title + ".mp3"
        convert_file_to_mp3(title, downloaded_filepath, converted_filepath)
    """


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
        print("\n\nFAIL: Downloading song %s with url %s" % (songname, playlist_url))
        download_successful = False

    return download_successful






if __name__ == "__main__":
    #url = "https://www.youtube.com/watch?v=2XGYr9_BiEU"     #ep 1
    #url = "https://www.youtube.com/watch?v=9EceEemWo0k"     #ep 3
    #url = "https://www.youtube.com/watch?v=Xy2L3dHWZkI"     #test
    #url = "https://www.youtube.com/watch?v=lRXDeMBfvMk"
    #download_youtube_video(url, convert_to_mp3=True)

    playlist_url = "https://www.youtube.com/playlist?list=PLv9iVPU7Da8pJveNqzttL-6VDFK1dg16-"
    download_youtube_playlist(playlist_url)

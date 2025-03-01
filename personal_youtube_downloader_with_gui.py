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
import lxml.html
from pathlib import Path
import re
import time
import random

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

    On button click stuff:
    https://stackoverflow.com/questions/18041876/how-to-define-an-onclick-event-handler-for-a-button-from-within-qt-creator
    Uses signals, slots,
    https://doc.qt.io/qt-5/signalsandslots.html

    Slot = function it calls()

    Turn pyqt script (.py) --> executable
    https://stackoverflow.com/questions/5888870/how-do-i-compile-a-pyqt-script-py-to-a-single-standalone-executable-file-for

"""



#Directories
# root_dir = "C:\\Users\\Bryan Leung\\Desktop\\youtube_downloaders\\personal_youtube_downloader_with_gui\\" # old path on lenovo G50 laptop
# root_dir = "C:\\Users\\bleun\\Documents\\youtube_downloaders\\personal_youtube_downloader_with_gui\\" # old path on Lenovo flex 5 laptop
root_dir = "C:\\Users\\bleun\\OneDrive\\Desktop\\youtube_downloaders\\personal_youtube_downloader_with_gui\\"
raw_downloads_folder = "raw_downloads\\"
converted_folder = "converted\\"


def convert_file_to_mp3(videoname, downloaded_filepath, converted_filepath):
    print("Converting: ", videoname)
    print("downloaded_filepath: ", downloaded_filepath)
    print("converted_filepath: ", converted_filepath)
    subprocess.run(["ffmpeg", "-i", downloaded_filepath, "-f", "mp3", converted_filepath])



def get_yt_title_method(url, method_type=None):
    """
        https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
        https://stackoverflow.com/questions/32754229/python-and-beautifulsoup-opening-pages
        https://stackoverflow.com/questions/51233/how-can-i-retrieve-the-page-title-of-a-webpage-using-python

        https://stackoverflow.com/questions/36108621/get-all-html-tags-with-beautiful-soup
        https://stackoverflow.com/questions/36768068/get-meta-tag-content-property-with-beautifulsoup-and-python
    """
    title = None

    try:
        if method_type == "LXML_TITLE_SCRAPE":
            r = requests.get(url)
            soup = BeautifulSoup(r.content, features="lxml")
            title = str(soup.title.string)
            title = title.split(" - YouTube")[0]
        elif method_type == "BS4_META_TAG_CONTENT_SCRAPE":
            #Title is sometimes in the meta tag
            #<meta content="Hayao Miyazaki - The Essence of Humanity ^^!!" itemprop="name"/>
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            meta_tag_with_title_inside = soup.find("meta",  itemprop="name")
            title = meta_tag_with_title_inside["content"] if meta_tag_with_title_inside else "No meta title given"

    except Exception as e:
        print(e)


    return title



def get_title_of_youtube_video_bs4(url):
    title = None
    found_title = False
    method_counter = 0
    method_iteration_counter = 0
    method_iteration_timeout_limit = 10
    methods = ["LXML_TITLE_SCRAPE", "BS4_META_TAG_CONTENT_SCRAPE"]


    #Attempt each method
    while not found_title and method_counter < len(methods):

        current_method = methods[method_counter]
        print("Trying method: ", current_method)

        #Attempt each method 20 times
        while not found_title and method_iteration_counter < method_iteration_timeout_limit:
            title = get_yt_title_method(url, current_method)
            print("Found title %s for url %s" % (title, url))
            found_title = (title is not None and title != "YouTube")      #If title of Youtube video == "Youtube", then there was an error, so try again
            method_iteration_counter += 1

        #If we still haven't found the title, but our counter expired, go to new method, then reset it
        if not found_title:
            method_counter += 1
            method_iteration_counter = 0

    #If we still haven't found the title, give up and just default to "no_title_found"
    if not found_title:
        title = "no_title_found"

    return title


def get_filenames_of_files_in_directory(directory_filepath):
    return [str(f) for f in listdir(directory_filepath) if isfile(join(directory_filepath, f))]


def get_filenames_of_mp4_files_in_directory(directory_filepath):
    return [f[:f.find(".mp4")] for f in get_filenames_of_files_in_directory(directory_filepath)]



def clean_string(title):
    """
        https://stackoverflow.com/questions/2758921/regular-expression-that-finds-and-replaces-non-ascii-characters-with-python
        https://support.tresorit.com/hc/en-us/articles/216114167-Fixing-invalid-characters-and-colliding-file-names
        https://stackoverflow.com/questions/15658187/replace-all-words-from-word-list-with-another-string-in-python

        Cleans up the title

        Removes any:
        1. Non-ascii (unicode) string
        2. Certain ASCII chars that cause issues with window's file naming, such as:
            " (double quote), * (asterisk), < (less than), > (greater than), ? (question mark), \ (backslash), | (pipe), / (forward slash), : (colon)
            The filename can’t end with a space or a period
            The filename can’t contain any of the names reserved by Windows
                CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, and LPT9
    """
    print("Original title: ", title)
    #1. Remove non-ascii chars
    title = title.encode().decode('ascii', 'replace').replace(u'\ufffd', '')

    #2. Remove all bad ascii chars
    prohibited_ascii_chars = ['\"', '*', '<', '>', '?', '\\', '|', '/', ':', '.']
    windows_reserved_words = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
    prohibited_words = prohibited_ascii_chars + windows_reserved_words
    big_regex = re.compile('|'.join(map(re.escape, prohibited_words)))
    title = big_regex.sub("", title)

    #3. Check if last char of the title is a space or period. If so, remove
    last_char = title[-1]
    if last_char == " " or last_char == ".":
        title = title[:len(title)-1]


    print("Cleaned title: ", title)
    return title


def download_youtube_video(url, convert_to_mp3=False):
    #Find title
    title = get_title_of_youtube_video_bs4(url)

    #Clean title
    title = clean_string(title)

    #Download using yt-dlp
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
    print("Downloading video with title %s with url %s at path %s" % (title, url, path))
    download_successful = True
    try:
        # subprocess.run(["yt-dlp", "--verbose", "-f", 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', url, "-o", path])
        subprocess.run(["yt-dlp", "--verbose", "-f", 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',"-o", path, url])
    except Exception as e:
        print(e)
        print("\n\nFAIL: Downloading video %s with url %s" % (title, url))
        download_successful = False

    return download_successful



def download_youtube_playlist(playlist_url, convert_all_to_mp3=False):
    #Find title
    title = get_title_of_youtube_video_bs4(playlist_url)

    #Clean title
    title = clean_string(title)

    #Download playlist using yt-dlp
    #https://askubuntu.com/questions/694848/how-to-download-a-youtube-playlist-with-numbered-prefix-via-yt-dlp
    playlist_folder_path = title + "\\"
    raw_downloads_playlist_folder_path = raw_downloads_folder + playlist_folder_path

    #Create folder inside raw_downloads folder, if it doesn't already exist
    Path(raw_downloads_playlist_folder_path).mkdir(parents=True, exist_ok=True)

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
        https://stackoverflow.com/questions/48422377/youtube-downloading-a-playlist-yt-dlp
    """
    print("Downloading youtube playlist with title %s with url %s" % (title, playlist_url))
    download_successful = True
    try:
        subprocess.run(["yt-dlp", "--verbose", "-i", "-f", 'mp4', "--yes-playlist", "--retries", "infinite", "--limit-rate", "10000000", playlist_url, "-o", youtube_dl_path])
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


def download_list_of_videos(video_list):
    for url in video_list:
        download_youtube_video(url, convert_to_mp3=True)
        sleep(30, 20)


def download_list_of_playlists(playlist_list):
    for url in playlist_list:
        download_youtube_playlist(url, convert_all_to_mp3=False)

def sleep(base, range):
    time_to_sleep = base + random.randit(0, range)
    time.sleep(time_to_sleep)

if __name__ == "__main__":
    # url = "https://www.youtube.com/watch?v=o__NzkmLZoM"
    # download_youtube_video(url, convert_to_mp3=True)

    # video_list = [
    #     "https://www.youtube.com/watch?v=KsJ840J2iSY"
    # ]
    # download_list_of_videos(video_list)

    # playlist_list = [
    #     "https://www.youtube.com/playlist?list=PLMFGVXWuJ1C5JrEgn8FwS8rgDHvcgNsMS"
    # ]
    # download_list_of_playlists(playlist_list)

    playlist_url = "https://www.youtube.com/playlist?list=PLSaKzxcdPI4b12BxTxg4ux-xXMz6KW5vq"
    download_youtube_playlist(playlist_url, convert_all_to_mp3=True)

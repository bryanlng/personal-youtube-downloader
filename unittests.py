import unittest
import personal_youtube_downloader_with_gui
import os.path
from os import path

#Directories
root_dir = "C:\\Users\\Bryan Leung\\Desktop\\youtube_downloaders\\personal_youtube_downloader_with_gui\\"
raw_downloads_folder = "raw_downloads\\"
converted_folder = "converted\\"

#downloaded_filepath = root_dir + raw_downloads_folder + title + ".mp4"
#converted_filepath = root_dir + converted_folder + title + ".mp3"


class TestYoutubeDownloader(unittest.TestCase):
    def delete_videos_after_test(self, filepaths_to_delete):
        """
            filepaths_to_delete:        list of str representing filepaths to delete
        """
        for filepath in filepaths_to_delete:
            os.remove(filepath)



    def test_get_title_of_youtube_video_bs4(self):
        url = "https://www.youtube.com/watch?v=Xy2L3dHWZkI"
        correct_title = "Kids Slams Into Wall"

        found_title = personal_youtube_downloader_with_gui.get_title_of_youtube_video_bs4(url)
        self.assert(found_title, correct_title)


    def test_download_youtube_video_default(self):
        url = "https://www.youtube.com/watch?v=Xy2L3dHWZkI"
        video_has_downloaded = personal_youtube_downloader_with_gui.download_youtube_video(url)

        #Validate that the file exists
        title = "Kids Slams Into Wall"
        correct_file_path = root_dir + raw_downloads_folder + title + ".mp4"
        self.assertTrue(path.exists(correct_file_path))

        #Remove video
        #filepaths_to_delete = [correct_file_path]
        #self.delete_videos_after_test(filepaths_to_delete)


    def test_download_youtube_video_also_convert_to_mp3(self):
        url = "https://www.youtube.com/watch?v=Xy2L3dHWZkI"
        video_has_downloaded = personal_youtube_downloader_with_gui.download_youtube_video(url, convert_to_mp3=True)

        #Validate that the file exists
        title = "Kids Slams Into Wall"
        correct_download_file_path = root_dir + raw_downloads_folder + title + ".mp4"
        correct_converted_file_path = root_dir + converted_folder + title + ".mp3"

        self.assertTrue(path.exists(correct_download_file_path))
        self.assertTrue(path.exists(correct_converted_file_path))

        #Remove video
        #filepaths_to_delete = [correct_file_path]
        #self.delete_videos_after_test(filepaths_to_delete)



if __name__ == '__main__':
    unittest.main()

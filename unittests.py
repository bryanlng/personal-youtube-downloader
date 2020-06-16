import unittest
import personal_youtube_downloader_with_gui
import os.path
from os import path
import shutil

#Directories
root_dir = "C:\\Users\\Bryan Leung\\Desktop\\youtube_downloaders\\personal_youtube_downloader_with_gui\\"
raw_downloads_folder = "raw_downloads\\"
converted_folder = "converted\\"

#downloaded_filepath = root_dir + raw_downloads_folder + title + ".mp4"
#converted_filepath = root_dir + converted_folder + title + ".mp3"


class TestYoutubeDownloader(unittest.TestCase):
    def delete_videos_after_test(self, delete_file=False, delete_whole_directory=False, files_to_delete = [], directories_to_delete = []):
        """
            https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder
            filepaths_to_delete:        list of str representing filepaths to delete
        """
        if delete_file:
            for filepath in files_to_delete:
                os.remove(filepath)

        if delete_whole_directory:
            for directory in directories_to_delete:
                shutil.rmtree(directory)


    @unittest.skip("reason for skipping")
    def test_get_title_of_youtube_video_bs4(self):
        url = "https://www.youtube.com/watch?v=Xy2L3dHWZkI"
        correct_title = "Kids Slams Into Wall"

        found_title = personal_youtube_downloader_with_gui.get_title_of_youtube_video_bs4(url)
        self.assertEquals(found_title, correct_title)



    #@unittest.skip("reason for skipping")
    def test_download_youtube_video_default(self):
        url = "https://www.youtube.com/watch?v=Xy2L3dHWZkI"
        video_has_downloaded = personal_youtube_downloader_with_gui.download_youtube_video(url)

        #Validate that the file exists
        title = "Kids Slams Into Wall"
        correct_file_path = root_dir + raw_downloads_folder + title + ".mp4"
        self.assertTrue(path.exists(correct_file_path))

        #Remove video
        self.delete_videos_after_test(delete_file=True, files_to_delete=[correct_file_path])



    #@unittest.skip("reason for skipping")
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
        self.delete_videos_after_test(delete_file=True, files_to_delete=[correct_download_file_path, correct_converted_file_path])



    @unittest.skip("reason for skipping")
    def test_download_youtube_playlist_default(self):
        url = "https://www.youtube.com/playlist?list=PLv9iVPU7Da8pJveNqzttL-6VDFK1dg16-"
        video_has_downloaded = personal_youtube_downloader_with_gui.download_youtube_playlist(url)

        #Validate that the folder exists
        title = "The National Children's Orchestras of Great Britain"
        playlist_folder_path = title + "\\"
        raw_downloads_playlist_folder_path = raw_downloads_folder + playlist_folder_path
        correct_file_path = root_dir + raw_downloads_playlist_folder_path
        self.assertTrue(path.exists(correct_file_path))

        #Validate that files exist within the folder
        filenames = personal_youtube_downloader_with_gui.get_filenames_of_mp4_files_in_directory(correct_file_path)
        self.assertTrue(len(filenames) > 0)

        #Remove all videos
        filepaths_to_delete = [correct_file_path + filename + ".mp4" for filename in filenames]
        self.delete_videos_after_test(filepaths_to_delete)



    @unittest.skip("reason for skipping")
    def test_download_youtube_playlist_also_convert_to_mp3(self):
        url = "https://www.youtube.com/playlist?list=PLv9iVPU7Da8pJveNqzttL-6VDFK1dg16-"
        video_has_downloaded = personal_youtube_downloader_with_gui.download_youtube_playlist(url, convert_all_to_mp3=True)

        #Validate that folder exists in both the downloads and converted folder
        title = "The National Children's Orchestras of Great Britain"
        playlist_folder_path = title + "\\"
        raw_downloads_playlist_folder_path = raw_downloads_folder + playlist_folder_path
        converted_playlist_folder_path = converted_folder + playlist_folder_path

        correct_downloads_file_path = root_dir + raw_downloads_playlist_folder_path
        correct_converted_file_path = root_dir + converted_playlist_folder_path

        self.assertTrue(path.exists(correct_downloads_file_path))
        self.assertTrue(path.exists(correct_converted_file_path))

        #Validate that files exist within the downloads folder
        download_filenames = personal_youtube_downloader_with_gui.get_filenames_of_mp4_files_in_directory(correct_downloads_file_path)
        self.assertTrue(len(download_filenames) > 0)

        #Validate that files exist within the downloads folder
        converted_filenames = personal_youtube_downloader_with_gui.get_filenames_of_files_in_directory(correct_converted_file_path)
        self.assertTrue(len(converted_filenames) > 0)

        #Validate that # of files in downloads folder == # of files in converted folder
        self.assertEqual(download_filenames, converted_filenames)

        #Remove all videos
        downloads_filepaths_to_delete = [correct_downloads_file_path + filename + ".mp4" for filename in download_filenames]
        converted_filepaths_to_delete = [correct_converted_file_path + filename + ".mp3" for filename in converted_filenames]
        filepaths_to_delete = downloads_filepaths_to_delete + converted_filepaths_to_delete
        self.delete_videos_after_test(filepaths_to_delete)



if __name__ == '__main__':
    unittest.main()

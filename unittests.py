import unittest
import personal_youtube_downloader_with_gui

class TestYoutubeDownloader(unittest.TestCase):

    def test_download_youtube_video_default(self):
        url = "https://www.youtube.com/watch?v=2XGYr9_BiEU"     #ep 1
        video_has_downloaded = download_youtube_video(url)

        #Validate that the file exists


if __name__ == '__main__':
    unittest.main()

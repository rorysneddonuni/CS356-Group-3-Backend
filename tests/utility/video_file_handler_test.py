import os
import unittest

import cv2
import app.services.utility.video_file_handler as video_file_handler


class Test_video_file_handler(unittest.TestCase):
    def test_store_video(self):
        self.test_filename = "test.mp4"
        self.test_output_filename = "testVideo.mp4"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

        video = cv2.VideoCapture('test.mp4')
        video_file_handler.store_video_file(video, self.test_output_filename, "mp4v", 30)

        self.assertTrue(os.path.exists(self.test_output_filename))
        os.remove(self.test_output_filename)

    def test_delete_video(self):
        self.test_output_filename = "testVideo.mp4"
        video_file_handler.delete_video_file(self.test_output_filename)
        self.assertFalse(os.path.exists(self.test_output_filename))

    def test_retrieve_video(self):
        self.test_output_filename = "testVideo.mp4"
        output = video_file_handler.retrieve_video_file(self.test_output_filename)
        self.assertTrue(output.isOpened)
        output.release()



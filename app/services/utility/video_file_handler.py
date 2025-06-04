import os
import shutil

import cv2


def store_video_file(video, file_path, filename):
    path = os.path.join(file_path, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(video, buffer)
    return {"filename": filename, "saved_to": file_path}

def delete_video_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The video file does not exist")

def retrieve_video_file(file_path):
    return open(file_path, 'rb')

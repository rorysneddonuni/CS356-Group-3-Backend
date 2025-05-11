import os
import cv2

video_file_dir = "app/database/videos"

def store_video_file(video, file_name, file_type):
    # https://www.geeksforgeeks.org/saving-a-video-using-opencv/
    file = video_file_dir + file_name
    if video.isOpened() == False:
        print("Error reading video file")
    result = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*file_type), 10)

    while (True):
        ret, frame = video.read()
        if ret == True:
            result.write(frame)
            cv2.imshow('Frame', frame)
        else:
            break

    video.release()
    result.release()
    cv2.destroyAllWindows()

def delete_video_file(file_name):
    file = video_file_dir + file_name
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The video file does not exist")

def retrieve_video_file(file_name):
    return open(video_file_dir + file_name, "r")

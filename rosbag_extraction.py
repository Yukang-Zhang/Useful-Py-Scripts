import rosbag
import rospy
from std_msgs.msg import String
import sys
import cv2
from cv_bridge import CvBridge
import os
import numpy as np
from datetime import datetime, timedelta
import ffmpeg


def nanoseconds_to_datetime(ns):
    epoch = datetime(1970, 1, 1)
    seconds = ns / 1e9
    return epoch + timedelta(seconds=seconds)

def read_rosbag(bag_path):
    # 打开bag文件
    bag = rosbag.Bag(bag_path)
    
    try:
        # 遍历所有的消息
        for topic, msg, t in bag.read_messages():
            if topic == '/C/Camera/NearRangeFront':
                image_data = [int(x) for x in (str(msg).split(': ')[-1][1:-1].split(', '))]
                
                date_time = nanoseconds_to_datetime(int(str(t)))

                datetime1 = datetime(2024, 5, 24, 3, 43, 41)
                datetime2 = datetime(2024, 5, 24, 3, 43, 43)

                # print("F")
                # print(date_time)

                
                
                if date_time < datetime1:
                    continue
                if date_time > datetime2:
                    break
                

                print('Time: ' + str(date_time))
                
                byte_stream = bytes(image_data)

                output_filename = 'output_image' + str(date_time) + '.jpg'
                # output_filename = 'output_image.jpg'


                with open(output_filename, 'wb') as file:
                    file.write(byte_stream)


                
                '''
                
                cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
                cv2.moveWindow('Image', 100, 100)
                cv2.resizeWindow('Image', 800, 600)
                image = cv2.imread('output_image.jpg')
                cv2.imshow('Image', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                '''

                # os.remove('output_image.jpg')
    finally:
        # 关闭bag文件
        bag.close()

def convert_jpg_to_yuv(input_image_path, output_yuv_path, pix_fmt='yuv422p'):
    try:
        stream = ffmpeg.input(input_image_path)
        stream = ffmpeg.output(stream, output_yuv_path, pix_fmt=pix_fmt)
        ffmpeg.run(stream)
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")


if __name__ == "__main__":
    
    bag_path = 'OT30_2024-05-24-11-43-23.bag'
    with open('ros_output.txt', 'w') as f:
        read_rosbag(bag_path)
    '''
    input_image_path = 'output_image_2024-05-24 034341695884.jpg'
    output_yuv_path = 'out1.yuv'
    convert_jpg_to_yuv(input_image_path, output_yuv_path)

    input_image_path = 'output_image_2024-05-24 034341793374.jpg'
    output_yuv_path = 'out2.yuv'
    convert_jpg_to_yuv(input_image_path, output_yuv_path)
    '''

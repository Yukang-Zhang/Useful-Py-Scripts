import cv2
import numpy as np
import os

def convert_rgb_to_yuv422(frame):
    """
    Convert an RGB frame to YUV422 format.

    :param frame: A numpy array representing the RGB image.
    :return: A numpy array representing the YUV422 image.
    """
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    height, width, _ = frame.shape
    y = yuv[:, :, 0]
    u = yuv[:, :, 1]
    v = yuv[:, :, 2]

    # Subsample U and V channels to get YUV422
    u_sub = u[:, ::2]
    v_sub = v[:, ::2]

    # Interleave Y, U, V to get YUV422 format
    yuv422 = np.zeros((height, width * 2), dtype=np.uint8)
    yuv422[:, 0::2] = y
    yuv422[:, 1::4] = u_sub
    yuv422[:, 3::4] = v_sub

    return yuv422

def save_yuv422_image(yuv_image, output_path):
    """
    Save the YUV422 image to a file.

    :param yuv_image: A numpy array representing the YUV422 image.
    :param output_path: The path to save the YUV422 image.
    """
    with open(output_path, 'wb') as f:
        f.write(yuv_image.tobytes())

def convert_jpg_to_yuv(input_image_path, output_yuv_path):
    """
    Convert a JPG image to YUV422 format and save it.

    :param input_image_path: Path to the input JPG image.
    :param output_yuv_path: Path to save the output YUV422 image.
    """
    # Read the input image
    frame = cv2.imread(input_image_path)
    if frame is None:
        raise FileNotFoundError(f"Image file {input_image_path} not found.")
    
    # Convert the image to YUV422 format
    yuv_image = convert_rgb_to_yuv422(frame)
    
    # Save the YUV422 image
    save_yuv422_image(yuv_image, output_yuv_path)





def convert_rgb_to_y(frame):
    """
    Convert an RGB frame to the Y plane of YUV format.

    :param frame: A numpy array representing the RGB image.
    :return: A numpy array representing the Y plane (grayscale image).
    """
    # Convert RGB to YUV
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    
    # Extract only the Y plane
    y = yuv[:, :, 0]
    
    return y

def save_y_image(y_image, output_path):
    """
    Save the Y plane image to a file.

    :param y_image: A numpy array representing the Y plane image.
    :param output_path: The path to save the Y plane image.
    """
    with open(output_path, 'wb') as f:
        f.write(y_image.tobytes())

def convert_jpg_to_y(input_image_path, output_y_path):
    """
    Convert a JPG image to the Y plane and save it.

    :param input_image_path: Path to the input JPG image.
    :param output_y_path: Path to save the output Y plane image.
    """
    # Read the input image
    frame = cv2.imread(input_image_path)
    if frame is None:
        raise FileNotFoundError(f"Image file {input_image_path} not found.")
    
    # Convert the image to the Y plane
    y_image = convert_rgb_to_y(frame)
    
    # Save the Y plane image
    save_y_image(y_image, output_y_path)


# Example usage
input_image_path = '1.jpg'
output_yuv_path = '1.yuv'
convert_jpg_to_y(input_image_path, output_yuv_path)

# input_image_path = 'frame_0000.jpg'
# output_yuv_path = 'frame_0000.yuv'
# convert_jpg_to_yuv(input_image_path, output_yuv_path)

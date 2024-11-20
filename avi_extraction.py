import cv2
import numpy as np
import os

def convert_rgb_to_yuv422(frame):
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

def add_padding_to_yuv422(image_yuv422, width=1920, height=1536, top_pad=1, bottom_pad=14):
    """
    Add padding to a YUV422 image.

    :param image_yuv422: A numpy array representing the YUV422 image
    :param width: Width of the original image (default 1920)
    :param height: Height of the original image (default 1536)
    :param top_pad: Number of rows to add at the top (default 1)
    :param bottom_pad: Number of rows to add at the bottom (default 14)
    :return: A new numpy array with the padded YUV422 image
    """
    # Calculate size of a frame
    frame_size = width * height * 2
    if image_yuv422.size != frame_size:
        raise ValueError(f"Input size mismatch. Expected size: {frame_size}, got: {image_yuv422.size}")

    # Reshape the input image into (height, width*2) for YUV422 interleaved format
    yuv422_frame = image_yuv422.reshape((height, width * 2))

    # Pad the frame
    top_padding = np.zeros((top_pad, width * 2), dtype=image_yuv422.dtype)
    bottom_padding = np.zeros((bottom_pad, width * 2), dtype=image_yuv422.dtype)
    padded_yuv422_frame = np.vstack((top_padding, yuv422_frame, bottom_padding))

    # Flatten the padded frame back to 1D array
    padded_yuv422 = padded_yuv422_frame.flatten()

    return padded_yuv422

def save_yuv422_frame(yuv_frame, frame_index, output_dir):
    output_file = os.path.join(output_dir, f'frame_{frame_index:04d}.yuv')
    with open(output_file, 'wb') as f:
        f.write(yuv_frame.tobytes())

def extract_frames_to_yuv(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(input_file)
    frame_index = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        yuv_frame = convert_rgb_to_yuv422(frame)
        yuv_frame_padded = add_padding_to_yuv422(yuv_frame)
        save_yuv422_frame(yuv_frame_padded, frame_index, output_dir)
        frame_index += 1

    cap.release()

input_file = 'nrcs_front.avi'
output_dir = 'frames_yuv'

extract_frames_to_yuv(input_file, output_dir)

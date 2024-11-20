import numpy as np
import cv2 as cv
import struct
from PIL import Image

def read_motion_vectors(filename, grid_block_size, img_dims):
    vector_format = 'hh'  # Two shorts (16-bit integers)
    vector_size = struct.calcsize(vector_format)

    out_width, out_height = img_dims[0] // grid_block_size, img_dims[1] // grid_block_size

    motion_vectors = np.zeros((out_height, out_width, 2))

    with open(filename, 'rb') as file:
        for grid_y in range(out_height):
            for grid_x in range(out_width):
                data = file.read(vector_size)
                if not data:
                    break
                packed_x, packed_y = struct.unpack(vector_format, data)
                float_x = packed_x / float(1 << 5)
                float_y = packed_y / float(1 << 5)
                motion_vectors[grid_y, grid_x, :] = [float_x, float_y]

    return motion_vectors

def ofmedian_square(motion_vectors, window_size):
    out_width, out_height = motion_vectors.shape[1], motion_vectors.shape[0]
    
    motion_vectors_new = np.zeros((out_height, out_width, 2))

    for i in range(out_height):
        for j in range(out_width):
            for dim in range(0, 2):
                neighbours = []
                w = 0
                ws = window_size // 2
                for wi in range(-ws, ws + 1):
                    for wj in range(-ws, ws + 1):
                        if wi != 0 and wj != 0:
                            continue
                        x = (i + wi if i + wi >= 0 else 0) if i + wi < out_height else out_height - 1
                        y = (j + wj if j + wj >= 0 else 0) if j + wj < out_width else out_width - 1
                        neighbours.append(motion_vectors[x, y, dim])
                for k in range(window_size):
                    for l in range((window_size * 2) - k - 2):
                        # print(window_size, l, k, "FUCK")
                        if neighbours[l] > neighbours[l + 1]:
                            temp = neighbours[l]
                            neighbours[l] = neighbours[l + 1]
                            neighbours[l + 1] = temp
                motion_vectors_new[i, j, dim] = neighbours[window_size]

    return motion_vectors_new


def draw_motion_vectors(image_dims, motion_vectors, grid_block_size, arrow_spacing, arrow_length_factor=10, arrow_thickness=1):
    # 获取运动矢量数组的宽度和高度
    out_width, out_height = motion_vectors.shape[1], motion_vectors.shape[0]
    
    # 获取输出图像的宽度和高度
    img_height, img_width = image_dims[1], image_dims[0]

    print(out_width, out_height, img_height, img_width)
    
    # 创建一个空的图像，大小为给定的图像尺寸，初始化为黑色
    vector_image = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    
    # 定义颜色列表
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

    # 遍历运动矢量网格，按照给定的箭头间隔
    for grid_y in range(0, out_height, arrow_spacing * 2):  # 每隔一个网格绘制
        for grid_x in range(0, out_width, arrow_spacing * 2):  # 每隔一个网格绘制
            # 计算箭头的起点
            start_point = (grid_x * grid_block_size + grid_block_size // 2, grid_y * grid_block_size + grid_block_size // 2)
            
            # 获取当前网格点的运动矢量
            vector = motion_vectors[grid_y, grid_x]
            
            # 计算矢量的大小（模长）
            magnitude = np.linalg.norm(vector)
            
            # 如果矢量大小大于0，则绘制箭头
            if magnitude > 0:
                # 根据箭头长度因子缩放矢量
                scaled_vector = vector * 2
                
                # 计算箭头的终点
                end_point = (int(start_point[0] + scaled_vector[0]),
                             int(start_point[1] + scaled_vector[1]))
                
                # 选择颜色
                color = colors[(grid_y // arrow_spacing + grid_x // arrow_spacing) % len(colors)]
                
                # 在图像上绘制箭头
                cv.arrowedLine(vector_image, start_point, end_point, color, arrow_thickness, tipLength=0.3)

    return vector_image

def save_motion_vector_image(image, output_file):
    cv.imwrite(output_file, image)

def overlay_images(bg_path, overlay_path, output_path, alpha=0.5):
    bg = Image.open(bg_path).convert("RGBA")
    overlay = Image.open(overlay_path).convert("RGBA")

    overlay = overlay.resize(bg.size, Image.LANCZOS)

    combined = Image.blend(bg, overlay, alpha)
    combined.save(output_path)

def main():

    filename = 'flow1_file.bin'
    bg_path = 'frame_0000.jpg'  # Path to the background image
    output_overlay_path = 'overlay_output0.png'

    grid_block_size = 4
    arrow_spacing = 4  # Increase this value to decrease arrow density
    arrow_length = 0.5  # Length of arrows relative to the grid block size
    arrow_thickness = 2  # Thickness of the arrow lines
    image_dimensions = (1920, 1536)
    output_file = 'motion_vectors_arrows.png'
    window_size = 9

    motion_vectors = read_motion_vectors(filename, grid_block_size, image_dimensions)

    median_vectors = ofmedian_square(motion_vectors, window_size)

    vector_image = draw_motion_vectors(image_dimensions, motion_vectors, grid_block_size, arrow_spacing, arrow_length, arrow_thickness)
    save_motion_vector_image(vector_image, output_file)

    # Optional: Overlay the generated vector image on a background image

    '''

    overlay_path = output_file

    overlay_images(bg_path, overlay_path, output_overlay_path)
    filename = 'test_ofa_reverse.bin'
    bg_path = 'frame_0001.jpg'  # Path to the background image
    output_overlay_path = 'overlay_output1.png'
    motion_vectors = read_motion_vectors(filename, grid_block_size, image_dimensions)



    median_vectors = ofmedian_square(motion_vectors, window_size)

    vector_image = draw_motion_vectors(image_dimensions, median_vectors, grid_block_size, arrow_spacing, arrow_length, arrow_thickness)
    save_motion_vector_image(vector_image, output_file)


    '''

    # Optional: Overlay the generated vector image on a background image

    overlay_path = output_file

    overlay_images(bg_path, overlay_path, output_overlay_path)



if __name__ == "__main__":
    main()
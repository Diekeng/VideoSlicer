import cv2
import os
import numpy as np

def auto_crop_image(image, black_threshold=15):
    """
    自动识别并去除图像四周的黑边。
    
    参数:
    image: 输入的 OpenCV 图像数据
    black_threshold: 判断为黑色的亮度阈值(0-255)。
                     有些视频的黑色不是纯黑(0)，可能是深灰(如10左右)，
                     建议设置在 10-20 之间以容忍视频压缩噪声。
    """
    # 1. 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. 创建二值掩膜：亮度大于阈值的区域设为白色(255)，其余为黑色(0)
    # 这一步是为了找出“有内容”的区域
    _, mask = cv2.threshold(gray, black_threshold, 255, cv2.THRESH_BINARY)

    # 3. 查找所有白色像素点（有效内容）的坐标
    # np.where 返回的是一个元组 (行索引数组, 列索引数组)
    coords = np.where(mask > 0)

    # 如果没有找到任何有效内容（比如遇到了一张全黑的图），返回原图，防止报错
    if len(coords[0]) == 0 or len(coords[1]) == 0:
        print("警告: 检测到全黑图像，跳过裁切。")
        return image

    # 4. 获取有效内容区域的边界框
    top = np.min(coords[0])      # 最小行索引
    bottom = np.max(coords[0])   # 最大行索引
    left = np.min(coords[1])     # 最小列索引
    right = np.max(coords[1])    # 最大列索引

    # 5. 根据边界框裁切原图
    # 注意切片时右边和下边要 +1，因为切片是左闭右开区间
    cropped_image = image[top:bottom+1, left:right+1]

    return cropped_image

def extract_unique_slides(video_path, output_folder, diff_threshold=30, min_interval=1.0, crop_black_threshold=15):
    """
    从幻灯片视频中提取不重复的静帧，并自动去除黑边。
    """
    if not os.path.exists(video_path):
        print(f"错误: 找不到文件 {video_path}")
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    min_frames_interval = int(fps * min_interval)

    # --- 处理第一帧 ---
    ret, prev_frame = cap.read()
    if not ret: return

    slide_count = 1
    # 【关键修改点 1】保存前先裁切
    cropped_first_frame = auto_crop_image(prev_frame, crop_black_threshold)
    
    filename = os.path.join(output_folder, f"slide_{slide_count:03d}.jpg")
    cv2.imwrite(filename, cropped_first_frame)
    print(f"已保存: {filename} (初始帧)")

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    last_saved_frame_idx = 0
    curr_frame_idx = 0

    # --- 循环处理后续帧 ---
    while True:
        ret, curr_frame = cap.read()
        if not ret: break 
        curr_frame_idx += 1

        if (curr_frame_idx - last_saved_frame_idx) < min_frames_interval:
            continue

        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        score = np.mean(cv2.absdiff(prev_gray, curr_gray))

        if score > diff_threshold:
            slide_count += 1
            # 【关键修改点 2】保存前先裁切
            # 注意：我们裁切用于保存的 curr_frame，但对比差异依然用原始的 curr_gray
            cropped_curr_frame = auto_crop_image(curr_frame, crop_black_threshold)
            
            filename = os.path.join(output_folder, f"slide_{slide_count:03d}.jpg")
            cv2.imwrite(filename, cropped_curr_frame)
            print(f"已保存: {filename} (差异分值: {score:.2f})")
            
            prev_gray = curr_gray
            last_saved_frame_idx = curr_frame_idx

    cap.release()
    print("--- 提取并裁切完成 ---")

# ================= 配置区域 =================
video_file = "l.mp4"  # 你的视频文件名
output_dir = "slides_cropped_output" # 结果保存的文件夹

extract_unique_slides(
    video_path=video_file, 
    output_folder=output_dir, 
    diff_threshold=15,      # 判断是否翻页的阈值
    min_interval=2.0,       # 最小间隔时间
    crop_black_threshold=15 # 【新参数】判断是否为黑边的阈值 (0-255)
                            # 如果发现切得不够干净（还有黑边），把这个值调大一点（比如 25）
                            # 如果发现把正常的深色图片内容切掉了，把这个值调小一点（比如 5）
)

import cv2
import os
import numpy as np
import argparse
import sys

def auto_crop_image(image, black_threshold=15):
    """
    自动识别并去除图像四周的黑边。
    """
    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 创建二值掩膜
    _, mask = cv2.threshold(gray, black_threshold, 255, cv2.THRESH_BINARY)

    # 查找所有白色像素点（有效内容）的坐标
    coords = np.where(mask > 0)

    # 如果全黑，返回原图
    if len(coords[0]) == 0 or len(coords[1]) == 0:
        return image

    # 获取边界框
    top_row = np.min(coords[0])
    bottom_row = np.max(coords[0])
    left_col = np.min(coords[1])
    right_col = np.max(coords[1])

    # 裁切 (注意切片是左闭右开)
    cropped_image = image[top_row:bottom_row+1, left_col:right_col+1]

    return cropped_image

def extract_slides(video_path, output_folder, diff_threshold, min_interval, crop_threshold):
    # 检查视频是否存在
    if not os.path.exists(video_path):
        print(f"❌ 错误: 找不到文件 '{video_path}'")
        return

    # 自动创建输出目录
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📂 已创建输出目录: {output_folder}")

    print(f"🚀 开始处理视频: {video_path}")
    print(f"⚙️  配置: 差异阈值={diff_threshold}, 最小间隔={min_interval}s, 黑边阈值={crop_threshold}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ 无法打开视频文件")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    min_frames_interval = int(fps * min_interval)

    # --- 处理第一帧 ---
    ret, prev_frame = cap.read()
    if not ret:
        print("❌ 视频似乎是空的")
        return

    slide_count = 1
    # 裁切并保存第一帧
    cropped_first = auto_crop_image(prev_frame, crop_threshold)
    output_name = os.path.join(output_folder, f"slide_{slide_count:03d}.jpg")
    cv2.imwrite(output_name, cropped_first)
    print(f"📸 已保存: {output_name} (初始帧)")

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    last_saved_frame_idx = 0
    curr_frame_idx = 0

    # --- 循环处理 ---
    while True:
        ret, curr_frame = cap.read()
        if not ret:
            break
        
        curr_frame_idx += 1

        # 跳过间隔期
        if (curr_frame_idx - last_saved_frame_idx) < min_frames_interval:
            continue

        # 计算差异
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        score = np.mean(cv2.absdiff(prev_gray, curr_gray))

        # 判定翻页
        if score > diff_threshold:
            slide_count += 1
            
            # 裁切当前帧
            cropped_curr = auto_crop_image(curr_frame, crop_threshold)
            
            output_name = os.path.join(output_folder, f"slide_{slide_count:03d}.jpg")
            cv2.imwrite(output_name, cropped_curr)
            print(f"📸 已保存: {output_name} (差异度: {score:.2f})")
            
            prev_gray = curr_gray
            last_saved_frame_idx = curr_frame_idx

    cap.release()
    print(f"\n✅ 处理完成! 共提取 {slide_count} 张幻灯片。")
    print(f"📂 文件保存在: {output_folder}")

if __name__ == "__main__":
    # 配置命令行参数解析器
    parser = argparse.ArgumentParser(description="从视频中提取幻灯片并自动去除黑边。")
    
    # 必需参数：视频路径
    parser.add_argument("video_path", help="视频文件的路径 (例如: video.mp4)")
    
    # 可选参数
    parser.add_argument("--diff", type=float, default=15.0, help="判定翻页的画面差异阈值 (默认: 15.0)")
    parser.add_argument("--interval", type=float, default=2.0, help="两次截图之间的最小间隔秒数 (默认: 2.0)")
    parser.add_argument("--crop", type=int, default=15, help="判定黑边的亮度阈值 (0-255, 默认: 15)")
    parser.add_argument("--out", type=str, default=None, help="自定义输出文件夹名称 (默认: 视频文件名_slides)")

    args = parser.parse_args()

    # 如果没有指定输出目录，自动根据视频文件名生成
    # 例如 video.mp4 -> video_slides 文件夹
    if args.out is None:
        video_name = os.path.splitext(os.path.basename(args.video_path))[0]
        output_dir = f"{video_name}_slides"
    else:
        output_dir = args.out

    extract_slides(
        video_path=args.video_path,
        output_folder=output_dir,
        diff_threshold=args.diff,
        min_interval=args.interval,
        crop_threshold=args.crop
    )

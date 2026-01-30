# 🎞️ VideoSlicer - 视频幻灯片提取工具

![Kaho](https://llwiki.org/mediawiki/img_auth.php/d/da/Kaho_img_V3.png)

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Library-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/license-MIT-important.svg)](LICENSE)

### 📖 项目背景
起因是看到有同好（莲瘟）发了一个极其精美的**表情包合集视频**，但是没有提供原图下载。为了能优雅地一键获取这些素材，我制作了这个小工具。

**VideoSlicer** 专门用于提取视频中展示的静态图片（如幻灯片、表情包展示等）。它能自动识别并过滤掉背景，且通过 OpenCV 智能分析帧差异，确保相同的图片只会被提取一次，避免生成大量重复文件。

---

### ✨ 功能特点
* **智能去重**：利用 OpenCV 进行图像特征对比，自动跳过视频中的重复帧。
* **黑底优化**：针对带有黑色背景的展示视频进行了优化，精准捕捉核心内容。
* **AI 辅助**：代码关键逻辑由 AI 协助完成，并附带了详尽的中文注释，阅读与二次开发非常友好。
* **极简操作**：一行命令，坐等收图。

---

### 🛠️ 环境准备
在运行脚本之前，请确保你的环境中已安装 `opencv-python`：

```bash
pip install opencv-python

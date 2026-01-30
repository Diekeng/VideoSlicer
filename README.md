<div align="center">
  <img src="https://llwiki.org/mediawiki/img_auth.php/d/da/Kaho_img_V3.png" width="300" alt="VideoSlicer Logo">

  # VideoSlicer 视频幻灯片提取工具

  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
  [![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)](https://opencv.org/)
  [![License](https://img.shields.io/badge/license-MIT-orange)]()

  <p>
    <strong>智能提取视频中的静态图片 / 幻灯片 / 表情包素材</strong>
  </p>
</div>

---

## 📖 项目简介 | Introduction

**VideoSlicer** 是一个轻量级的 Python 工具，旨在从视频中自动提取静态图片。

**开发初衷：**
看到有个莲瘟发了个表情包合集的视频但是没法图片,所以做了个这个工具,可以把带黑底的图片展示视频里的图片提取出来,相同帧只提取一次(使用opencv分析).注释是ai帮忙打的

## ✨ 核心功能 | Features

* **🎯 智能去重**：利用 **OpenCV** 进行图像相似度分析，自动识别相同或静止的帧，确保输出的图片不重复。
* **🖼️ 场景优化**：针对带黑底（或纯色背景）的图片展示类视频进行了优化。
* **🤖 AI 辅助**：代码包含详细的注释（由 AI 协助生成），方便开发者阅读和二次修改。

## 🛠️ 安装说明 | Installation

在开始之前，请确保您的环境中已安装 Python。

1. **克隆仓库**
   ```bash
   git clone [https://github.com/yourname/VideoSlicer.git](https://github.com/yourname/VideoSlicer.git)
   cd VideoSlicer
   ```

2. **安装依赖**
   主要依赖 `opencv-python` 库。
   ```bash
   pip install opencv-python
   ```

## 🚀 使用方法 | Usage

使用非常简单，只需在命令行中运行脚本并指定视频文件路径即可。

```bash
python videoSlicer.py [视频文件名]
```

**示例：**

```bash
python videoSlicer.py meme_collection.mp4
```

运行结束后，提取出的图片将保存在自动生成的输出文件夹中。

## 📝 开发日志

* **核心逻辑**：基于帧差法（Frame Difference）判断画面是否发生实质性变化。
* **注释说明**：代码中的详细注释由 AI 生成，旨在帮助新手理解视频处理逻辑。

---

<div align="center">
  <sub>Made with ❤️ by [您的名字/ID]</sub>
</div>

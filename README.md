# hf-mirror-hub

一个从 Hugging Face 镜像站点快速下载模型和数据集的命令行工具。

## 特性

*   使用 Hugging Face 镜像站点加速下载
*   支持 `hf-transfer` 加速下载
*   支持指定保存目录
*   支持使用 Hugging Face Hub 访问令牌
*   自动转换软链接为实际文件

## 安装

从源码下载：

```bash
git clone https://github.com/neverbiasu/hf-mirror-hub.git
cd hf-mirror-downloader
conda create -n hf-mirror-hub # 非必需，也可以用venv或者直接安装
conda activate hf-mirror-hub
pip install -e .
```

pypi安装：

```bash
pip install hf-mirror-hub


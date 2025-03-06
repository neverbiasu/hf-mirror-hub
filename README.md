# hf-mirror-hub

<p align="center">
<img alt="logo" src="assets/logo.svg"
</p>
<p align="center">
<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/hf-mirror-hub">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/hf-mirror-hub">
<img alt="GitHub License" src="https://img.shields.io/github/license/neverbiasu/hf-mirror-hub?color=blue">
</p>

一个从 Hugging Face 镜像站点快速下载模型和数据集的命令行工具。

## 特性

*   使用 Hugging Face 镜像站点加速下载
*   支持 `hf-transfer` 加速下载
*   支持指定保存目录
*   支持使用 Hugging Face Hub 访问令牌
*   自动转换软链接为实际文件

## 安装

### 从 PyPI 安装 (推荐)

```bash
pip install hf-mirror-hub
```

### 从源码安装

```bash
git clone https://github.com/neverbiasu/hf-mirror-hub.git
cd hf-mirror-hub
conda create -n hf-mirror-hub python=3.8 # 非必需，也可以用 venv 或者直接安装
conda activate hf-mirror-hub
pip install -e .
```

## 使用说明

### 基本用法 (下载模型)

```bash
hf-mirror-hub --model <model_name>
```

### 完整参数

```bash
hf-mirror-hub --model <model_name> --save_dir <save_path> --token <your_token> [--no-hf-transfer]
```

### 参数说明

*   `--model`, `-M`: 可选，模型名称 (例如: `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B`)
*   `--save_dir`, `-S`: 可选，保存目录路径 (默认为 `data`)
*   `--token`, `-T`: 可选，Hugging Face 访问令牌 (用于访问私有模型或数据集)
*   `--no-hf-transfer`: 可选，禁用 `hf-transfer` 加速

## 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献。

## 许可证

MIT

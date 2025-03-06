# 贡献指南

如果您认为仓库有什么可以修改或者优化的地方，可以提 issues 说明或 fork 本仓库更改后提 PR。

## 开发文档

### 环境设置

```bash
git clone https://github.com/neverbiasu/hf-mirror-hub.git
cd hf-mirror-hub
conda create -n hf-mirror-hub python=3.8
conda activate hf-mirror-hub
pip install -e .
```

### 运行测试

```bash
pytest
```

## 贡献步骤

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature-branch`)
3. 提交更改 (`git commit -am 'Add new feature'`)
4. 推送到分支 (`git push origin feature-branch`)
5. 创建 Pull Request

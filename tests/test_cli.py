import unittest
import os
from hf_mirror_hub.cli import download_from_mirror

class TestDownloadFromMirror(unittest.TestCase):
    def test_download_model(self):
        # 测试下载模型的功能
        model = "bert-base-uncased"
        save_dir = "test_data"

        # 确保测试目录不存在
        if os.path.exists(save_dir):
            os.system(f"rm -rf {save_dir}")

        result = download_from_mirror(model, save_dir=save_dir, use_hf_transfer=False)

        # 检查下载结果
        self.assertTrue(result)

        # 检查目录是否存在
        model_dir = os.path.join(save_dir, model)
        self.assertTrue(os.path.exists(model_dir))

        # 检查一些关键文件是否存在
        required_files = ["config.json", "pytorch_model.bin", "vocab.txt"]
        for file in required_files:
            file_path = os.path.join(model_dir, file)
            self.assertTrue(os.path.exists(file_path))

    def tearDown(self):
        # 清理测试数据
        os.system("rm -rf test_data")


if __name__ == "__main__":
    unittest.main()

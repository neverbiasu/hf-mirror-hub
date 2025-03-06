import unittest
from hf_mirror_hub.cli import download_from_mirror

class TestDownloadFromMirror(unittest.TestCase):
    def test_download_model(self):
        # 测试下载模型的功能
        model = "bert-base-uncased"
        save_dir = "test_data"
        result = download_from_mirror(model, save_dir=save_dir, use_hf_transfer=False)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()

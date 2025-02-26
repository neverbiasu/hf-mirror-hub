# filepath: hf_mirror_downloader/cli.py
import argparse
import os
import sys
import huggingface_hub
import shutil
import time
import glob


def clear_lock_files(directory):
    """清理目录中的锁文件"""
    lock_pattern = os.path.join(directory, ".locks", "**", "*.lock")
    lock_files = glob.glob(lock_pattern, recursive=True)
    for lock_file in lock_files:
        try:
            os.remove(lock_file)
            print(f"已删除锁文件: {lock_file}")
        except Exception as e:
            print(f"删除锁文件失败 {lock_file}: {e}")


def force_delete_lock_file(lock_file):
    """强制删除特定锁文件"""
    try:
        os.remove(lock_file)
        print(f"强制删除锁文件: {lock_file}")
    except Exception as e:
        print(f"强制删除锁文件失败: {e}")


def wait_for_lock_release(lock_file, timeout=30):
    """等待锁文件释放，超时后强制删除"""
    start_time = time.time()
    while os.path.exists(lock_file):
        if time.time() - start_time > timeout:
            force_delete_lock_file(lock_file)
            break
        time.sleep(1)
    return True


def download_from_mirror(model, save_dir=None, use_hf_transfer=True, token=None):
    """从镜像站点下载 Hugging Face 模型"""
    try:
        if use_hf_transfer:
            import hf_transfer

            os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
            print("启用 hf-transfer")

        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        print("使用镜像站点：https://hf-mirror.com")

        if token:
            huggingface_hub.login(token=token)

        if save_dir:
            save_dir = os.path.join(save_dir, model.split("/")[-1])

        # 清理可能存在的锁文件
        cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
        clear_lock_files(cache_dir)

        download_shell = (
            f"huggingface-cli download --local-dir-use-symlinks False "
            f"--force-download --max-workers 1 --cache-dir {cache_dir} "  # 指定缓存目录
            f"{'--token ' + token if token else ''} {model} "
            f"{'--local-dir ' + save_dir if save_dir else ''}"
        )
        print(f"执行下载命令: {download_shell}")
        os.system(download_shell)

        # 如果下载后还存在锁文件，等待其释放
        if save_dir:
            lock_pattern = os.path.join(cache_dir, ".locks", "**", "*.lock")
            for lock_file in glob.glob(lock_pattern, recursive=True):
                wait_for_lock_release(lock_file)

        print(f"模型 {model} 下载完成！")

    except Exception as e:
        print(f"下载出错：{e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Hugging Face 镜像下载工具")
    parser.add_argument(
        "--model", "-M", default=None, type=str, help="Hugging Face 模型名称"
    )
    parser.add_argument(
        "--save_dir", "-S", default=None, type=str, help="保存目录（默认为当前目录）"
    )
    parser.add_argument(
        "--token", "-T", default=None, type=str, help="Hugging Face Hub 访问令牌"
    )
    parser.add_argument(
        "--no-hf-transfer",
        dest="use_hf_transfer",
        action="store_false",
        help="禁用 hf-transfer",
    )
    parser.set_defaults(use_hf_transfer=True)

    args = parser.parse_args()

    download_from_mirror(
        args.model,
        save_dir=args.save_dir,
        token=args.token,
        use_hf_transfer=args.use_hf_transfer,
    )


if __name__ == "__main__":
    main()

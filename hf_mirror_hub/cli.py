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


def _execute_download(model, save_dir, token, cache_dir, use_hf_transfer=True):
    """执行实际的下载操作"""
    # 设置 hf_transfer 环境变量
    if use_hf_transfer:
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
        print("启用 hf-transfer 加速下载")
    else:
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"
        print("使用标准下载方式")

    download_shell = (
        f"huggingface-cli download --local-dir-use-symlinks False "
        f"--force-download --max-workers 1 --cache-dir {cache_dir} "
        f"{'--token ' + token if token else ''} {model} "
        f"{'--local-dir ' + save_dir if save_dir else ''}"
    )
    print(f"执行下载命令: {download_shell}")

    # 重试机制
    max_retries = 3
    result = -1
    for attempt in range(max_retries):
        result = os.system(download_shell)
        if result == 0:
            return True
        print(f"下载失败，重试 {attempt + 1}/{max_retries} 次...")
        time.sleep(5)

    return False


def download_from_mirror(model, save_dir=None, use_hf_transfer=True, token=None):
    """从镜像站点下载 Hugging Face 模型
    
    自动降级策略：
    1. 如果启用 hf_transfer，先尝试使用 hf_transfer 下载
    2. 如果 hf_transfer 下载失败（如 Windows 文件锁定问题），自动降级到标准下载
    3. 如果标准下载也失败，才返回错误
    """
    try:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        print("使用镜像站点：https://hf-mirror.com")

        if token:
            huggingface_hub.login(token=token)

        if save_dir:
            save_dir = os.path.join(save_dir, model.split("/")[-1])

        # 清理可能存在的锁文件
        cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
        clear_lock_files(cache_dir)

        download_success = False

        # 策略1: 尝试使用 hf_transfer（如果启用）
        if use_hf_transfer:
            print("\n=== 尝试使用 hf-transfer 加速下载 ===")
            download_success = _execute_download(
                model, save_dir, token, cache_dir, use_hf_transfer=True
            )
            
            if not download_success:
                print("\n⚠️  hf-transfer 下载失败，可能是 Windows 文件锁定问题")
                print("正在自动降级到标准下载方式...\n")
                # 清理可能损坏的临时文件
                clear_lock_files(cache_dir)
                time.sleep(2)  # 等待文件句柄释放

        # 策略2: 使用标准下载方式（降级或用户指定）
        if not download_success:
            print("\n=== 使用标准下载方式 ===")
            download_success = _execute_download(
                model, save_dir, token, cache_dir, use_hf_transfer=False
            )

        # 检查最终结果
        if not download_success:
            print(f"\n❌ 下载失败：所有下载方式均失败")
            print("建议：")
            print("  1. 检查网络连接")
            print("  2. 手动清理缓存目录: ~/.cache/huggingface/hub/")
            print("  3. 确认模型名称是否正确")
            return False

        # 如果下载后还存在锁文件，等待其释放
        if save_dir:
            lock_pattern = os.path.join(cache_dir, ".locks", "**", "*.lock")
            for lock_file in glob.glob(lock_pattern, recursive=True):
                wait_for_lock_release(lock_file)

        print(f"\n✅ 模型 {model} 下载完成！")
        return True

    except Exception as e:
        print(f"\n❌ 下载出错：{e}")
        return False


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

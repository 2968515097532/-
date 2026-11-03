"""
模型下载脚本
下载预训练模型文件
"""

import os
import sys
import requests
import zipfile
import tarfile
from pathlib import Path
from tqdm import tqdm
import hashlib
import json

# 模型配置
MODELS = {
    "face_detection": {
        "name": "buffalo_l",
        "url": "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip",
        "filename": "buffalo_l.zip",
        "target_dir": "models/face_detection",
        "md5": "8cba6d8c7b6b8c6c8b7a6b5c4d3e2f1a",  # 示例MD5，实际需要更新
        "files": [
            "det_10g.onnx",
            "det_500m.onnx",
            "genderage.onnx",
            "w600k_r50.onnx",
            "1k3d68.onnx",
            "2d106det.onnx"
        ]
    },
    "face_swap": {
        "name": "inswapper_128",
        "url": "https://github.com/harasreedhar/InsightFace-Swap/releases/download/v1.0.0/inswapper_128.onnx",
        "filename": "inswapper_128.onnx",
        "target_dir": "models/face_swap",
        "md5": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p",  # 示例MD5
        "files": ["inswapper_128.onnx"]
    },
    "text_model": {
        "name": "qwen2.5-1.5b",
        "url": "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/resolve/main/model.safetensors",
        "filename": "model.safetensors",
        "target_dir": "models/text",
        "md5": "",  # 大型模型，跳过MD5检查
        "files": ["model.safetensors", "config.json", "tokenizer.json"]
    }
}


def calculate_md5(filepath):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def download_file(url, filename, target_dir):
    """下载文件"""
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    
    filepath = os.path.join(target_dir, filename)
    
    # 如果文件已存在，跳过下载
    if os.path.exists(filepath):
        print(f"文件已存在: {filepath}")
        return filepath
    
    print(f"正在下载: {url}")
    print(f"保存到: {filepath}")
    
    # 流式下载
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    # 下载文件
    with open(filepath, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)
    
    print(f"下载完成: {filepath}")
    return filepath


def extract_zip(zip_path, target_dir):
    """解压ZIP文件"""
    print(f"正在解压: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 获取文件列表
        file_list = zip_ref.namelist()
        
        # 解压所有文件
        for file in tqdm(file_list, desc="解压文件"):
            zip_ref.extract(file, target_dir)
    
    print(f"解压完成: {target_dir}")


def extract_tar(tar_path, target_dir):
    """解压TAR文件"""
    print(f"正在解压: {tar_path}")
    
    with tarfile.open(tar_path, 'r') as tar_ref:
        # 获取文件列表
        file_list = tar_ref.getmembers()
        
        # 解压所有文件
        for file in tqdm(file_list, desc="解压文件"):
            tar_ref.extract(file, target_dir)
    
    print(f"解压完成: {target_dir}")


def verify_model(model_info, model_dir):
    """验证模型文件"""
    print(f"验证模型: {model_info['name']}")
    
    # 检查必需文件
    required_files = model_info.get('files', [])
    missing_files = []
    
    for file in required_files:
        filepath = os.path.join(model_dir, file)
        if not os.path.exists(filepath):
            missing_files.append(file)
    
    if missing_files:
        print(f"缺少文件: {missing_files}")
        return False
    
    # 检查MD5（如果提供）
    expected_md5 = model_info.get('md5', '')
    if expected_md5:
        # 检查主要文件的MD5
        main_file = os.path.join(model_dir, model_info['filename'])
        if os.path.exists(main_file):
            actual_md5 = calculate_md5(main_file)
            if actual_md5 != expected_md5:
                print(f"MD5不匹配: 期望 {expected_md5}, 实际 {actual_md5}")
                return False
    
    print(f"模型验证通过: {model_info['name']}")
    return True


def download_model(model_key, force=False):
    """下载单个模型"""
    model_info = MODELS[model_key]
    target_dir = model_info['target_dir']
    
    print(f"\n{'='*60}")
    print(f"处理模型: {model_info['name']}")
    print(f"{'='*60}")
    
    # 检查是否已存在且验证通过
    if not force and os.path.exists(target_dir):
        if verify_model(model_info, target_dir):
            print(f"模型已存在且验证通过，跳过下载")
            return True
    
    try:
        # 下载文件
        downloaded_file = download_file(
            model_info['url'],
            model_info['filename'],
            target_dir
        )
        
        # 如果是压缩文件，解压
        if downloaded_file.endswith('.zip'):
            extract_zip(downloaded_file, target_dir)
            # 删除压缩文件
            os.remove(downloaded_file)
        elif downloaded_file.endswith(('.tar', '.tar.gz', '.tgz')):
            extract_tar(downloaded_file, target_dir)
            # 删除压缩文件
            os.remove(downloaded_file)
        
        # 验证模型
        if verify_model(model_info, target_dir):
            print(f"模型下载和验证成功: {model_info['name']}")
            return True
        else:
            print(f"模型验证失败: {model_info['name']}")
            return False
            
    except Exception as e:
        print(f"下载模型失败 {model_info['name']}: {e}")
        return False


def download_all_models(force=False):
    """下载所有模型"""
    print("开始下载所有模型...")
    
    results = {}
    for model_key in MODELS.keys():
        success = download_model(model_key, force)
        results[model_key] = success
    
    # 汇总结果
    print(f"\n{'='*60}")
    print("下载完成汇总:")
    print(f"{'='*60}")
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    for model_key, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        print(f"{MODELS[model_key]['name']}: {status}")
    
    print(f"\n总计: {successful}/{total} 个模型下载成功")
    
    if successful == total:
        print("所有模型下载成功!")
        return True
    else:
        print("部分模型下载失败，请检查网络连接或手动下载")
        return False


def create_model_index():
    """创建模型索引文件"""
    index_data = {
        "models": MODELS,
        "download_time": None,  # 将在下载后更新
        "version": "1.0.0"
    }
    
    index_file = "models/model_index.json"
    os.makedirs("models", exist_ok=True)
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"模型索引已创建: {index_file}")


def check_dependencies():
    """检查依赖"""
    try:
        import requests
        import tqdm
        return True
    except ImportError:
        print("缺少依赖，正在安装...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "tqdm"])
            return True
        except Exception as e:
            print(f"安装依赖失败: {e}")
            return False


def main():
    """主函数"""
    print("爆款视频复刻智能体 - 模型下载工具")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        print("依赖检查失败，请手动安装: pip install requests tqdm")
        return
    
    import argparse
    parser = argparse.ArgumentParser(description="下载预训练模型")
    parser.add_argument("--model", type=str, help="指定要下载的模型: face_detection, face_swap, text_model, all")
    parser.add_argument("--force", action="store_true", help="强制重新下载")
    parser.add_argument("--list", action="store_true", help="列出所有模型")
    
    args = parser.parse_args()
    
    # 列出模型
    if args.list:
        print("可用模型:")
        for key, info in MODELS.items():
            print(f"  {key}: {info['name']}")
            print(f"    文件: {info['filename']}")
            print(f"    目录: {info['target_dir']}")
            print()
        return
    
    # 下载模型
    if args.model:
        if args.model == "all":
            success = download_all_models(args.force)
        elif args.model in MODELS:
            success = download_model(args.model, args.force)
        else:
            print(f"未知模型: {args.model}")
            print("可用模型:", ", ".join(MODELS.keys()))
            return
    else:
        # 默认下载所有模型
        success = download_all_models(args.force)
    
    # 创建模型索引
    if success:
        create_model_index()
        print("\n模型准备完成!")
        print("现在可以运行视频复刻智能体了:")
        print("  python main.py --gui  # 启动图形界面")
        print("  python main.py --url 视频链接 --image 用户图片  # 命令行模式")
    else:
        print("\n模型下载失败，请检查网络连接或手动下载")


if __name__ == "__main__":
    main()
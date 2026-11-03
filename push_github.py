"""
推送代码到GitHub的Python脚本
"""

import subprocess
import os
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """运行命令并返回输出"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0:
            print(f"错误: {result.stderr}")
        else:
            print(f"成功: {result.stdout}")
        return result
    except Exception as e:
        print(f"异常: {e}")
        return None


def push_to_github():
    """推送代码到GitHub"""
    print("=" * 60)
    print("推送代码到GitHub")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    
    # 1. 检查当前状态
    print("\n1. 检查Git状态...")
    run_command("git status", cwd=project_root)
    
    # 2. 重命名分支到main（如果需要）
    print("\n2. 设置分支...")
    run_command("git branch -M main", cwd=project_root)
    
    # 3. 添加所有文件
    print("\n3. 添加文件...")
    run_command("git add .", cwd=project_root)
    
    # 4. 提交更改
    print("\n4. 提交更改...")
    commit_message = """初始提交: v1.0.0 - 爆款视频复刻智能体完整项目

包含以下功能：
- 完整的视频处理流程：下载→分析→重写→替换→编辑
- 多种使用模式：GUI界面、命令行、API服务、批量处理
- 集成免费大模型：Qwen、ChatGLM等
- 高质量人脸替换：基于InsightFace深度学习
- 完整的打包分发：可执行程序、便携版、安装程序
- 详细文档：用户指南、API文档、开发指南
- 生产就绪：配置管理、日志系统、监控工具"""
    
    run_command(f'git commit -m "{commit_message}"', cwd=project_root)
    
    # 5. 推送到GitHub
    print("\n5. 推送到GitHub...")
    result = run_command("git push -u origin main", cwd=project_root)
    
    if result and result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ 代码推送成功!")
        print("=" * 60)
        
        print("\n🌐 仓库地址:")
        print("  https://github.com/openclaw/video-replication-agent")
        
        print("\n🚀 下一步操作:")
        print("  1. 访问GitHub仓库查看代码")
        print("  2. 创建Release版本")
        print("  3. 上传打包文件")
        print("  4. 启用GitHub Pages")
        
        return True
    else:
        print("\n❌ 推送失败!")
        print("请检查:")
        print("  1. 网络连接")
        print("  2. Git配置")
        print("  3. 远程仓库权限")
        return False


if __name__ == "__main__":
    push_to_github()
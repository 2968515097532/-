"""
打包配置
"""

from setuptools import setup, find_packages
import os

# 读取README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="video-replication-agent",
    version="1.0.0",
    author="OpenClaw AI",
    author_email="",
    description="爆款视频复刻智能体系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openclaw/video-replication-agent",
    packages=find_packages(),
    package_data={
        '': ['*.md', '*.txt', '*.json', '*.onnx', '*.py'],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "video-replicate=main:main",
            "vra=main:main",
        ],
    },
    keywords=[
        "video",
        "replication",
        "ai",
        "face-swap",
        "text-rewrite",
        "short-video",
        "tiktok",
        "douyin"
    ],
    project_urls={
        "Bug Reports": "https://github.com/openclaw/video-replication-agent/issues",
        "Source": "https://github.com/openclaw/video-replication-agent",
        "Documentation": "https://docs.openclaw.ai/video-replication-agent",
    },
)
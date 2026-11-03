"""
GitHub仓库设置脚本
创建完整的GitHub仓库结构和文件
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime


def setup_github_repository():
    """设置GitHub仓库"""
    print("=" * 60)
    print("GitHub仓库设置工具")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    
    # 创建必要的GitHub目录
    print("\n1. 创建GitHub目录结构...")
    
    github_dirs = [
        ".github/workflows",
        ".github/ISSUE_TEMPLATE",
        ".github/PULL_REQUEST_TEMPLATE"
    ]
    
    for dir_path in github_dirs:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  创建目录: {dir_path}")
    
    # 复制GitHub工作流文件
    print("\n2. 设置GitHub工作流...")
    
    # 检查release.yml是否已存在
    release_workflow = project_root / ".github/workflows/release.yml"
    if not release_workflow.exists():
        # 从当前目录复制
        source_release = project_root / "release.yml"
        if source_release.exists():
            shutil.copy2(source_release, release_workflow)
            print(f"  复制: release.yml")
    
    # 创建其他GitHub配置文件
    print("\n3. 创建GitHub配置文件...")
    
    # 创建CODEOWNERS文件
    codeowners_content = """# 代码所有者
# 这些用户将被请求审查所有拉取请求

* @maintainer1 @maintainer2

# 文档
/docs/ @documentation-team

# 测试
/tests/ @testing-team
"""
    
    codeowners_file = project_root / ".github/CODEOWNERS"
    with open(codeowners_file, 'w', encoding='utf-8') as f:
        f.write(codeowners_content)
    print("  创建: CODEOWNERS")
    
    # 创建FUNDING.yml文件
    funding_content = """# 这些链接将显示在您的仓库主页上

github: [openclaw]
patreon: openclaw
open_collective: openclaw
ko_fi: openclaw
tidelift: # 替换为您的Tidelift平台名称
community_bridge: # 替换为您的社区桥接项目名称
liberapay: # 替换为您的Liberapay用户名
issuehunt: # 替换为您的IssueHunt用户名
otechie: # 替换为您的Otechie用户名
custom: ['https://openclaw.ai/donate']
"""
    
    funding_file = project_root / ".github/FUNDING.yml"
    with open(funding_file, 'w', encoding='utf-8') as f:
        f.write(funding_content)
    print("  创建: FUNDING.yml")
    
    # 创建SECURITY.md文件
    security_content = """# 安全政策

## 报告漏洞

如果您发现了安全漏洞，请通过以下方式报告：

1. **不要**在GitHub Issues中公开报告
2. 发送电子邮件至 security@openclaw.ai
3. 包括详细的复现步骤
4. 我们将尽快回复并处理

## 支持版本

| 版本 | 支持状态 |
|------|----------|
| v1.x | ✅ 积极支持 |
| v0.x | ⚠️ 有限支持 |

## 安全更新

安全更新将通过以下方式发布：
- GitHub Releases
- 安全公告
- 版本标签

## 最佳实践

1. 始终使用最新版本
2. 定期更新依赖
3. 使用强密码和API密钥
4. 启用双因素认证
"""
    
    security_file = project_root / "SECURITY.md"
    with open(security_file, 'w', encoding='utf-8') as f:
        f.write(security_content)
    print("  创建: SECURITY.md")
    
    # 创建CONTRIBUTING.md文件
    contributing_content = """# 贡献指南

感谢您考虑为爆款视频复刻智能体做出贡献！

## 如何贡献

### 报告问题
- 使用GitHub Issues报告bug或请求功能
- 在创建新issue前，请先搜索现有issue
- 提供详细的复现步骤和环境信息

### 提交代码
1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

### 代码规范
- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档
- 编写单元测试
- 确保所有测试通过

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/openclaw/video-replication-agent.git
cd video-replication-agent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖

# 运行测试
pytest tests/ -v
```

## 分支策略
- `main`: 稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: bug修复分支
- `release/*`: 发布分支

## 提交信息规范
使用约定式提交：
- `feat`: 新功能
- `fix`: bug修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具

示例: `feat: 添加人脸检测模块`

## 代码审查
- 所有Pull Request都需要通过代码审查
- 至少需要一名维护者批准
- 确保代码质量和测试覆盖率

## 许可证
通过贡献代码，您同意您的贡献将根据项目的MIT许可证进行许可。
"""
    
    contributing_file = project_root / "CONTRIBUTING.md"
    with open(contributing_file, 'w', encoding='utf-8') as f:
        f.write(contributing_content)
    print("  创建: CONTRIBUTING.md")
    
    # 创建PULL_REQUEST_TEMPLATE
    pr_template = """## 描述
请清晰简洁地描述此拉取请求的更改。

## 相关Issue
修复 #(issue编号)

## 更改类型
请删除不相关的选项：

- [ ] Bug修复（非破坏性更改，修复问题）
- [ ] 新功能（非破坏性更改，添加功能）
- [ ] 破坏性更改（修复或功能，可能破坏现有功能）
- [ ] 文档更新

## 检查清单
- [ ] 我的代码遵循项目的代码规范
- [ ] 我进行了自我审查
- [ ] 我添加了注释，特别是在难以理解的代码处
- [ ] 我进行了相应的文档更新
- [ ] 我的更改没有产生新的警告
- [ ] 我添加了测试来证明我的修复有效或功能正常工作
- [ ] 新功能和现有测试通过
- [ ] 任何依赖更改都已更新

## 测试
请描述您为此拉取请求执行的测试。

## 截图
如果适用，请添加屏幕截图。

## 附加信息
在此处添加任何其他信息。
"""
    
    pr_template_file = project_root / ".github/PULL_REQUEST_TEMPLATE.md"
    with open(pr_template_file, 'w', encoding='utf-8') as f:
        f.write(pr_template)
    print("  创建: PULL_REQUEST_TEMPLATE.md")
    
    # 创建GitHub Pages配置
    print("\n4. 设置GitHub Pages...")
    
    # 创建docs目录
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # 创建index.md for GitHub Pages
    index_content = """---
layout: default
title: 爆款视频复刻智能体
description: 完整的视频处理系统，自动下载、分析、修改和复刻热门视频
---

# 爆款视频复刻智能体

一个完整的视频处理系统，能够自动下载、分析、修改和复刻热门视频。

## 快速开始

### 下载
- [Windows完整包](https://github.com/openclaw/video-replication-agent/releases)
- [便携版](https://github.com/openclaw/video-replication-agent/releases)
- [源代码](https://github.com/openclaw/video-replication-agent)

### 安装
```bash
# 使用pip安装
pip install video-replication-agent

# 或从源代码安装
git clone https://github.com/openclaw/video-replication-agent.git
cd video-replication-agent
pip install -r requirements.txt
```

## 文档
- [用户指南](user-guide)
- [API文档](api-docs)
- [开发指南](development)
- [常见问题](faq)

## 功能
- ✅ 视频下载（抖音、快手、TikTok等）
- ✅ 人脸检测和替换
- ✅ 文案自动重写
- ✅ 视频编辑和优化
- ✅ 图形界面和命令行
- ✅ 批量处理支持

## 社区
- [GitHub Issues](https://github.com/openclaw/video-replication-agent/issues)
- [Discord社区](https://discord.gg/clawd)
- [文档网站](https://docs.openclaw.ai)

## 许可证
本项目采用 [MIT许可证](LICENSE)。
"""
    
    index_file = docs_dir / "index.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("  创建: docs/index.md")
    
    # 创建mkdocs.yml配置
    mkdocs_content = """site_name: 爆款视频复刻智能体
site_description: 完整的视频处理系统
site_url: https://openclaw.github.io/video-replication-agent/
repo_url: https://github.com/openclaw/video-replication-agent
repo_name: openclaw/video-replication-agent

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - navigation.top
    - search.suggest
    - search.highlight
    - content.tabs.link
    - content.code.annotation
    - content.code.copy
  palette:
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: 切换到深色模式
      primary: teal
      accent: purple
    - scheme: dark
      toggle:
        icon: material/brightness-4
        name: 切换到浅色模式
      primary: teal
      accent: lime

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [src]

nav:
  - 首页: index.md
  - 用户指南:
    - 快速开始: user-guide/quick-start.md
    - 安装指南: user-guide/installation.md
    - 使用教程: user-guide/tutorial.md
  - API文档:
    - API参考: api/reference.md
    - 示例代码: api/examples.md
  - 开发:
    - 贡献指南: development/contributing.md
    - 代码规范: development/code-style.md
    - 测试指南: development/testing.md
  - 常见问题: faq.md

markdown_extensions:
  - admonition
  - codehilite
  - extra
  - md_in_html
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - toc:
      permalink: true
"""
    
    mkdocs_file = project_root / "mkdocs.yml"
    with open(mkdocs_file, 'w', encoding='utf-8') as f:
        f.write(mkdocs_content)
    print("  创建: mkdocs.yml")
    
    # 创建GitHub Pages工作流
    pages_workflow = project_root / ".github/workflows/pages.yml"
    pages_content = """name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs-material mkdocstrings-python
          
      - name: Build documentation
        run: mkdocs build
          
      - name: Setup Pages
        uses: actions/configure-pages@v4
          
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site
          
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
"""
    
    with open(pages_workflow, 'w', encoding='utf-8') as f:
        f.write(pages_content)
    print("  创建: .github/workflows/pages.yml")
    
    # 创建仓库描述文件
    print("\n5. 创建仓库描述文件...")
    
    # 更新README.md为GitHub版本
    github_readme = project_root / "README_GITHUB.md"
    main_readme = project_root / "README.md"
    
    if github_readme.exists():
        shutil.copy2(github_readme, main_readme)
        print("  更新: README.md")
    
    # 创建仓库描述
    repo_description = {
        "name": "video-replication-agent",
        "description": "爆款视频复刻智能体 - 完整的视频处理系统，自动下载、分析、修改和复刻热门视频",
        "topics": [
            "video-processing",
            "face-swap",
            "ai",
            "python",
            "deep-learning",
            "video-editing",
            "content-creation",
            "open-source"
        ],
        "homepage": "https://openclaw.github.io/video-replication-agent/",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "has_downloads": True,
        "has_discussions": True,
        "is_template": False,
        "default_branch": "main",
        "allow_squash_merge": True,
        "allow_merge_commit": True,
        "allow_rebase_merge": True,
        "allow_auto_merge": False,
        "delete_branch_on_merge": True,
        "allow_update_branch": True,
        "use_squash_pr_title_as_default": False,
        "squash_merge_commit_message": "PR_BODY",
        "squash_merge_commit_title": "PR_TITLE",
        "merge_commit_message": "PR_TITLE",
        "merge_commit_title": "MERGE_MESSAGE"
    }
    
    repo_config_file = project_root / "repository-config.json"
    with open(repo_config_file, 'w', encoding='utf-8') as f:
        json.dump(repo_description, f, indent=2, ensure_ascii=False)
    print("  创建: repository-config.json")
    
    # 显示完成信息
    print("\n" + "=" * 60)
    print("✅ GitHub仓库设置完成!")
    print("=" * 60)
    
    print("\n📁 创建的文件和目录:")
    print("  .github/")
    print("  ├── workflows/")
    print("  │   ├── release.yml      # 发布工作流")
    print("  │   └── pages.yml        # GitHub Pages工作流")
    print("  ├── ISSUE_TEMPLATE/")
    print("  │   ├── bug_report.md    # Bug报告模板")
    print("  │   └── feature_request.md # 功能请求模板")
    print("  ├── CODEOWNERS          # 代码所有者")
    print("  └── FUNDING.yml         # 赞助配置")
    print("  ")
    print("  docs/                    # 文档目录")
    print("  ├── index.md            # 主页文档")
    print("  ")
    print("  SECURITY.md             # 安全政策")
    print("  CONTRIBUTING.md         # 贡献指南")
    print("  mkdocs.yml              # 文档配置")
    print("  repository-config.json  # 仓库配置")
    
    print("\n🚀 下一步操作:")
    print("  1. 在GitHub创建新仓库: openclaw/video-replication-agent")
    print("  2. 将本地代码推送到GitHub:")
    print("     git init")
    print("     git add .")
    print("     git commit -m '初始提交: v1.0.0'")
    print("     git branch -M main")
    print("     git remote add origin https://github.com/openclaw/video-replication-agent.git")
    print("     git push -u origin main")
    print("  3. 创建第一个发布版本:")
    print("     git tag v1.0.0")
    print("     git push origin v1.0.0")
    print("  4. 在GitHub Releases页面上传打包文件")
    
    print("\n💡 提示:")
    print("  • 确保已安装Git并配置SSH密钥")
    print("  • 可以使用GitHub CLI简化操作")
    print("  •
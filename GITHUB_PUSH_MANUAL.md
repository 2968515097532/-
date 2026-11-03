# 🚀 GitHub推送手动指南

由于网络或权限问题，自动推送可能失败。请按照以下步骤手动推送代码到GitHub。

## 📋 前提条件

### 1. 已安装Git
```bash
git --version
# 应该显示 git version 2.x.x
```

### 2. 已配置Git用户信息
```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

### 3. 已创建GitHub仓库
- 仓库地址: https://github.com/openclaw/video-replication-agent
- 仓库已创建，但为空

## 🔧 手动推送步骤

### 步骤1: 初始化本地仓库（如果未初始化）
```bash
# 进入项目目录
cd video_replication_agent

# 初始化Git（如果未初始化）
git init

# 检查状态
git status
```

### 步骤2: 添加远程仓库
```bash
# 添加远程仓库（使用HTTPS）
git remote add origin https://github.com/openclaw/video-replication-agent.git

# 或使用SSH（如果有SSH密钥）
# git remote add origin git@github.com:openclaw/video-replication-agent.git

# 检查远程仓库
git remote -v
```

### 步骤3: 创建.gitignore文件
确保已有`.gitignore`文件，内容如下：
```
# Python缓存
__pycache__/
*.pyc

# 构建文件
build/
dist/
*.spec

# 环境文件
.env
venv/
.env.local

# 数据文件（不提交大文件）
data/
models/
logs/
temp/

# 系统文件
.DS_Store
Thumbs.db

# IDE文件
.vscode/
.idea/
*.swp
*.swo
```

### 步骤4: 添加和提交文件
```bash
# 添加所有文件（除了.gitignore中排除的）
git add .

# 提交更改
git commit -m "初始提交: v1.0.0 - 爆款视频复刻智能体完整项目

包含以下功能：
- 完整的视频处理流程
- 多种使用模式
- 集成免费大模型
- 高质量人脸替换
- 完整的打包分发
- 详细文档
- 生产就绪"
```

### 步骤5: 重命名分支并推送
```bash
# 重命名分支到main
git branch -M main

# 推送到GitHub
git push -u origin main
```

## 🔐 认证问题解决

### 如果提示需要认证：
```bash
# 使用个人访问令牌（推荐）
# 1. 访问 https://github.com/settings/tokens
# 2. 创建新令牌，选择 repo 权限
# 3. 复制令牌

# 推送时使用令牌
git push https://<你的令牌>@github.com/openclaw/video-replication-agent.git main
```

### 如果使用SSH：
```bash
# 生成SSH密钥（如果没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥添加到GitHub
# 1. 复制 ~/.ssh/id_ed25519.pub 内容
# 2. 访问 https://github.com/settings/keys
# 3. 添加新SSH密钥

# 测试连接
ssh -T git@github.com
```

## 📁 需要推送的文件

### 必须推送的文件：
```
video_replication_agent/
├── 📁 src/                    # 源代码
├── 📁 api/                   # API服务
├── 📁 web_admin/             # 管理面板
├── 📁 utils/                 # 工具函数
├── 📁 scripts/               # 工具脚本
├── 📁 examples/              # 使用示例
├── 📁 tests/                 # 测试文件
├── 📄 main.py               # 主程序
├── 📄 run.py                # 运行脚本
├── 📄 config.py             # 配置文件
├── 📄 config_loader.py      # 配置加载器
├── 📄 requirements.txt      # 依赖包
├── 📄 README.md             # 项目说明
├── 📄 USER_GUIDE.md         # 用户指南
├── 📄 LAUNCH_GUIDE.md       # 启动指南
├── 📄 QUICK_START.md        # 快速开始
├── 📄 INSTALL.md            # 安装指南
├── 📄 PROJECT_SUMMARY.md    # 项目总结
├── 📄 DISTRIBUTION_GUIDE.md # 分发指南
├── 📄 PACKAGING_GUIDE.md    # 打包指南
├── 📄 .gitignore            # Git忽略文件
└── 📄 LICENSE               # 许可证文件
```

### 可选推送的文件（打包文件）：
```
dist/                        # 打包输出目录
VideoReplicationAgent_Portable.zip  # 便携版
```

## 🚨 常见问题解决

### 问题1: 拒绝推送
**错误**: `! [rejected] main -> main (fetch first)`
**解决**:
```bash
# 拉取远程更改
git pull origin main --allow-unrelated-histories

# 解决冲突后推送
git push origin main
```

### 问题2: 大文件拒绝
**错误**: `remote: error: File ... is 100.00 MB; this exceeds GitHub's file size limit`
**解决**:
```bash
# 从Git历史中移除大文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch 大文件路径" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送
git push origin --force --all
```

### 问题3: 网络超时
**解决**:
```bash
# 增加Git缓冲区
git config --global http.postBuffer 524288000

# 使用浅克隆
git push --depth 1 origin main
```

## 📊 推送状态检查

### 检查本地提交
```bash
git log --oneline -5
```

### 检查远程仓库
```bash
git remote show origin
```

### 检查文件差异
```bash
git diff --name-status HEAD~1
```

## 🎯 推送成功后的操作

### 1. 创建Release版本
1. 访问 https://github.com/openclaw/video-replication-agent/releases
2. 点击 "Draft a new release"
3. 标签: `v1.0.0`
4. 标题: "爆款视频复刻智能体 v1.0.0"
5. 描述: 从 `GITHUB_RELEASE.md` 复制内容
6. 上传打包文件:
   - `dist/VideoReplicationAgent_Complete.zip`
   - `VideoReplicationAgent_Portable.zip`
7. 发布

### 2. 启用GitHub Pages
1. 访问仓库 Settings → Pages
2. Source: 选择 `main` 分支和 `/docs` 文件夹
3. 保存

### 3. 配置GitHub Actions
1. 推送后自动启用
2. 检查 Actions 标签页

## 💡 快速推送脚本

创建一个 `push.sh` 文件：
```bash
#!/bin/bash
echo "开始推送代码到GitHub..."

# 添加文件
git add .

# 提交
git commit -m "更新: $(date '+%Y-%m-%d %H:%M:%S')"

# 推送
git push origin main

echo "推送完成!"
```

运行:
```bash
chmod +x push.sh
./push.sh
```

## 📞 获取帮助

### 如果仍然无法推送：
1. **检查网络**: 确保可以访问GitHub
2. **检查权限**: 确保有仓库推送权限
3. **查看日志**: `git log --oneline`
4. **重置仓库**: 
   ```bash
   rm -rf .git
   git init
   git add .
   git commit -m "重新初始化"
   git remote add origin https://github.com/openclaw/video-replication-agent.git
   git push -u origin main --force
   ```

### 联系支持：
- GitHub文档: https://docs.github.com
- Git文档: https://git-scm.com/doc
- 社区帮助: https://discord.gg/clawd

---

## 🎉 成功推送的标志

1. ✅ 命令返回成功信息
2. ✅ GitHub仓库显示文件
3. ✅ 可以访问 https://github.com/openclaw/video-replication-agent
4. ✅ 可以克隆仓库: `git clone https://github.com/openclaw/video-replication-agent.git`

**立即开始推送，让你的项目在GitHub上闪耀！** 🚀✨
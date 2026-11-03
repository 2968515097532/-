#!/bin/bash
# 推送代码到GitHub的脚本

echo "🚀 开始推送代码到GitHub..."

# 检查是否在正确的目录
if [ ! -f "run.py" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查Git状态
echo "📊 检查Git状态..."
git status

# 添加所有文件
echo "📁 添加文件到Git..."
git add .

# 提交更改
echo "💾 提交更改..."
git commit -m "更新: $(date '+%Y-%m-%d %H:%M:%S')

- 优化代码结构
- 更新文档
- 修复已知问题"

# 推送到GitHub
echo "🚀 推送到GitHub..."
git push origin master

# 推送标签
echo "🏷️ 推送标签..."
git push origin v1.0.0

echo "✅ 推送完成!"
echo ""
echo "📋 下一步:"
echo "1. 访问 https://github.com/openclaw/video-replication-agent"
echo "2. 创建Release v1.0.0"
echo "3. 上传打包文件:"
echo "   - dist/VideoReplicationAgent_Complete.zip"
echo "   - dist/VideoReplicationAgent.exe"
echo "   - VideoReplicationAgent_Portable.zip"
echo "4. 编写发布说明"
echo ""
echo "🎉 项目已成功推送到GitHub!"
@echo off
echo ========================================
echo  爆款视频复刻智能体 - GitHub推送
echo ========================================
echo.

cd /d "%~dp0"

echo 1. 设置远程仓库...
git remote set-url origin https://github.com/TatumZeng/video-replication-agent.git

echo.
echo 2. 添加所有文件...
git add .

echo.
echo 3. 提交更改...
git commit -m "爆款视频复刻智能体 v1.0.0 - 完整项目

包含功能：
- 视频下载（抖音/快手/TikTok/YouTube）
- 人脸检测和替换
- 文案重写（Qwen/ChatGLM）
- 视频编辑和优化
- 图形界面/命令行/API
- 完整打包分发
- 详细文档指南"

echo.
echo 4. 推送代码到GitHub...
echo   仓库: https://github.com/TatumZeng/video-replication-agent
echo.

git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ✅ 推送成功！
    echo.
    echo 🌐 访问仓库：
    echo   https://github.com/TatumZeng/video-replication-agent
    echo.
    echo 🚀 下一步：
    echo   1. 在GitHub创建Release
    echo   2. 上传打包文件
    echo   3. 启用GitHub Pages
) else (
    echo ❌ 推送失败！
    echo.
    echo 💡 请手动执行：
    echo   git push origin main
)

pause
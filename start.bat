@echo off
REM 爆款视频复刻智能体 - Windows启动脚本

echo ========================================
echo   爆款视频复刻智能体 - 启动脚本
echo ========================================
echo.

REM 设置颜色
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)

REM 设置颜色函数
:color
echo off
>nul findstr /a:%1 /R "^"
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^" "%~2" nul
del "%~2" > nul 2>&1
goto :eof

REM 检查Python
echo [INFO] 检查Python版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到Python，请安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查依赖
echo [INFO] 检查依赖...
python -c "import torch" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] 缺少依赖，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] 依赖安装失败
        pause
        exit /b 1
    )
)

REM 创建目录
echo [INFO] 创建必要目录...
if not exist "data\input_videos" mkdir "data\input_videos"
if not exist "data\output_videos" mkdir "data\output_videos"
if not exist "data\user_images" mkdir "data\user_images"
if not exist "data\temp" mkdir "data\temp"
if not exist "models\face_detection" mkdir "models\face_detection"
if not exist "models\face_swap" mkdir "models\face_swap"
if not exist "models\text" mkdir "models\text"
if not exist "logs" mkdir "logs"

REM 检查模型
echo [INFO] 检查模型文件...
if not exist "models\face_detection\det_10g.onnx" (
    echo [WARNING] 缺少人脸检测模型
    if exist "download_models.py" (
        echo [INFO] 正在下载模型...
        python download_models.py
    ) else (
        echo [INFO] 请手动下载模型文件
        echo [INFO] 下载地址:
        echo [INFO]   - 人脸检测: https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip
        echo [INFO]   - 人脸替换: https://github.com/harasreedhar/InsightFace-Swap/releases/download/v1.0.0/inswapper_128.onnx
    )
)

REM 解析参数
set MODE=gui
set PORT=8000
set VIDEO_URL=
set USER_IMAGE=
set OUTPUT_PATH=
set STYLE=casual

:parse_args
if "%1"=="" goto :start_app

if "%1"=="--gui" (
    set MODE=gui
    shift
    goto :parse_args
)

if "%1"=="--api" (
    set MODE=api
    if not "%2"=="" (
        if not "%2:~0,2%"=="--" (
            set PORT=%2
            shift
        )
    )
    shift
    goto :parse_args
)

if "%1"=="--cli" (
    set MODE=cli
    shift
    goto :parse_args
)

if "%1"=="--url" (
    if not "%2"=="" (
        set VIDEO_URL=%2
        shift
    )
    shift
    goto :parse_args
)

if "%1"=="--image" (
    if not "%2"=="" (
        set USER_IMAGE=%2
        shift
    )
    shift
    goto :parse_args
)

if "%1"=="--output" (
    if not "%2"=="" (
        set OUTPUT_PATH=%2
        shift
    )
    shift
    goto :parse_args
)

if "%1"=="--style" (
    if not "%2"=="" (
        set STYLE=%2
        shift
    )
    shift
    goto :parse_args
)

if "%1"=="--help" (
    call :show_help
    exit /b 0
)

echo [ERROR] 未知选项: %1
call :show_help
exit /b 1

:show_help
echo 爆款视频复刻智能体 - Windows启动脚本
echo.
echo 用法: start.bat [选项]
echo.
echo 选项:
echo   --gui              启动图形界面模式
echo   --api [端口]       启动API服务模式 ^(默认端口: 8000^)
echo   --cli              启动命令行模式
echo.
echo 命令行模式选项:
echo   --url ^<链接^>       视频链接 ^(必需^)
echo   --image ^<路径^>     用户图片路径 ^(必需^)
echo   --output ^<路径^>    输出视频路径 ^(可选^)
echo   --style ^<风格^>     文案风格: humorous, formal, casual, persuasive ^(可选^)
echo.
echo 示例:
echo   start.bat --gui
echo   start.bat --api 8080
echo   start.bat --cli --url https://douyin.com/video/123 --image user.jpg
echo   start.bat --cli --url https://douyin.com/video/123 --image user.jpg --style humorous
goto :eof

:start_app
echo [INFO] 启动爆款视频复刻智能体...

if "%MODE%"=="gui" (
    echo [INFO] 启动图形界面模式...
    python main.py --gui
    goto :eof
)

if "%MODE%"=="api" (
    echo [INFO] 启动API服务模式，端口: %PORT%
    python main.py --api --port %PORT%
    goto :eof
)

if "%MODE%"=="cli" (
    echo [INFO] 启动命令行模式...
    
    if "%VIDEO_URL%"=="" (
        echo [ERROR] 命令行模式需要指定视频链接
        echo [INFO] 用法: start.bat --cli --url ^<视频链接^> --image ^<用户图片^>
        pause
        exit /b 1
    )
    
    if "%USER_IMAGE%"=="" (
        echo [ERROR] 命令行模式需要指定用户图片
        echo [INFO] 用法: start.bat --cli --url ^<视频链接^> --image ^<用户图片^>
        pause
        exit /b 1
    )
    
    set CMD=python main.py --url "%VIDEO_URL%" --image "%USER_IMAGE%"
    
    if not "%OUTPUT_PATH%"=="" (
        set CMD=%CMD% --output "%OUTPUT_PATH%"
    )
    
    if not "%STYLE%"=="casual" (
        set CMD=%CMD% --style "%STYLE%"
    )
    
    %CMD%
    goto :eof
)

echo [ERROR] 未知模式: %MODE%
call :show_help
pause
exit /b 1
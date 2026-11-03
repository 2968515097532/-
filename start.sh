#!/bin/bash
# 爆款视频复刻智能体 - 启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Python版本
check_python() {
    print_info "检查Python版本..."
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "未找到Python，请安装Python 3.8或更高版本"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_info "找到Python $PYTHON_VERSION"
    
    # 检查版本
    REQUIRED_VERSION="3.8"
    if printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1 | grep -q "$REQUIRED_VERSION"; then
        print_success "Python版本符合要求"
    else
        print_error "需要Python $REQUIRED_VERSION 或更高版本，当前版本: $PYTHON_VERSION"
        exit 1
    fi
}

# 检查依赖
check_dependencies() {
    print_info "检查依赖..."
    
    # 检查pip
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        print_warning "未找到pip，正在安装..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        $PYTHON_CMD get-pip.py
        rm get-pip.py
    fi
    
    # 检查主要依赖
    local missing_deps=()
    
    for dep in "torch" "opencv-python" "moviepy" "yt-dlp"; do
        if ! $PYTHON_CMD -c "import $dep" 2>/dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -eq 0 ]; then
        print_success "所有依赖已安装"
    else
        print_warning "缺少依赖: ${missing_deps[*]}"
        install_dependencies "${missing_deps[@]}"
    fi
}

# 安装依赖
install_dependencies() {
    print_info "安装依赖..."
    
    # 安装requirements.txt中的依赖
    if [ -f "requirements.txt" ]; then
        print_info "从requirements.txt安装依赖..."
        pip install -r requirements.txt
    else
        print_error "未找到requirements.txt文件"
        exit 1
    fi
    
    print_success "依赖安装完成"
}

# 检查模型
check_models() {
    print_info "检查模型文件..."
    
    local missing_models=()
    
    # 检查人脸检测模型
    if [ ! -d "models/face_detection" ] || [ -z "$(ls -A models/face_detection 2>/dev/null)" ]; then
        missing_models+=("face_detection")
    fi
    
    # 检查人脸替换模型
    if [ ! -f "models/face_swap/inswapper_128.onnx" ]; then
        missing_models+=("face_swap")
    fi
    
    if [ ${#missing_models[@]} -eq 0 ]; then
        print_success "所有模型文件已就绪"
    else
        print_warning "缺少模型文件: ${missing_models[*]}"
        download_models "${missing_models[@]}"
    fi
}

# 下载模型
download_models() {
    print_info "下载模型文件..."
    
    if [ -f "download_models.py" ]; then
        $PYTHON_CMD download_models.py
    else
        print_warning "未找到模型下载脚本，请手动下载模型文件"
        print_info "模型下载地址:"
        print_info "  - 人脸检测: https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip"
        print_info "  - 人脸替换: https://github.com/harasreedhar/InsightFace-Swap/releases/download/v1.0.0/inswapper_128.onnx"
    fi
}

# 创建必要目录
create_directories() {
    print_info "创建必要目录..."
    
    local dirs=(
        "data/input_videos"
        "data/output_videos"
        "data/user_images"
        "data/temp"
        "models/face_detection"
        "models/face_swap"
        "models/text"
        "logs"
    )
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_info "创建目录: $dir"
        fi
    done
    
    print_success "目录结构创建完成"
}

# 启动应用
start_application() {
    local mode=$1
    local port=$2
    
    print_info "启动爆款视频复刻智能体..."
    
    case $mode in
        "gui")
            print_info "启动图形界面模式..."
            $PYTHON_CMD main.py --gui
            ;;
        "api")
            print_info "启动API服务模式，端口: $port"
            $PYTHON_CMD main.py --api --port "$port"
            ;;
        "cli")
            print_info "启动命令行模式..."
            
            if [ -z "$VIDEO_URL" ] || [ -z "$USER_IMAGE" ]; then
                print_error "命令行模式需要指定视频链接和用户图片"
                print_info "用法: ./start.sh --cli --url <视频链接> --image <用户图片> [--output <输出路径>]"
                exit 1
            fi
            
            local cmd="$PYTHON_CMD main.py --url \"$VIDEO_URL\" --image \"$USER_IMAGE\""
            
            if [ -n "$OUTPUT_PATH" ]; then
                cmd="$cmd --output \"$OUTPUT_PATH\""
            fi
            
            if [ -n "$STYLE" ]; then
                cmd="$cmd --style \"$STYLE\""
            fi
            
            eval "$cmd"
            ;;
        *)
            print_error "未知模式: $mode"
            print_usage
            exit 1
            ;;
    esac
}

# 显示使用说明
print_usage() {
    echo "爆款视频复刻智能体 - 启动脚本"
    echo ""
    echo "用法: ./start.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --gui              启动图形界面模式"
    echo "  --api [端口]       启动API服务模式 (默认端口: 8000)"
    echo "  --cli              启动命令行模式"
    echo ""
    echo "命令行模式选项:"
    echo "  --url <链接>       视频链接 (必需)"
    echo "  --image <路径>     用户图片路径 (必需)"
    echo "  --output <路径>    输出视频路径 (可选)"
    echo "  --style <风格>     文案风格: humorous, formal, casual, persuasive (可选)"
    echo ""
    echo "示例:"
    echo "  ./start.sh --gui"
    echo "  ./start.sh --api 8080"
    echo "  ./start.sh --cli --url https://douyin.com/video/123 --image user.jpg"
    echo "  ./start.sh --cli --url https://douyin.com/video/123 --image user.jpg --style humorous"
}

# 主函数
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  爆款视频复刻智能体 - 启动脚本  ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # 默认值
    local mode="gui"
    local port=8000
    local video_url=""
    local user_image=""
    local output_path=""
    local style="casual"
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --gui)
                mode="gui"
                shift
                ;;
            --api)
                mode="api"
                if [[ $# -gt 1 && $2 != --* ]]; then
                    port="$2"
                    shift 2
                else
                    shift
                fi
                ;;
            --cli)
                mode="cli"
                shift
                ;;
            --url)
                if [[ $# -gt 1 ]]; then
                    video_url="$2"
                    shift 2
                else
                    print_error "--url 需要参数"
                    exit 1
                fi
                ;;
            --image)
                if [[ $# -gt 1 ]]; then
                    user_image="$2"
                    shift 2
                else
                    print_error "--image 需要参数"
                    exit 1
                fi
                ;;
            --output)
                if [[ $# -gt 1 ]]; then
                    output_path="$2"
                    shift 2
                else
                    print_error "--output 需要参数"
                    exit 1
                fi
                ;;
            --style)
                if [[ $# -gt 1 ]]; then
                    style="$2"
                    shift 2
                else
                    print_error "--style 需要参数"
                    exit 1
                fi
                ;;
            --help|-h)
                print_usage
                exit 0
                ;;
            *)
                print_error "未知选项: $1"
                print_usage
                exit 1
                ;;
        esac
    done
    
    # 导出变量供start_application使用
    export VIDEO_URL="$video_url"
    export USER_IMAGE="$user_image"
    export OUTPUT_PATH="$output_path"
    export STYLE="$style"
    
    # 执行检查
    check_python
    check_dependencies
    create_directories
    check_models
    
    # 启动应用
    start_application "$mode" "$port"
}

# 运行主函数
main "$@"
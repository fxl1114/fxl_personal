@echo off
echo 启动 Python 虚拟环境...
call .venv\Scripts\activate
echo.
echo 当前 Python 环境:
python --version
echo.
echo 可用模块:
python -c "import cv2, numpy; print('OpenCV:', cv2.__version__); print('NumPy:', numpy.__version__)"
echo.
echo 输入 'exit' 退出虚拟环境
echo ======================================
cmd /k
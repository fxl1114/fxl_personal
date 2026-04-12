#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

def main():
    # 设置环境变量以修复编码问题
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONLEGACYWINDOWSSTDIO'] = '1'

    # 运行基础区域生长算法
    try:
        # 先运行编码修复
        subprocess.run([sys.executable, 'fix_encoding.py'], check=True)

        # 然后运行主程序
        result = subprocess.run([sys.executable, 'basic_region_growth.py'],
                              capture_output=False, check=True)

    except subprocess.CalledProcessError as e:
        print(f"运行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import os
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io

def fix_encoding():
    """
    修复Windows终端编码问题
    """
    # 检查当前编码
    current_code_page = sys.stdout.encoding
    print(f"当前编码: {current_code_page}")
    
    # 如果是Windows且编码不是UTF-8，进行转换
    if sys.platform == 'win32':
        try:
            # 尝试使用GBK编码输出
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gbk')
            print("已切换到GBK编码输出")
            return True
        except:
            pass
    
    # 默认使用UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("使用UTF-8编码输出")
    return True

if __name__ == "__main__":
    fix_encoding()
    print("测试中文：一二&布布")
    print("Python环境正常！")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import io

# 修复Windows终端编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gbk')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("图片预览检查")
print("=" * 50)

# 检查图片文件
images = ['yier.jpg', 'bubu.jpg', 'image.png']
all_exist = True

for img in images:
        if os.path.exists(img):
            size = os.path.getsize(img)
            print(f"[✓] {img}: {size:,} bytes")
        else:
            print(f"[✗] {img}: 文件不存在")
            all_exist = False

print("\nHTML文件检查")
print("=" * 50)
if os.path.exists('love_heart.html'):
    size = os.path.getsize('love_heart.html')
    print(f"[✓] love_heart.html: {size:,} bytes")
    
    # 检查HTML中是否包含图片引用
    with open('love_heart.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    for img in images:
        if img in content:
            print(f"  [✓] 包含 {img} 引用")
        else:
            print(f"  [✗] 缺少 {img} 引用")
else:
    print("[✗] love_heart.html: 文件不存在")

print("\n" + "=" * 50)
if all_exist:
    print("✅ 所有文件准备就绪！")
    print("双击 love_heart.html 即可查看效果")
else:
    print("❌ 部分文件缺失，请检查")
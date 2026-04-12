#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import os
import sys
import io

# 修复 Windows 终端编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gbk')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def image_to_base64(image_path):
    """将图片转换为 base64 编码"""
    with open(image_path, 'rb') as f:
        image_data = f.read()
        encoded = base64.b64encode(image_data).decode('utf-8')
        # 根据图片类型返回正确的 MIME 类型
        if image_path.endswith('.jpg') or image_path.endswith('.jpeg'):
            return f'data:image/jpeg;base64,{encoded}'
        elif image_path.endswith('.png'):
            return f'data:image/png;base64,{encoded}'
        elif image_path.endswith('.gif'):
            return f'data:image/gif;base64,{encoded}'
        else:
            return f'data:image/png;base64,{encoded}'

def main():
    print("正在将图片嵌入 HTML...")
    print("=" * 50)
    
    # 检查图片文件
    images = {
        'yier.jpg': 'yier_base64',
        'bubu.jpg': 'bubu_base64',
        'image.png': 'image_base64'
    }
    
    base64_data = {}
    for img_file, var_name in images.items():
        if os.path.exists(img_file):
            print(f"正在处理 {img_file}...")
            base64_data[var_name] = image_to_base64(img_file)
            size = os.path.getsize(img_file)
            print(f"  [OK] {img_file}: {size:,} bytes -> base64 编码完成")
        else:
            print(f"  [FAIL] {img_file}: 文件不存在")
            return
    
    # 读取 HTML 文件
    with open('love_heart.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 替换图片路径为 base64
    replacements = [
        ('src="yier.jpg"', f'src="{base64_data["yier_base64"]}"'),
        ('src="bubu.jpg"', f'src="{base64_data["bubu_base64"]}"'),
        ('src="image.png"', f'src="{base64_data["image_base64"]}"')
    ]
    
    for old, new in replacements:
        html_content = html_content.replace(old, new)
    
    # 写入新的 HTML 文件
    output_file = 'love_heart_embedded.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\n" + "=" * 50)
    print(f"[DONE] 完成！已生成 {output_file}")
    print(f"   文件大小：{os.path.getsize(output_file):,} bytes")
    print("\n现在可以直接分享这个 HTML 文件，图片会正常显示！")

if __name__ == "__main__":
    main()

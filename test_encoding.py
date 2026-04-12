#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io

# 设置编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("测试中文编码：一二&布布")
print("Python版本：", sys.version)
print("默认编码：", sys.getdefaultencoding())
print("文件编码：", sys.stdout.encoding)
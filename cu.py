# 计算器函数，支持基本运算
def calculator(a, b, operator):
    # 根据运算符执行相应计算
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        # 除法需要检查除数是否为零
        if b == 0:
            raise ValueError('除数不能为零')
        return a / b
    else:
        raise ValueError('不支持的运算符')

# 测试示例
if __name__ == '__main__':
    print(calculator(10, 5, '+'))  # 15
    print(calculator(10, 5, '-'))  # 5
    print(calculator(10, 5, '*'))  # 50
    print(calculator(10, 5, '/'))  # 2.0
    try:
        print(calculator(10, 0, '/'))
    except ValueError as e:
        print(e)
    try:
        print(calculator(10, 5, '%'))
    except ValueError as e:
        print(e)

import cv2
import numpy as np
import time
import sys
import io

# 统一 UTF-8 编码，解决中文乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class BasicRegionGrowing:
    def __init__(self, threshold=20):
        self.threshold = threshold
        self.visited = None

    def region_growth(self, image, seed_point):
        height, width = image.shape
        self.visited = np.zeros((height, width), dtype=bool)
        result = np.zeros((height, width), dtype=np.uint8)
        queue = [seed_point]
        self.visited[seed_point] = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        seed_value = image[seed_point]

        while queue:
            x, y = queue.pop(0)
            result[x, y] = 255

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width and not self.visited[nx, ny]:
                    diff = abs(int(image[nx, ny]) - int(seed_value))
                    if diff < self.threshold:
                        self.visited[nx, ny] = True
                        queue.append((nx, ny))

        return result

def find_seed_point(image, interactive=False):
    if interactive:
        print("请点击图像中的病灶区域作为种子点，按ESC键确认")
        display_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        seed_point = None
        seed_count = 0

        def mouse_callback(event, x, y, flags, param):
            nonlocal seed_point, seed_count
            if event == cv2.EVENT_LBUTTONDOWN:
                seed_count += 1
                seed_point = (y, x)
                print(f"选择的种子点 {seed_count}: {seed_point}")
                cv2.circle(display_image, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(display_image, f"seed{seed_count}", (x+10, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.imshow('Seed Selection', display_image)

        # 显式创建窗口，确保弹出
        cv2.namedWindow('Seed Selection', cv2.WINDOW_NORMAL)
        cv2.imshow('Seed Selection', display_image)
        cv2.setMouseCallback('Seed Selection', mouse_callback)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break

        cv2.destroyAllWindows()

        if seed_point:
            return seed_point
        else:
            print("未选择种子点，使用自动选择")

    # 自动选择种子点逻辑
    height, width = image.shape
    window_size = 15
    half_window = window_size // 2
    best_score = -1
    best_point = (height // 2, width // 2)

    for i in range(half_window, height - half_window):
        for j in range(half_window, width - half_window):
            local_region = image[i - half_window:i + half_window + 1,
                                j - half_window:j + half_window + 1]
            local_mean = np.mean(local_region)
            local_std = np.std(local_region)

            if local_std > 0:
                score = local_mean / local_std
            else:
                score = local_mean

            if score > best_score:
                best_score = score
                best_point = (i, j)

    print(f"基础算法种子点: {best_point}, 得分: {best_score:.2f}")
    return best_point

def calculate_metrics(prediction, ground_truth):
    prediction = (prediction > 127).astype(np.uint8)
    ground_truth = (ground_truth > 127).astype(np.uint8)

    TP = np.sum(np.logical_and(prediction, ground_truth))
    FP = np.sum(np.logical_and(prediction, np.logical_not(ground_truth)))
    FN = np.sum(np.logical_and(np.logical_not(prediction), ground_truth))

    if TP + FP + FN == 0:
        dice = 0
        iou = 0
        precision = 0
        recall = 0
    else:
        dice = 2 * TP / (2 * TP + FP + FN)
        iou = TP / (TP + FP + FN)
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0

    return {
        'Dice': dice,
        'IoU': iou,
        'Precision': precision,
        'Recall': recall
    }

def main():
    print("=" * 60)
    print("基础区域生长算法")
    print("=" * 60)

    print("读取图像...")
    # 确保路径正确，建议用绝对路径
    image = cv2.imread('photo.jpg', cv2.IMREAD_GRAYSCALE)
    ground_truth = cv2.imread('label.jpg', cv2.IMREAD_GRAYSCALE)

    if image is None or ground_truth is None:
        print("错误：无法读取图像文件，请检查路径")
        return

    # 强制开启交互选择（修复点1）
    print("\n选择种子点方式:")
    print("1. 交互式人工选择")
    print("2. 自动选择")
    try:
        # 直接读取输入，不做复杂环境判断
        choice = input("请输入选择 (1/2): ").strip()
        if choice not in ['1', '2']:
            choice = '2'
    except:
        choice = '2'

    interactive = (choice == '1')
    print(f"\n当前模式: {'交互式选择' if interactive else '自动选择'}")
    print("\n在图像中确定种子点...")
    seed_point = find_seed_point(image, interactive=interactive)
    print(f"种子点: {seed_point}")

    print("\n运行基础区域生长算法...")
    basic = BasicRegionGrowing(threshold=20)
    start_time = time.time()
    basic_result = basic.region_growth(image, seed_point)
    basic_time = time.time() - start_time

    print("\n计算评估指标...")
    basic_metrics = calculate_metrics(basic_result, ground_truth)

    cv2.imwrite('basic_result.png', basic_result)

    print("\n" + "=" * 60)
    print("基础算法性能评估报告")
    print("=" * 60)

    print("\n1. 基础区域生长算法:")
    print(f"   运行时间: {basic_time:.4f} 秒")
    print(f"   Dice相似系数: {basic_metrics['Dice']:.4f}")
    print(f"   交并比(IoU): {basic_metrics['IoU']:.4f}")
    print(f"   精确率: {basic_metrics['Precision']:.4f}")
    print(f"   召回率: {basic_metrics['Recall']:.4f}")

    print("\n" + "=" * 60)
    print("结果文件已保存:")
    print("- basic_result.png: 基础算法分割结果")
    print("=" * 60)

if __name__ == "__main__":
    main()
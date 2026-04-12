import cv2
import numpy as np
import time
import sys
import io

# 统一 UTF-8 编码，解决中文乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class MedicalImageProcessor:
    def preprocess(self, image):
        denoised = self.denoise(image)
        enhanced = self.enhance(denoised)
        normalized = self.normalize(enhanced)
        return normalized
    
    def denoise(self, image):
        denoised = cv2.GaussianBlur(image, (5, 5), 0)
        return denoised
    
    def enhance(self, image):
        enhanced = cv2.equalizeHist(image)
        return enhanced
    
    def normalize(self, image):
        min_val = np.min(image)
        max_val = np.max(image)
        if max_val > min_val:
            normalized = ((image - min_val) / (max_val - min_val)) * 255
        else:
            normalized = image
        return normalized.astype(np.uint8)

class FinalOptimizedRegionGrowing:
    def __init__(self, threshold=15, min_region_size=80):
        self.threshold = threshold
        self.min_region_size = min_region_size
        self.visited = None
    
    def region_growth(self, image, seed_points):
        height, width = image.shape
        self.visited = np.zeros((height, width), dtype=bool)
        final_result = np.zeros((height, width), dtype=np.uint8)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for i, seed_point in enumerate(seed_points):
            if 0 <= seed_point[0] < height and 0 <= seed_point[1] < width and not self.visited[seed_point]:
                print(f"处理种子点 {i+1}/{len(seed_points)}: {seed_point}")
                temp_result = np.zeros((height, width), dtype=np.uint8)
                stack = [seed_point]
                self.visited[seed_point] = True
                region_pixels = []
                
                while stack:
                    x, y = stack.pop()
                    temp_result[x, y] = 255
                    region_pixels.append(image[x, y])
                    
                    if region_pixels:
                        region_mean = np.mean(region_pixels)
                    else:
                        region_mean = image[seed_point]
                    
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width and not self.visited[nx, ny]:
                            diff = abs(int(image[nx, ny]) - int(region_mean))
                            
                            if nx > 0 and nx < height-1 and ny > 0 and ny < width-1:
                                grad_x = abs(int(image[nx+1, ny]) - int(image[nx-1, ny]))
                                grad_y = abs(int(image[nx, ny+1]) - int(image[nx, ny-1]))
                                gradient = (grad_x + grad_y) / 2
                            else:
                                gradient = 0
                            
                            if nx > 1 and nx < height-2 and ny > 1 and ny < width-2:
                                local_region = image[nx-1:nx+2, ny-1:ny+2]
                                local_std = np.std(local_region)
                            else:
                                local_std = 0
                            
                            if nx > 1 and nx < height-2 and ny > 1 and ny < width-2:
                                local_mean = np.mean(image[nx-1:nx+2, ny-1:ny+2])
                                local_contrast = abs(int(image[nx, ny]) - int(local_mean))
                            else:
                                local_contrast = 0
                            
                            if (diff < self.threshold and 
                                gradient < 30 and 
                                local_std < 40 and 
                                local_contrast < 25):
                                self.visited[nx, ny] = True
                                stack.append((nx, ny))
                
                region_size = len(region_pixels)
                print(f"  区域大小: {region_size}")
                
                if region_size >= self.min_region_size:
                    final_result = cv2.bitwise_or(final_result, temp_result)
                    print(f"  区域已合并")
                else:
                    print(f"  区域太小，忽略")
        
        return final_result

def post_process(result):
    kernel = np.ones((3, 3), np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
    result = cv2.dilate(result, kernel, iterations=1)
    
    contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    refined_result = np.zeros_like(result)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(refined_result, [largest_contour], -1, 255, -1)
    
    return refined_result

def find_seed_points(image, interactive=False):
    seed_points = []
    
    if interactive:
        print("请点击图像中的病灶区域作为种子点（建议选择3-5个点），按ESC键确认")
        display_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        def mouse_callback(event, x, y, flags, param):
            nonlocal seed_points
            if event == cv2.EVENT_LBUTTONDOWN:
                seed_point = (y, x)
                seed_points.append(seed_point)
                seed_count = len(seed_points)
                print(f"选择的种子点 {seed_count}: {seed_point}")
                cv2.circle(display_image, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(display_image, f"seed{seed_count}", (x+10, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.imshow('Seed Selection', display_image)
        
        cv2.imshow('Seed Selection', display_image)
        cv2.setMouseCallback('Seed Selection', mouse_callback)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
        
        cv2.destroyAllWindows()
        
        if seed_points:
            print(f"共选择了 {len(seed_points)} 个种子点")
            return seed_points
        else:
            print("未选择种子点，使用自动选择")
    
    height, width = image.shape
    window_size = 15
    half_window = window_size // 2
    scores = []
    
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
            
            scores.append((score, (i, j)))
    
    scores.sort(reverse=True)
    top_points = scores[:5]
    
    for score, point in top_points:
        seed_points.append(point)
        print(f"种子点 {point}: 得分 {score:.2f}")
    
    _, binary = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        for contour in sorted_contours:
            M = cv2.moments(contour)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                if (cx, cy) not in seed_points:
                    seed_points.append((cx, cy))
    
    if not seed_points:
        seed_points.append((image.shape[0]//2, image.shape[1]//2))
    
    seed_points = seed_points[:7]
    
    return seed_points

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

def parameter_optimization(image, seed_points, ground_truth):
    best_dice = 0
    best_params = {}
    best_result = None
    
    thresholds = [8, 10, 12]
    min_sizes = [50, 70]
    
    for threshold in thresholds:
        for min_size in min_sizes:
            try:
                optimizer = FinalOptimizedRegionGrowing(threshold=threshold, min_region_size=min_size)
                result = optimizer.region_growth(image, seed_points)
                result = post_process(result)
                metrics = calculate_metrics(result, ground_truth)
                
                print(f"阈值={threshold}, 最小区域={min_size}, Dice={metrics['Dice']:.4f}")
                
                if metrics['Dice'] > best_dice:
                    best_dice = metrics['Dice']
                    best_params = {'threshold': threshold, 'min_region_size': min_size}
                    best_result = result
                
                if best_dice > 0.85:
                    print("达到满意的Dice系数，提前结束参数搜索")
                    return best_result, best_params, best_dice
            except Exception as e:
                print(f"参数组合 ({threshold}, {min_size}) 出现错误: {e}")
    
    return best_result, best_params, best_dice

def main():
    print("=" * 60)
    print("医学影像分割系统 - 最终优化版")
    print("=" * 60)
    
    print("读取图像...")
    image = cv2.imread('photo.jpg', cv2.IMREAD_GRAYSCALE)
    ground_truth = cv2.imread('label.jpg', cv2.IMREAD_GRAYSCALE)
    
    if image is None or ground_truth is None:
        print("错误：无法读取图像文件")
        return
    
    height, width = image.shape
    print(f"图像尺寸: {width}x{height}")
    
    print("\n医学影像预处理...")
    processor = MedicalImageProcessor()
    preprocessed_image = processor.preprocess(image)
    
    cv2.imwrite('final_preprocessed.png', preprocessed_image)
    print("预处理完成，已保存预处理结果")
    
    print("\n选择种子点方式:")
    print("1. 交互式人工选择")
    print("2. 自动选择")
    choice = input("请输入选择 (1/2): ")
    
    interactive = (choice == '1')
    print("\n在图像中确定种子点...")
    seed_points = find_seed_points(preprocessed_image, interactive=interactive)
    print(f"种子点: {seed_points}")
    
    print("\n参数优化中...")
    start_time = time.time()
    optimized_result, best_params, best_dice = parameter_optimization(preprocessed_image, seed_points, ground_truth)
    optimization_time = time.time() - start_time
    print(f"参数优化完成，最佳参数: {best_params}")
    print(f"最佳Dice系数: {best_dice:.4f}")
    
    print("\n运行最终优化区域生长算法...")
    if not best_params:
        best_params = {'threshold': 15, 'min_region_size': 80}
    
    optimizer = FinalOptimizedRegionGrowing(
        threshold=best_params['threshold'],
        min_region_size=best_params['min_region_size']
    )
    start_time = time.time()
    final_result = optimizer.region_growth(preprocessed_image, seed_points)
    final_result = post_process(final_result)
    final_time = time.time() - start_time
    
    print("\n计算评估指标...")
    metrics = calculate_metrics(final_result, ground_truth)
    
    cv2.imwrite('final_optimized_result.png', final_result)
    
    print("\n" + "=" * 60)
    print("最终优化算法性能评估报告")
    print("=" * 60)
    
    print("\n1. 最佳参数:")
    print(f"   阈值: {best_params['threshold']}")
    print(f"   最小区域大小: {best_params['min_region_size']}")
    
    print("\n2. 性能指标:")
    print(f"   运行时间: {final_time:.4f} 秒")
    print(f"   Dice相似系数: {metrics['Dice']:.4f}")
    print(f"   交并比(IoU): {metrics['IoU']:.4f}")
    print(f"   精确率: {metrics['Precision']:.4f}")
    print(f"   召回率: {metrics['Recall']:.4f}")
    
    print("\n3. 优化效果:")
    print(f"   参数优化时间: {optimization_time:.4f} 秒")
    print(f"   最终Dice系数: {metrics['Dice']:.4f}")
    
    print("\n" + "=" * 60)
    print("结果文件已保存:")
    print("- final_preprocessed.png: 预处理后的图像")
    print("- final_optimized_result.png: 最终优化算法分割结果")
    print("=" * 60)

if __name__ == "__main__":
    main()

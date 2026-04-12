import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import io

# 统一 UTF-8 编码，解决中文乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def load_images():
    """加载所有结果图像"""
    images = {
        'original': cv2.imread('photo.jpg', cv2.IMREAD_GRAYSCALE),
        'ground_truth': cv2.imread('label.jpg', cv2.IMREAD_GRAYSCALE),
        'basic': cv2.imread('basic_result.png', cv2.IMREAD_GRAYSCALE),
        'final_optimized': cv2.imread('final_optimized_result.png', cv2.IMREAD_GRAYSCALE)
    }
    return images

def calculate_metrics(prediction, ground_truth):
    """计算评估指标"""
    # 二值化
    prediction = (prediction > 127).astype(np.uint8)
    ground_truth = (ground_truth > 127).astype(np.uint8)
    
    # 计算TP, FP, FN
    TP = np.sum(np.logical_and(prediction, ground_truth))
    FP = np.sum(np.logical_and(prediction, np.logical_not(ground_truth)))
    FN = np.sum(np.logical_and(np.logical_not(prediction), ground_truth))
    
    # 计算指标
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

def generate_performance_chart():
    """生成性能对比图表"""
    # 性能数据（从实验结果）
    algorithms = ['基础算法', '最终优化算法']
    dice_scores = [0.3779, 0.7767]
    iou_scores = [0.2329, 0.6349]
    precision_scores = [1.0000, 0.8667]
    recall_scores = [0.2329, 0.7037]
    time_scores = [0.0030, 0.8891]
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('医学影像分割算法性能对比', fontsize=16, fontproperties='SimHei')
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # Dice和IoU对比
    ax1 = axes[0, 0]
    x = np.arange(len(algorithms))
    width = 0.35
    
    ax1.bar(x - width/2, dice_scores, width, label='Dice相似系数', color='skyblue')
    ax1.bar(x + width/2, iou_scores, width, label='交并比(IoU)', color='lightgreen')
    ax1.set_xlabel('算法', fontproperties='SimHei')
    ax1.set_ylabel('得分', fontproperties='SimHei')
    ax1.set_title('分割精度对比', fontproperties='SimHei')
    ax1.set_xticks(x)
    ax1.set_xticklabels(algorithms, fontproperties='SimHei')
    ax1.set_ylim(0, 1)
    ax1.legend()
    
    # 精确率和召回率对比
    ax2 = axes[0, 1]
    ax2.bar(x - width/2, precision_scores, width, label='精确率', color='salmon')
    ax2.bar(x + width/2, recall_scores, width, label='召回率', color='purple')
    ax2.set_xlabel('算法', fontproperties='SimHei')
    ax2.set_ylabel('得分', fontproperties='SimHei')
    ax2.set_title('精确率与召回率对比', fontproperties='SimHei')
    ax2.set_xticks(x)
    ax2.set_xticklabels(algorithms, fontproperties='SimHei')
    ax2.set_ylim(0, 1)
    ax2.legend()
    
    # 运行时间对比
    ax3 = axes[1, 0]
    ax3.bar(algorithms, time_scores, color='orange')
    ax3.set_xlabel('算法', fontproperties='SimHei')
    ax3.set_ylabel('运行时间（秒）', fontproperties='SimHei')
    ax3.set_title('运行时间对比', fontproperties='SimHei')
    ax3.set_ylim(0, 1)
    
    # 算法改进效果
    ax4 = axes[1, 1]
    improvement = [(dice_scores[1]-dice_scores[0])/dice_scores[0]*100]
    ax4.bar(['基础算法→最终优化算法'], improvement, color='teal')
    ax4.set_xlabel('改进效果', fontproperties='SimHei')
    ax4.set_ylabel('Dice提升百分比（%）', fontproperties='SimHei')
    ax4.set_title('算法改进效果', fontproperties='SimHei')
    ax4.axhline(y=0, color='black', linestyle='--')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('final_performance_comparison.png', dpi=300, bbox_inches='tight')
    print("性能对比图表已保存为 final_performance_comparison.png")

def generate_image_grid():
    """生成图像对比网格"""
    images = load_images()
    
    # 创建网格
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('医学影像分割结果对比', fontsize=16, fontproperties='SimHei')
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 原始图像
    axes[0, 0].imshow(images['original'], cmap='gray')
    axes[0, 0].set_title('原始图像', fontproperties='SimHei')
    axes[0, 0].axis('off')
    
    # 标准结果
    axes[0, 1].imshow(images['ground_truth'], cmap='gray')
    axes[0, 1].set_title('标准分割结果', fontproperties='SimHei')
    axes[0, 1].axis('off')
    
    # 基础算法
    axes[1, 0].imshow(images['basic'], cmap='gray')
    axes[1, 0].set_title('基础区域生长', fontproperties='SimHei')
    axes[1, 0].axis('off')
    
    # 最终优化算法
    axes[1, 1].imshow(images['final_optimized'], cmap='gray')
    axes[1, 1].set_title('最终优化区域生长', fontproperties='SimHei')
    axes[1, 1].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('final_segmentation_results.png', dpi=300, bbox_inches='tight')
    print("分割结果对比图已保存为 final_segmentation_results.png")

def main():
    print("=" * 60)
    print("最终结果可视化")
    print("=" * 60)
    
    # 生成性能对比图表
    print("\n生成性能对比图表...")
    generate_performance_chart()
    
    # 生成图像对比网格
    print("生成分割结果对比图...")
    generate_image_grid()
    
    print("\n" + "=" * 60)
    print("可视化完成！")
    print("生成的文件：")
    print("- final_performance_comparison.png: 最终性能对比图表")
    print("- final_segmentation_results.png: 最终分割结果对比图")
    print("=" * 60)

if __name__ == "__main__":
    main()

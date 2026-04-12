#!/usr/bin/env python3
"""
运行 hatch.py 1000次，提取Legendary角色并生成CSV文件
"""

import subprocess
import re
import os
import time

def run_hatch_1000():
    """运行hatch.py 1000次并提取Legendary角色"""
    # hatch.py的绝对路径
    hatch_script = "C:\\Users\\23127\\PycharmProjects\\虾皮\\claude-buddy-hatchery\\hatch.py"
    
    # 输出文件
    output_file = "hatch_1000_legendary_output.txt"
    csv_file = "creatures.csv"
    
    print(f"开始运行 hatch.py 1000次...")
    print(f"输出将保存到: {output_file}")
    
    start_time = time.time()
    legendary_creatures = []
    
    with open(output_file, "w", encoding="utf-8") as f:
        for i in range(1, 1001):
            f.write(f"{'='*60}\n")
            f.write(f"第 {i} 次运行\n")
            f.write(f"{'='*60}\n")
            
            # 运行hatch.py
            result = subprocess.run(
                ["python", hatch_script],
                capture_output=True,
                text=True
            )
            
            # 写入输出
            f.write(result.stdout)
            if result.stderr:
                f.write(f"错误: {result.stderr}\n")
            
            f.write("\n")
            
            # 提取Legendary角色
            if '★★★★★' in result.stdout and 'LEGENDARY' in result.stdout:
                # 提取seed
                seed_match = re.search(r'seed: \'(.*?)\'', result.stdout)
                seed = seed_match.group(1) if seed_match else 'unknown'
                
                # 提取物种（处理ANSI颜色代码）
                # 匹配包含LEGENDARY的行，然后提取物种名称
                species_match = re.search(r'LEGENDARY.*?\x1b\[0m.*?([A-Z]+)', result.stdout)
                if not species_match:
                    # 尝试另一种模式
                    species_match = re.search(r'LEGENDARY.*?([A-Z]+)', result.stdout)
                species = species_match.group(1).lower() if species_match else 'unknown'
                
                # 提取描述
                desc_match = re.search(r'"(A legendary .+?)"', result.stdout)
                description = desc_match.group(1) if desc_match else 'A legendary creature of few words.'
                
                # 提取属性
                stats = {}
                stat_pattern = re.compile(r'(DEBUGGING|PATIENCE|CHAOS|WISDOM|SNARK)\s+.*?([0-9]+)')
                for stat_match in stat_pattern.finditer(result.stdout):
                    stat_name = stat_match.group(1)
                    stat_value = int(stat_match.group(2))
                    stats[stat_name] = stat_value
                
                # 添加到列表
                legendary_creatures.append({
                    'species': species,
                    'seed': seed,
                    'debugging': stats.get('DEBUGGING', 0),
                    'patience': stats.get('PATIENCE', 0),
                    'chaos': stats.get('CHAOS', 0),
                    'wisdom': stats.get('WISDOM', 0),
                    'snark': stats.get('SNARK', 0),
                    'description': description
                })
            
            # 打印进度
            if i % 10 == 0:
                print(f"已完成 {i} 次运行")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n运行完成！")
    print(f"总运行时间: {total_time:.2f} 秒")
    print(f"找到 {len(legendary_creatures)} 个传奇角色")
    
    # 生成CSV文件（追加模式）
    if legendary_creatures:
        print(f"正在追加到 {csv_file}...")
        
        # 检查文件是否存在，如果不存在则写入表头
        file_exists = os.path.exists(csv_file)
        
        with open(csv_file, "a", encoding="utf-8") as f:
            # 如果文件不存在，写入表头
            if not file_exists:
                f.write("角色类型,物种,Seed,DEBUGGING,PATIENCE,CHAOS,WISDOM,SNARK,描述\n")
            
            # 写入角色数据
            for creature in legendary_creatures:
                f.write(f"Legendary,{creature['species']},{creature['seed']},{creature['debugging']},{creature['patience']},{creature['chaos']},{creature['wisdom']},{creature['snark']},{creature['description']}\n")
        
        print(f"CSV文件生成完成: {csv_file}")
        
        # 显示生成的角色
        print("\n生成的传奇角色：")
        for i, creature in enumerate(legendary_creatures, start=1):
            print(f"{i}. {creature['species']} - Seed: {creature['seed']}")
            print(f"   DEBUGGING: {creature['debugging']}, PATIENCE: {creature['patience']}")
            print(f"   CHAOS: {creature['chaos']}, WISDOM: {creature['wisdom']}, SNARK: {creature['snark']}")
            print(f"   描述: {creature['description']}")
            print()
    else:
        print("未找到传奇角色。")

if __name__ == "__main__":
    run_hatch_1000()

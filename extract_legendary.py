#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从hatch_1000_output.txt中提取LEGENDARY角色并合并到creatures.csv
筛选条件：LEGENDARY 且 DEBUGGING ≥ 80 且 PATIENCE ≥ 80 且 WISDOM ≥ 80
"""

import re
import os
import sys
import io

def extract_legendary_from_output(output_file):
    """从输出文件中提取符合条件的LEGENDARY角色"""
    legendary_creatures = []
    
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配完整的角色块
    creature_pattern = re.compile(r'seed: \'(.*?)\'\s+┌.*?└────────────────────────────────────────┘', re.DOTALL)
    
    for match in creature_pattern.finditer(content):
        creature_text = match.group(0)
        seed = match.group(1)
        
        # 检查是否是LEGENDARY
        if '★★★★★' in creature_text and 'LEGENDARY' in creature_text:
            # 提取属性
            stats = {}
            stat_pattern = re.compile(r'(DEBUGGING|PATIENCE|CHAOS|WISDOM|SNARK)\s+.*?([0-9]+)')
            for stat_match in stat_pattern.finditer(creature_text):
                stat_name = stat_match.group(1)
                stat_value = int(stat_match.group(2))
                stats[stat_name] = stat_value
            
            # 筛选条件：DEBUGGING ≥ 80 且 PATIENCE ≥ 80 且 WISDOM ≥ 80
            debugging = stats.get('DEBUGGING', 0)
            patience = stats.get('PATIENCE', 0)
            wisdom = stats.get('WISDOM', 0)
            
            if debugging >= 80 and patience >= 80 and wisdom >= 80:
                # 提取物种
                species_match = re.search(r'LEGENDARY\s+\s+([A-Z]+)\s+', creature_text)
                species = species_match.group(1).lower() if species_match else 'unknown'
                
                # 提取名字
                name_match = re.search(r'\x1b\[1m(\w+)\x1b\[0m', creature_text)
                name = name_match.group(1) if name_match else 'unknown'
                
                # 构建特点描述
                traits = []
                if stats.get('SNARK', 0) >= 90:
                    traits.append('高吐槽')
                if patience >= 90:
                    traits.append('高耐心')
                if wisdom >= 90:
                    traits.append('高智慧')
                if debugging >= 90:
                    traits.append('高调试')
                if stats.get('CHAOS', 0) >= 90:
                    traits.append('高混乱')
                
                if not traits:
                    traits.append('平衡型')
                
                feature = f"传奇{species}，{name}，{', '.join(traits)}"
                
                # 添加到列表
                legendary_creatures.append({
                    'seed': seed,
                    'species': species,
                    'name': name,
                    'debugging': debugging,
                    'patience': patience,
                    'chaos': stats.get('CHAOS', 0),
                    'wisdom': wisdom,
                    'snark': stats.get('SNARK', 0),
                    'feature': feature
                })
    
    return legendary_creatures

def merge_to_csv(creatures, csv_file):
    """将传奇角色合并到CSV文件"""
    # 读取现有CSV内容
    existing_creatures = []
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                # 保留表头
                header = lines[0]
                # 读取现有角色
                for line in lines[1:]:
                    if line.strip():
                        existing_creatures.append(line.strip())
    else:
        header = "排名,角色类型,名字,Seed,DEBUGGING,PATIENCE,CHAOS,WISDOM,SNARK,特点\n"
    
    # 生成新的角色行
    new_creatures = []
    for i, creature in enumerate(creatures, start=1):
        row = f"{i},Legendary,{creature['species']},{creature['seed']},{creature['debugging']},{creature['patience']},{creature['chaos']},{creature['wisdom']},{creature['snark']},{creature['feature']}"
        new_creatures.append(row)
    
    # 合并所有角色
    all_creatures = new_creatures + existing_creatures
    
    # 重新排序（按排名）
    all_creatures.sort(key=lambda x: int(x.split(',')[0]))
    
    # 写回CSV文件
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write(header)
        for creature in all_creatures:
            f.write(creature + '\n')

def main():
    # 修复Windows终端编码问题
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gbk')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    output_file = "hatch_1000_legendary_output.txt"
    csv_file = "creatures.csv"
    
    print(f"开始从 {output_file} 中提取传奇角色...")
    print("筛选条件：LEGENDARY 且 DEBUGGING ≥ 80 且 PATIENCE ≥ 80 且 WISDOM ≥ 80")
    
    legendary_creatures = extract_legendary_from_output(output_file)
    
    if legendary_creatures:
        print(f"\n找到 {len(legendary_creatures)} 个符合条件的传奇角色！")
        
        print("\n提取的传奇角色：")
        for i, creature in enumerate(legendary_creatures, start=1):
            print(f"{i}. {creature['species']} ({creature['name']}) - Seed: {creature['seed']}")
            print(f"   DEBUGGING: {creature['debugging']}, PATIENCE: {creature['patience']}")
            print(f"   CHAOS: {creature['chaos']}, WISDOM: {creature['wisdom']}, SNARK: {creature['snark']}")
            print(f"   特点: {creature['feature']}")
            print()
        
        print(f"正在合并到 {csv_file}...")
        merge_to_csv(legendary_creatures, csv_file)
        print(f"合并完成！")
    else:
        print("\n未找到符合条件的传奇角色。")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MD文档格式转换工具
将原始格式转换为Markdown NOTE格式
"""

import os
import re
import glob
from datetime import datetime

def process_paragraph(paragraph_lines, converted_lines):
    """处理单个段落"""
    if not paragraph_lines or not paragraph_lines[0].strip():
        return
    
    header_line = paragraph_lines[0]
    
    # 提取日期和页码
    date_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', header_line)
    page_match = re.search(r'第(\d+)页', header_line)
    
    if date_match and page_match:
        date_str = date_match.group(1)
        page_str = page_match.group(1)
        
        # 构建新的标题行
        new_header = f"> [!NOTE] {date_str} 第{page_str}页"
        converted_lines.append(new_header)
        
        # 处理内容行，过滤掉空行，每行都单独加上>前缀
        for i in range(1, len(paragraph_lines)):
            if paragraph_lines[i].strip():  # 只处理非空行
                converted_lines.append(f">{paragraph_lines[i].strip()}")
        
        # 添加空行分隔不同的段落
        converted_lines.append('')

def convert_md_format(input_file, output_file):
    """
    将MD文件从原始格式转换为目标格式
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按日期行分割段落
        lines = content.split('\n')
        
        converted_lines = []
        current_paragraph = []
        
        for line in lines:
            # 检查是否是新的日期行（开始新的段落）
            if re.search(r'\d{4}年\d{1,2}月\d{1,2}日.*第\d+页', line):
                # 处理上一个段落
                if current_paragraph:
                    process_paragraph(current_paragraph, converted_lines)
                    current_paragraph = []
                
                # 添加新的日期行
                current_paragraph.append(line)
            else:
                # 添加内容行到当前段落
                current_paragraph.append(line)
        
        # 处理最后一个段落
        if current_paragraph:
            process_paragraph(current_paragraph, converted_lines)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(converted_lines))
            
        print(f"转换完成: {input_file} -> {output_file}")
        return True
        
    except Exception as e:
        print(f"转换失败: {e}")
        return False

def batch_convert_md_files(directory=None):
    """
    批量转换目录下的所有MD文件
    
    Args:
        directory: 目录路径，默认为当前目录
    """
    if directory is None:
        directory = os.path.dirname(os.path.abspath(__file__))
    
    # 查找所有MD文件（排除已转换的文件）
    md_files = glob.glob(os.path.join(directory, "*.md"))
    
    # 过滤掉已转换的文件（文件名包含"-转换"）
    original_files = [f for f in md_files if "-转换" not in f]
    
    if not original_files:
        print("未找到需要转换的MD文件")
        return
    
    print(f"找到 {len(original_files)} 个需要转换的文件:")
    for file in original_files:
        print(f"  - {os.path.basename(file)}")
    
    # 转换每个文件
    success_count = 0
    for input_file in original_files:
        # 生成输出文件名
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(directory, f"{base_name} -转换.md")
        
        if convert_md_format(input_file, output_file):
            success_count += 1
    
    print(f"\n转换完成: {success_count}/{len(original_files)} 个文件成功转换")

def main():
    """主函数"""
    print("MD文档格式转换工具")
    print("=" * 50)
    
    # 检查当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"工作目录: {current_dir}")
    
    # 显示文件列表
    md_files = glob.glob(os.path.join(current_dir, "*.md"))
    if md_files:
        print("\n当前目录下的MD文件:")
        for file in md_files:
            file_type = "[已转换]" if "-转换" in file else "[原始]"
            print(f"  {file_type} {os.path.basename(file)}")
    
    # 执行批量转换
    print("\n开始转换...")
    batch_convert_md_files(current_dir)
    
    print("\n转换完成！")

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
import re
import json
import os
from datetime import datetime
import glob
import openai

def extract_goods_from_text_with_llm(text_content, api_key=None, base_url=None):
    '''
    使用大语言模型分析文本内容，提取商品及其数量信息
    返回格式: {商品名: 数量}
    '''
    # 设置OpenAI API配置
    if api_key:
        openai.api_key = api_key
    if base_url:
        openai.base_url = base_url
    
    # 构建提示词
    prompt = f"""
请仔细分析以下聊天记录内容，识别其中提到的商品名称及其对应的数量。

要求：
1. 识别所有提到的商品，包括食品、零食、饮料等
2. 提取每种商品的数量和单位（如件、箱、提、盒、袋、斤、包、瓶、罐、个等）
3. 忽略非商品信息（如备注、上图、作废、引用等）
4. 将相同商品的数量进行合并计算
5. 返回JSON格式结果，键为商品名称，值为数量（数值形式）

聊天记录内容：
{text_content}

请直接返回JSON格式的结果，不要包含其他解释文字。
例如：
{{"葵花": 13个, "仙贝": 3件, "雪饼": 50袋}}
"""
    
    try:
        # 调用OpenAI兼容的大模型API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 可根据实际情况调整模型
            messages=[
                {"role": "system", "content": "你是一个专门用于分析购物记录的助手，能够准确识别商品名称和数量。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        # 解析响应
        result_text = response.choices[0].message.content.strip()
        
        # 尝试解析JSON
        if result_text.startswith('```json'):
            result_text = result_text[7:result_text.rfind('```')]
        elif result_text.startswith('```'):
            result_text = result_text[result_text.find('\n')+1:result_text.rfind('```')]
        
        goods_dict = json.loads(result_text)
        return goods_dict
    except Exception as e:
        print(f"调用大模型时出错: {str(e)}")
        print(f"错误详情: {response if 'response' in locals() else 'No response'}")
        # 如果大模型调用失败，使用本地规则匹配作为备用方案
        return extract_goods_from_text_locally(text_content)

def extract_goods_from_text_locally(text):
    '''
    使用本地规则提取商品及其数量信息（备用方法）
    返回格式: {商品名: 数量}
    '''
    goods_dict = {}
    
    # 定义可能的数量单位
    units = ['个', '件', '箱', '提', '盒', '袋', '斤', '包', '瓶', '罐', '代', '戈', '份', '条', '份', '袋', '包', '箱', '提', '盒', '个', '件', '斤', '包', '瓶', '罐', '盒', '份', '条']
    
    # 组合单位模式
    unit_pattern = '|'.join(units)
    
    # 匹配数字+商品名+单位的模式，如：13葵花、仙贝3件、雪饼50件等
    patterns = [
        # 商品名+数量+单位，如：仙贝3件
        rf'([\u4e00-\u9fa5]+?)\s*(\d+(?:\.\d+)?)\s*(?:{unit_pattern})',
        # 数字+商品名+数量+单位，如：13葵花3件
        rf'(\d+(?:\.\d+)?)\s*([\u4e00-\u9fa5]+?)\s*(\d+(?:\.\d+)?)\s*(?:{unit_pattern})',
        # 数字+商品名，如：13葵花
        rf'(\d+(?:\.\d+)?)\s*([\u4e00-\u9fa5]{1,15}?)(?=\s|{unit_pattern}|\d|$)',
        # 商品名+数字，如：葵花13
        rf'([\u4e00-\u9fa5]{1,15}?)\s*(\d+(?:\.\d+)?)(?=\s|{unit_pattern}|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) == 2:  # 商品名+数量 或 数字+商品名
                if match[0].isdigit():  # 数字+商品名
                    product = match[1].strip()
                    quantity = float(match[0])
                else:  # 商品名+数量
                    product = match[0].strip()
                    quantity = float(match[1])
                    
                if product and len(product) > 1:  # 确保商品名不为空且长度大于1
                    if product in goods_dict:
                        goods_dict[product] += quantity
                    else:
                        goods_dict[product] = quantity
            elif len(match) == 3:  # 数字+商品名+数量
                product = match[1].strip()
                quantity = float(match[2])
                if product and len(product) > 1:
                    if product in goods_dict:
                        goods_dict[product] += quantity
                    else:
                        goods_dict[product] = quantity
    
    # 过滤掉一些不是商品的词汇
    exclude_words = {'备注', '上图', '作废', '引用', '已撤回', '撤回', '图片', '表情包', '语音', '视频', '文件', '动画表情', '链接'}
    filtered_goods = {k: v for k, v in goods_dict.items() if k not in exclude_words and len(k) > 1}
    
    return filtered_goods

def analyze_daily_goods_with_llm(date_text, api_key=None, base_url=None):
    '''
    使用大模型分析一天的货物信息
    输入格式: 'YYYY-MM-DD: 消息内容'
    返回格式: {"date": "YYYY-MM-DD", "goods": {商品名: 数量}}
    '''
    # 分割日期和内容
    parts = date_text.split(':', 1)
    if len(parts) != 2:
        return None
    
    date = parts[0].strip()
    content = parts[1].strip()
    
    # 使用大模型提取商品信息
    goods = extract_goods_from_text_with_llm(content, api_key, base_url)
    
    return {
        "date": date,
        "goods": goods
    }

def process_clean_files_with_llm(api_key=None, base_url=None):
    '''
    使用大模型处理所有以clean开头的txt文件
    '''
    # 获取所有以clean开头的txt文件
    clean_files = glob.glob('clean*.txt')
    
    all_results = []
    
    for file_path in clean_files:
        print(f'正在分析文件: {file_path}')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            daily_results = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                print(f'正在分析第{i+1}天的数据...')
                
                # 使用大模型分析每一天的数据
                daily_data = analyze_daily_goods_with_llm(line, api_key, base_url)
                if daily_data:
                    daily_results.append(daily_data)
                    print(f'  {daily_data["date"]}: 识别到 {len(daily_data["goods"])} 种商品')
            
            all_results.extend(daily_results)
            print(f'文件 {file_path} 分析完成，共处理 {len(daily_results)} 天的数据')
        
        except Exception as e:
            print(f'处理文件 {file_path} 时出错: {str(e)}')
    
    return all_results

def save_results_to_json(results, output_file='分析.json'):
    '''
    将结果保存到JSON文件
    '''
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f'结果已保存到 {output_file}')

def main():
    print('开始使用大模型分析聊天记录中的货物信息...')
    
    # 获取API密钥和基础URL
    api_key = os.getenv('OPENAI_API_KEY', input('请输入OpenAI API密钥 (或设置环境变量OPENAI_API_KEY): ') or None)
    if not api_key:
        print('警告: 未提供API密钥，将仅使用本地规则匹配进行分析')
    
    base_url = os.getenv('OPENAI_BASE_URL', input('请输入OpenAI基础URL (可选，直接回车跳过): ') or None)
    if not base_url:
        base_url = None
    
    # 使用大模型处理所有clean开头的文件
    results = process_clean_files_with_llm(api_key, base_url)
    
    if results:
        # 保存结果
        save_results_to_json(results)
        
        # 打印摘要
        print('\n分析完成! 摘要:')
        print(f'总共分析了 {len(results)} 天的数据')
        
        # 显示前几天的数据作为示例
        for i, result in enumerate(results[:3]):
            print(f'\n{result["date"]}:')
            for item, count in result["goods"].items():
                print(f'  {item}: {count}')
        
        if len(results) > 3:
            print('\n...')
    else:
        print('未找到任何数据或分析失败')

if __name__ == '__main__':
    main()
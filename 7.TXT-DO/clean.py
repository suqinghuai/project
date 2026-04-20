import re
import os

def clean_chat_log(input_file, output_file):
    """
    清洗聊天记录文件，清除多媒体消息和撤回消息
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    # 读取原始聊天记录
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 使用字典按日期分组消息
    messages_by_date = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 匹配时间戳行，格式如：2025-01-19 11:22:51 '用户名'
        time_user_pattern = r'^(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}\s+\'([^\']+)\''
        match = re.match(time_user_pattern, line)
        
        if match:
            date = match.group(1)  # 提取日期部分
            username = match.group(2)  # 提取用户名
            
            # 查找下一行消息内容
            i += 1
            if i < len(lines):
                message_line = lines[i].strip()
                
                # 检查是否为多媒体消息（如[图片]、[表情包]等）
                multimedia_patterns = ['[图片]', '[表情包]', '[语音]', '[视频]', '[文件]', '[动画表情]', '[链接]']
                is_multimedia = (message_line in multimedia_patterns or 
                               re.search(r'\\[(图片|表情包|语音|视频|文件|动画表情|链接)\\]', message_line))
                
                # 检查是否为撤回消息
                is_recall = re.search(r'撤回.*消息', message_line) or re.search(r'已撤回', message_line)
                
                if is_multimedia or is_recall:
                    # 跳过这条消息（不保存到结果中）
                    pass
                else:
                    # 处理多行消息内容
                    message_parts = []
                    j = i
                    
                    # 收集连续的消息行，直到遇到下一个时间戳或其他需要过滤的消息
                    while j < len(lines):
                        current_line = lines[j].strip()
                        
                        # 检查下一行是否是新的时间戳
                        next_match = re.match(time_user_pattern, current_line)
                        if next_match:
                            break
                        
                        # 检查是否是多媒体消息或撤回消息
                        current_is_multimedia = (current_line in multimedia_patterns or 
                                               re.search(r'\\[(图片|表情包|语音|视频|文件|动画表情|链接)\\]', current_line))
                        current_is_recall = re.search(r'撤回.*消息', current_line) or re.search(r'已撤回', current_line)
                        
                        if current_is_multimedia or current_is_recall:
                            break
                        
                        # 添加非空行到消息内容中
                        if current_line:
                            message_parts.append(current_line)
                        
                        j += 1
                    
                    # 将多行消息合并成单行，用空格分隔
                    if message_parts:
                        combined_message = ' '.join(message_parts)
                        # 按日期分组消息
                        if date not in messages_by_date:
                            messages_by_date[date] = []
                        messages_by_date[date].append(combined_message)
                    
                    # 更新索引位置
                    i = j - 1
        i += 1
    
    # 将按日期分组的消息合并成最终输出
    cleaned_lines = []
    for date in sorted(messages_by_date.keys()):
        # 将同一个日期的所有消息用空格连接
        all_messages = ' '.join(messages_by_date[date])
        cleaned_lines.append(f"{date}: {all_messages}")
    
    # 将清洗后的内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + '\n')
    
    print(f"清洗完成！共处理 {len(cleaned_lines)} 条有效消息。")
    print(f"结果已保存至: {output_file}")

def main():
    # 获取当前目录下的所有txt文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    txt_files = [f for f in os.listdir(current_dir) if f.endswith('.txt') and f != 'main.py']
    
    if not txt_files:
        print("未找到任何txt文件！")
        return
    
    print("找到以下txt文件:")
    for idx, file in enumerate(txt_files, 1):
        print(f"{idx}. {file}")
    
    # 默认处理"聊天记录.txt"，如果存在的话
    target_file = "聊天记录.txt"
    if target_file in txt_files:
        input_path = os.path.join(current_dir, target_file)
        output_path = os.path.join(current_dir, "cleaned_" + target_file)
        
        print(f"\n正在处理: {target_file}")
        clean_chat_log(input_path, output_path)
    else:
        # 如果没有"聊天记录.txt"，则让用户选择
        print("\n请选择要处理的文件编号:")
        try:
            choice = int(input()) - 1
            if 0 <= choice < len(txt_files):
                input_path = os.path.join(current_dir, txt_files[choice])
                output_path = os.path.join(current_dir, "cleaned_" + txt_files[choice])
                
                print(f"正在处理: {txt_files[choice]}")
                clean_chat_log(input_path, output_path)
            else:
                print("无效的选择！")
        except ValueError:
            print("请输入有效的数字！")

if __name__ == "__main__":
    main()
import configparser
import pyautogui
import time
import os

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 读取配置文件
config = configparser.ConfigParser()
config_path = os.path.join(script_dir, 'config5.ini')
config.read(config_path)

# 获取配置参数
time_interval = int(config.get('base', 'time'))
coordinates = config.get('base', 'zuobiao')
x, y = map(int, coordinates.split(','))

print(f"自动点击器已启动")
print(f"脚本目录: {script_dir}")
print(f"配置文件: {config_path}")
print(f"点击间隔: {time_interval}秒")
print(f"点击坐标: ({x}, {y})")
print("按 Ctrl+C 停止")
print("=" * 50)

try:
    while True:
        try:
            # 模拟鼠标点击
            pyautogui.click(x, y)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 执行点击: ({x}, {y})")
            # 等待指定时间
            time.sleep(time_interval)
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 错误: {str(e)}")
            # 等待1秒后继续
            time.sleep(1)
except KeyboardInterrupt:
    print("\n自动点击器已停止")
    # 等待用户按回车键退出
    input("按回车键退出...")
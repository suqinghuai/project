import os
import subprocess
import sys

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# 虚拟环境名称
VENV_NAME = "venv"
# 阿里云镜像源
ALIYUN_MIRROR = "https://mirrors.aliyun.com/pypi/simple/"


def create_venv():
    """创建虚拟环境"""
    print("正在创建虚拟环境...")
    venv_path = os.path.join(PROJECT_ROOT, VENV_NAME)
    
    # 检查虚拟环境是否已存在
    if os.path.exists(venv_path):
        print(f"虚拟环境 {VENV_NAME} 已存在，跳过创建步骤")
        return
    
    # 使用uv创建虚拟环境
    try:
        subprocess.run(
            ["uv", "venv", VENV_NAME],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
        print("虚拟环境创建成功！")
    except subprocess.CalledProcessError as e:
        print(f"创建虚拟环境失败: {e.stderr}")
        sys.exit(1)


def set_aliyun_mirror():
    """在虚拟环境中永久设置阿里云镜像源"""
    print("正在设置阿里云镜像源...")
    
    # 虚拟环境中pip配置文件路径
    pip_ini_path = os.path.join(PROJECT_ROOT, VENV_NAME, "pip.ini")
    
    # 写入pip配置文件
    config_content = f"""[global]
index-url = {ALIYUN_MIRROR}
trusted-host = mirrors.aliyun.com
"""
    
    try:
        with open(pip_ini_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        print("阿里云镜像源设置成功！")
    except Exception as e:
        print(f"设置镜像源失败: {e}")
        sys.exit(1)


def copy_gitignore():
    """复制.gitignore文件"""
    print("正在设置.gitignore文件...")
    gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
    
    # 检查.gitignore文件是否已存在
    if os.path.exists(gitignore_path):
        print(".gitignore文件已存在，跳过复制步骤")
        return
    
    # 模板内容（与现有.gitignore文件内容一致）
    gitignore_content = """# Python 通用
__pycache__/
*.py[cod]
*$py.class
*.so

# 虚拟环境
venv/
env/
.venv/
.env/

# 日志
*.log
*.pdb

# IDE
.idea/
.vscode/

# PyInstaller
build/
dist/
*.spec

# 配置文件
config.ini"""
    
    try:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print(".gitignore文件创建成功！")
    except Exception as e:
        print(f"创建.gitignore文件失败: {e}")
        sys.exit(1)


def create_requirements():
    """创建requirements.txt文件"""
    print("正在创建requirements.txt文件...")
    requirements_path = os.path.join(PROJECT_ROOT, "requirements.txt")
    
    # 检查requirements.txt文件是否已存在
    if os.path.exists(requirements_path):
        print("requirements.txt文件已存在，跳过创建步骤")
        return
    
    # 写入依赖项
    requirements_content = "pyinstaller\n"
    
    try:
        with open(requirements_path, "w", encoding="utf-8") as f:
            f.write(requirements_content)
        print("requirements.txt文件创建成功！")
    except Exception as e:
        print(f"创建requirements.txt文件失败: {e}")
        sys.exit(1)


def install_pyinstaller():
    """安装pyinstaller库"""
    print("正在安装pyinstaller库...")
    
    # 虚拟环境中的Python解释器路径
    python_exe = os.path.join(PROJECT_ROOT, VENV_NAME, "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        print(f"未找到虚拟环境Python解释器: {python_exe}")
        sys.exit(1)

    # 确保pip可用（uv创建的环境可能不包含pip）
    try:
        subprocess.run(
            [python_exe, "-m", "ensurepip", "--upgrade"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
        subprocess.run(
            [python_exe, "-m", "pip", "install", "--upgrade", "pip", "--index-url", ALIYUN_MIRROR, "--trusted-host", "mirrors.aliyun.com"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"初始化pip失败: {e.stderr}")
        sys.exit(1)
    
    try:
        # 使用虚拟环境中的pip安装pyinstaller
        subprocess.run(
            [python_exe, "-m", "pip", "install", "pyinstaller", "--index-url", ALIYUN_MIRROR, "--trusted-host", "mirrors.aliyun.com"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
        print("pyinstaller安装成功！")
    except subprocess.CalledProcessError as e:
        print(f"安装pyinstaller失败: {e.stderr}")
        sys.exit(1)


def main():
    """主函数"""
    print("开始初始化Python项目...")
    
    # 1. 创建虚拟环境
    create_venv()
    
    # 2. 设置阿里云镜像源
    set_aliyun_mirror()
    
    # 3. 复制.gitignore文件
    copy_gitignore()
    
    # 4. 创建requirements.txt文件
    create_requirements()
    
    # 5. 安装pyinstaller
    install_pyinstaller()
    
    print("\n项目初始化完成！")


if __name__ == "__main__":
    main()
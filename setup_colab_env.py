import os
from google.colab import drive
import shutil
import subprocess

# 从 GitHub 克隆项目代码
github_repo_url = 'https://github.com/CATCATPAW/rope.git'
local_project_path = '/content/project_rope'
if not os.path.exists(local_project_path):
    print("cloning projects from GitHub...")
    subprocess.run(['git', 'clone', github_repo_url, local_project_path])
else:
    print("Project alreasy exists, skip cloning.")
project_requirements_path = os.path.join(local_project_path, 'requirements.txt')

#从google drive恢复环境
# Step 1: 挂载 Google Drive
drive.mount('/content/drive') #colab中 google drive的挂载目录

# Step 2: 设置 Google Drive 上的路径
#Colab 挂载路径 (/content/drive/MyDrive/) 是你 在 Colab 里 drive.mount('/content/drive') 后的路径
drive_base_path = '/content/drive/MyDrive/rope'  # Google Drive存放项目相关文件的主目录，例如虚拟环境压缩包和 requirements.txt
env_tar_path = os.path.join(drive_base_path, 'envcfm.tar.gz')


# Step 3: 解压虚拟环境到 Colab
env_path = '/content/env'
if not os.path.exists(env_path):
    print("unpack env...")
    try:
        shutil.unpack_archive(env_tar_path, env_path)
        print(f"env unpacked into: {env_path}")
    expect Exception as e:
        print(f"fail to unpack env: {e}")
else:
    print(f"env already exists: {env_path}")

# Step 4: 安装依赖包
# 如果你的 Colab 中使用的是不同的 Python 版本，删除colab预安装的版本，通过 requirements.txt 安装依赖
import subprocess

def check_pytorch_installed():
    try:
        # 检查是否安装了 PyTorch
        result = subprocess.run(['pip', 'show', 'torch'], capture_output=True, text=True)
        if "Version:" in result.stdout:
            version = result.stdout.split("Version:")[1].split("\n")[0].strip()
            print(f"PyTorch is installed, version: {version}")
            return True
        else:
            print("PyTorch is not installed.")
            return False
    except Exception as e:
        print(f"Error checking PyTorch installation: {e}")
        return False

def uninstall_pytorch():
    try:
        print("Uninstalling PyTorch...")
        subprocess.run(['pip', 'uninstall', 'torch', '-y'], check=True)
        print("PyTorch uninstalled successfully.")
    except Exception as e:
        print(f"Error uninstalling PyTorch: {e}")

def install_requirements():
    try:
        print("Installing dependencies from requirements.txt...")
        subprocess.run(['pip', 'install', '-r', project_requirements_path], check=True)
        print("Dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")

if os.path.exists(project_requirements_path):
        # 检查是否安装了 PyTorch
    if check_pytorch_installed():
        # 卸载 PyTorch
        uninstall_pytorch()
    # 安装 requirements.txt 中的依赖
    install_requirements()    
else:
    print(f"dependencies {project_requirements_path} doesn't exitst,skip.")

# Step 5: 设置 PATH 环境变量，激活虚拟环境
bin_path = os.path.join(env_path, 'bin')
os.environ['PATH'] = f"{bin_path}:{os.environ['PATH']}"

# 验证 Python 和 pip 是否是虚拟环境专属版本
print("env Python version:")
subprocess.run(['python', '--version'])
print("env pip version:")
subprocess.run(['pip', '--version'])



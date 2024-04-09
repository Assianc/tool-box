import subprocess

# 获取已安装的软件包列表
completed_process = subprocess.run(['pip', 'list', '--format=freeze'], capture_output=True, text=True)

# 拆分输出，获取软件包名列表
installed_packages = [line.split('==')[0] for line in completed_process.stdout.split('\n') if line]

# 更新每个软件包
for package in installed_packages:
    subprocess.run(['pip', 'install', '--upgrade', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

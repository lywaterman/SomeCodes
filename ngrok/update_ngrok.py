import requests
import json
import paramiko
from os.path import expanduser

url = 'http://localhost:4040/api/tunnels'
response = requests.get(url)

data = response.content.decode()

obj = json.loads(data)

# 提取 public_url
public_url = obj['tunnels'][0]['public_url']

# 打印 public_url
print(public_url)

# 设置 SSH 服务器的连接参数
hostname = '8.210.47.108'  # 将其替换为实际主机名或 IP 地址
username = 'root'  # 将其替换为实际用户名
private_key_path = expanduser("~/.ssh/id_rsa")  # 将其替换为实际私钥文件路径

# 加载私钥
private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

# 创建 SSH 客户端并连接到服务器
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加服务器的主机密钥（仅用于测试，生产环境下不安全）

with client:
    client.connect(hostname, username=username, pkey=private_key)

    # 在服务器上执行命令
    command = f'python3 /root/check_ngrok.py "{public_url}"'  # 将其替换为要在服务器上执行的实际命令
    stdin, stdout, stderr = client.exec_command(command)

    # 打印命令的输出
    print("命令输出:")
    print(stdout.read().decode('utf-8'))

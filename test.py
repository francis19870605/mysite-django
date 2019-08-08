from django.utils.text import slugify
from slugify import slugify

print(slugify("zao shang hao"))
print(slugify("zao_shang_hao"))
print(slugify("zao*shang*hao"))
print(slugify("早上好"))


import socket


def get_host_ip():
    """
    通过UDP获取本机IP地址：通过UDP协议生成一个UDP包，然后从UDP包中获取本机的IP地址。
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

print(get_host_ip())
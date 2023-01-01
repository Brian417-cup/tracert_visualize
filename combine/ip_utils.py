import socket


# 是否是ipv4
def is_ipv4(ip: str):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except AttributeError:
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False
        return ip.count('.') == 3
    except socket.error:
        return False
    return True


# 是否是ipv6
def is_ipv6(ip: str):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except socket.error:
        return False
    return True


# 判断是不是ip
def check_ip(ip):
    return is_ipv4(ip) or is_ipv6(ip)

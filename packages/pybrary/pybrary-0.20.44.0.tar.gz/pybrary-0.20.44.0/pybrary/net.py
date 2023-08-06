from urllib.request import urlopen


def get_ip_adr():
    url = 'http://api.ipify.org'
    with urlopen(url, timeout=1) as resp:
        if resp.status==200:
            adr = resp.read().decode().strip()
            return True, adr
        else:
            return False, resp.reason

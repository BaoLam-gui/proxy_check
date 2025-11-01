import requests
import socket
import threading

sources = [
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://raw.githubusercontent.com/tranchikiet/Proxy-Collections/refs/heads/main/proxies.txt",
]


proxies = set()
valid_proxies = []
lock = threading.Lock()

def fetch(url):
    try:
        r = requests.get(url, timeout=2)
        if r.ok:
            for line in r.text.splitlines():
                proxy = line.strip()
                if proxy.count(":") == 1:
                    with lock:
                        proxies.add(proxy)
    except:
        pass

def valid(proxy, timeout=1):
    try:
        ip, port = proxy.split(":")
        socket.create_connection((ip, int(port)), timeout=timeout).close()
        with lock:
            valid_proxies.append(proxy)
            print(f"Working: {proxy}")
    except:
        pass

threads = [threading.Thread(target=fetch, args=(src,)) for src in sources]
[t.start() for t in threads]
[t.join() for t in threads]
print(f"Total: {len(proxies)}")

check_threads = [threading.Thread(target=valid, args=(proxy,)) for proxy in proxies]
[t.start() for t in check_threads]
[t.join() for t in check_threads]

with open("proxies_valid.txt", "w") as f_valid:
    f_valid.write("\n".join(sorted(valid_proxies)))
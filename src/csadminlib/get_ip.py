import subprocess, socket

def get_ip_bash():
        with subprocess.Popen('ip route list', shell=True, stdout=subprocess.PIPE) as proc:
                data = (proc.communicate())[0].split()
        return data[data.index('src') + 1]

def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('10.255.255.255', 1))
        ip_address = sock.getsockname()[0]
    except:
        ip_address = '127.0.0.1'
    finally:
        sock.close()
        return ip_address
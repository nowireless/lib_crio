import os
import netifaces
import platform
import crio


class NetworkError(RuntimeError):
    pass


def check_interfaces(team):
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        info = netifaces.ifaddresses(interface)
        if netifaces.AF_INET not in info:
            continue
        if len(info[netifaces.AF_INET]) == 0:
            continue
        if 'addr' not in info[netifaces.AF_INET][0]:
            continue
        try:
            if info[netifaces.AF_INET][0]['addr'] == crio.team_to_ds(team):
                return True
        except:
            pass
    return False


def ping(host):
    """
    From ping man page:
    If a packet count and deadline are both specified, and fewer than count packets are
    received by the time the deadline has arrived, it will also exit with code 1.
    On other error it exits with code 2. Otherwise it exits with code 0. This makes it
    possible to use the exit code to see if a host is alive or not.
    """
    if platform.system() == "Windows":
        raise NetworkError, "Unsupported platform for ping"
    else:
        print type(host)
        return os.system("ping -c1 " + host)


def is_host_alive(host):
    return ping(host) == 0

if __name__ == "__main__":
    print check_interfaces(3081)

import re
import time
import sys
import os
import ssl
import socket
from . import socks as socks

TIMEOUT = 30


def get_status_code(response_string: str) -> int:
    """
    :param response_string: response string from server
    :type response_string: str
    :return: status code
    :rtype: int
    """
    try:
        response_header_lines = response_string.split("\r\n", maxsplit=1)
        if response_header_lines and len(response_header_lines) > 0:
            status_line = response_header_lines[0]
            status_code = int(re.search(r"\d{3}", status_line).group())
            return status_code
        else:
            return 0
    except IndexError:  # for split() and accessing list elements
        return 0
    except AttributeError:  # for re.search() return None
        return 0
    except ValueError:  # for int() conversion
        return 0


def request(request_bytes: bytes, host: str, port: int, tls: bool = True, socks5=False, socks_proxy_ip: str = None,
            socks_port: int = None) -> bytes:
    """
    :param host: host name to connect to
    :param port: listening port for host
    :type request_bytes: bytes
    :type host: str
    :type tls: bool
    :type socks5: bool
    :type socks_proxy_ip: int
    :type socks_port: int
    """
    # socks 5 proxy
    start_time = time.perf_counter()
    
    if socks5:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks_proxy_ip, socks_port)
        s = socks.socksocket()
    
    # for only tls connections
    if tls and not socks5:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.settimeout(30)  # 30s timeout
    
    s.connect((host, port))
    if tls:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.check_hostname = True
        ssl_context.load_default_certs()
        if sys.platform != 'linux':
            try:
                import \
                    certifi  # Windows or Mac users will need to install certifi, as verify mode is set to CERT_REQUIRED, ssl.CertificateError may
                # arise and break the code
                ssl_context.load_verify_locations(
                    cafile=os.path.relpath(certifi.where()),
                    capath=None,
                    cadata=None)
            except ImportError:
                sys.exit("Certify is required for TLS connections. Setup instructions can be found inside the README.")
        s = ssl_context.wrap_socket(s,
                                    server_hostname=host)  # if socks5 is used with tls , "s" will already be a "socks.sockssocket()" object
    
    s.send(request_bytes)
    res_bytes = b""
    
    while True:
        
        end_time = time.perf_counter() - start_time
        if end_time >= TIMEOUT:
            raise TimeoutError
        
        new = s.recv(256)
        if not new:
            s.close()
            break
        res_bytes += new
    
    res_string = res_bytes.decode('utf-8', errors='ignore')
    
    # get status code from decoded response bytes
    status_code = get_status_code(res_string)
    
    return res_bytes, status_code

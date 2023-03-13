from . import handle_connections, parse_raw_header

CONTENT_TYPE_FORM = "application/x-www-form-urlencoded"


class API:
    def __init__(self, RUNTIME_COOKIE: str, host: str, port: int, tls: bool, socks5_ip: str, socks5_port: int,
                 socks5: bool):
        super(API, self).__init__()
        self.socks5 = socks5
        self.socks5_port = socks5_port
        self.socks5_ip = socks5_ip
        self.tls = tls
        self.port = port
        self.host = host
        self.RUNTIME_COOKIE = RUNTIME_COOKIE
        self.redirect = False
    
    def set_cookie(self, cookie_value):  # used to deal with setting of cookies for the whole session
        self.RUNTIME_COOKIE = cookie_value
    
    def get_cookie(self):
        return self.RUNTIME_COOKIE
    
    def make_request(self, request_bytes: bytes, return_header=False):
        resp_bytes, status_code = handle_connections.request(request_bytes, self.host, self.port, self.tls, self.socks5,
                                                             self.socks5_ip, self.socks5_port)
        header_string, resp = parse_raw_header.resp_header_parse(resp_bytes, do_return=True)
        if return_header:
            return header_string, resp
        return resp
    
    def api_call(self, request_alias: str, payload: bytes = None, params=None):
        if params is None:
            params = {}
        if request_alias == 'GET /json/account':
            request = """\
GET /json/account HTTP/1.1\r
Host: {host}\r
Cookie: {cookie}\r
Connection: close\r
\r\n
"""
            request_bytes = request.format(
                host=self.host,
                cookie=self.RUNTIME_COOKIE
            ).encode('utf-8')
            resp = self.make_request(request_bytes)
            return resp
        elif request_alias == 'GET /json/cashout':
            request = """\
GET /json/cashout HTTP/1.1\r
Host: {host}\r
Cookie: {cookie}\r
Connection: close\r
\r\n
"""
            request_bytes = request.format(
                cookie=self.RUNTIME_COOKIE,
                host=self.host
            ).encode('ascii')
            resp = self.make_request(request_bytes)
            return resp
        elif request_alias == 'GET /json/tables':
            request = "GET /json/tables HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            request_bytes = request.format(
                host=self.host
            ).encode('utf-8')
            
            header_string, resp = self.make_request(request_bytes, return_header=True)
            if header_string and not self.RUNTIME_COOKIE:
                header_json = parse_raw_header.header_to_json(header_string)
                if 'Cookie' in header_json:
                    self.set_cookie(header_json['Cookie'])
            return resp
        elif request_alias == 'POST /json/table/{table_id}/join':
            request = """\
POST /json/table/{table_id}/join HTTP/1.1\r
Content-Type: {content_type}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            request_bytes = request.format(
                table_id=params['table_id'],
                content_type=CONTENT_TYPE_FORM,
                cookie=self.RUNTIME_COOKIE,
                host=self.host,
            ).encode('utf-8')
            header_string, resp = self.make_request(request_bytes, return_header=True)
            return resp
        elif request_alias == 'POST /json/table/{table_id}/join/confirm':
            headers = """\
POST /json/table/{table_id}/join/confirm HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            header_bytes = headers.format(
                table_id=params['table_id'],
                content_type=CONTENT_TYPE_FORM,
                content_length=len(payload),
                cookie=self.RUNTIME_COOKIE,
                host=self.host
            ).encode('utf-8')
            request_bytes = header_bytes + payload
            header_string, resp = self.make_request(request_bytes, return_header=True)
            return resp
        elif request_alias == 'GET /json/join':
            request = "GET /json/join HTTP/1.1\r\nHost: {host}\r\nCookie: {cookie}\r\nConnection: close\r\n\r\n"
            request_bytes = request.format(
                host=self.host,
                cookie=self.RUNTIME_COOKIE
            ).encode('utf-8')
            resp_bytes, status_code = handle_connections.request(request_bytes, self.host, self.port, self.tls,
                                                                 self.socks5,
                                                                 self.socks5_ip, self.socks5_port)
            header_string, image_data = parse_raw_header.resp_header_parse(resp_bytes, do_return=False, captcha=True)
            if header_string and image_data:
                return image_data
        elif request_alias == 'POST /json/send':
            headers = """\
POST /json/send HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            header_bytes = headers.format(
                content_type=CONTENT_TYPE_FORM,
                content_length=len(payload),
                cookie=self.RUNTIME_COOKIE,
                host=self.host,
            ).encode('utf-8')
            request_bytes = header_bytes + payload
            resp = self.make_request(request_bytes)
            return resp
        elif request_alias == 'GET /json/send':
            request = """GET /json/send HTTP/1.1\r
Host:{host}\r
Cookie: {Cookie}
Connection: close\r
\r\n"""
            request_bytes = request.format(
                host=self.host,
                Cookie=self.RUNTIME_COOKIE
            ).encode('utf-8')
            resp = self.make_request(request_bytes)
            return resp
        elif request_alias == 'GET /json/table/{table_id}':
            headers = """\
GET /json/table/{table_id} HTTP/1.1\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            header_bytes = headers.format(
                table_id=params["table_id"],
                cookie=self.RUNTIME_COOKIE,
                host=self.host,
            ).encode('utf-8')
            return self.make_request(header_bytes)
        elif request_alias == "POST /json/table/{table_id}/call":
            headers = """\
POST /json/table/{table_id}/call HTTP/1.1\r
Content-Type: {content_type}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            header_bytes = headers.format(
                table_id=params['table_id'],
                content_type=CONTENT_TYPE_FORM,
                cookie=self.RUNTIME_COOKIE,
                host=self.host,
            ).encode('utf-8')
            return self.make_request(header_bytes)
        elif request_alias == 'POST /json/table/{table_id}/fold':
            headers = """\
POST /json/table/{table_id}/fold HTTP/1.1\r
Content-Type: {content_type}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            header_bytes = headers.format(
                table_id=params['table_id'],
                content_type=CONTENT_TYPE_FORM,
                cookie=self.RUNTIME_COOKIE,
                host=self.host,
            ).encode('utf-8')
            resp = self.make_request(header_bytes)
            return resp
        elif request_alias == 'POST /json/table/{table_id}/check':
            request = """\
POST /json/table/{table_id}/check HTTP/1.1\r
Content-Type: {content_type}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            request_bytes = request.format(
                table_id=params['table_id'],
                content_type=CONTENT_TYPE_FORM,
                cookie=self.RUNTIME_COOKIE,
                host=self.host
            ).encode('utf-8')
            resp = self.make_request(request_bytes)
            return resp
        elif request_alias == 'POST /json/table/{table_id}/raise':
            headers = """\
POST /json/table/{table_id}/raise HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            header_bytes = headers.format(
                table_id=params["table_id"],
                content_type=CONTENT_TYPE_FORM,
                content_length=len(payload),
                cookie=self.RUNTIME_COOKIE,
                host=self.host,
            ).encode('utf-8')
            resp = self.make_request(header_bytes + payload)
            return resp
        elif request_alias == 'POST /json/table/{table_id}/message':
            headers = """\
POST /json/table/{table_id}/message HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            header_bytes = headers.format(
                table_id=params['table_id'],
                content_type=CONTENT_TYPE_FORM,
                content_length=len(payload),
                cookie=self.RUNTIME_COOKIE,
                host=self.host,
            ).encode('utf-8')
            request_bytes = header_bytes + payload
            resp = self.make_request(request_bytes)
            if resp is not None:
                return resp
            return None
        elif request_alias == 'GET /json/table/{table_id}/quit':
            headers = """\
GET /json/table/{table_id}/quit HTTP/1.1\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
            header_bytes = headers.format(
                host=self.host,
                cookie=self.RUNTIME_COOKIE,
                table_id=params['table_id']
            ).encode('utf-8')
            header_string, resp = self.make_request(header_bytes, return_header=True)
            return resp

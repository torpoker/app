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
        resp_bytes = handle_connections.request(request_bytes, self.host, self.port, self.tls, self.socks5,
                                                self.socks5_ip, self.socks5_port)
        header_string, resp = parse_raw_header.resp_header_parse(resp_bytes, do_return=True)
        if return_header:
            return header_string, resp
        return resp

    def api_call(self, request_alias: str, payload: bytes = None, params=None):
        if params is None:
            params = {}


        request_mapping = {
            'GET /json/account': self.get_json_account,
            'GET /json/join': self.get_json_join,
            'GET /json/tables': self.get_json_tables,
            'GET /json/table/{table_id}': lambda: self.get_table_by_id(params["table_id"]),
            'GET /json/table/{table_id}/quit': lambda: self.quit_table(params['table_id']),
            'GET /json/send': self.get_json_send,
            'GET /json/cashout': self.get_json_cashout,

            'POST /json/table/{table_id}/join': lambda: self.post_json_table_join(params['table_id'], payload),
            'POST /json/table/{table_id}/join/confirm': lambda: self.post_json_table_join_confirm(params['table_id'],
                                                                                                  payload),
            'POST /json/table/{table_id}/call': lambda: self.post_table_call(params['table_id']),
            'POST /json/table/{table_id}/fold': lambda: self.post_table_fold(params['table_id']),
            'POST /json/table/{table_id}/check': lambda: self.post_table_check(params['table_id']),
            'POST /json/table/{table_id}/raise': lambda: self.post_table_raise(params["table_id"], payload),
            'POST /json/table/{table_id}/message': lambda: self.post_message_to_table(params['table_id'], payload),
            'POST /json/send': lambda: self.post_json_send(payload)

        }

        func = request_mapping.get(request_alias)
        if not func:
            raise ValueError(f"Unbekannter request_alias: {request_alias}")
        if callable(func):
            return func()
        else:
            return func

    def post_json_table_join(self, table_id, payload):
        """
        Sendet einen POST-Request, um einem Tisch beizutreten.

        :param table_id: Die ID des Tisches, zu dem beigetreten werden soll.
        :param payload: Die zu sendenden Daten als Byte-String.
        :return: Die Antwort des Servers auf den Beitrittsversuch.
        """

        headers = """\
    POST /json/table/{table_id}/join HTTP/1.1\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Cookie: {cookie}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""

        request_headers_bytes = headers.format(
            table_id=table_id,
            content_type=CONTENT_TYPE_FORM,
            content_length=len(payload),
            cookie=self.RUNTIME_COOKIE,
            host=self.host
        ).encode('utf-8')

        request_bytes = request_headers_bytes + payload

        header_string, response = self.make_request(request_bytes, return_header=True)
        return response












    def quit_table(self, table_id):
        headers = """\
    GET /json/table/{table_id}/quit HTTP/1.1\r
    Cookie: {cookie}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""
        header_bytes = headers.format(
            host=self.host,
            cookie=self.RUNTIME_COOKIE,
            table_id=table_id
        ).encode('utf-8')
        header_string, resp = self.make_request(header_bytes, return_header=True)
        return resp

    def get_tables(self):
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

    def post_message_to_table(self, table_id, payload):
        CONTENT_TYPE_FORM = 'application/x-www-form-urlencoded'
        headers = """\
    POST /json/table/{table_id}/message HTTP/1.1\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Cookie: {cookie}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""
        header_bytes = headers.format(
            table_id=table_id,
            content_type=CONTENT_TYPE_FORM,
            content_length=len(payload),
            cookie=self.RUNTIME_COOKIE,
            host=self.host,
        ).encode('utf-8')
        request_bytes = header_bytes + payload
        resp = self.make_request(request_bytes)
        return resp

    def post_table_raise(self, table_id, payload):
        CONTENT_TYPE_FORM = 'application/x-www-form-urlencoded'
        headers = """\
POST /json/table/{table_id}/raise HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
        header_bytes = headers.format(
            table_id=table_id,
            content_type=CONTENT_TYPE_FORM,
            content_length=len(payload),
            cookie=self.RUNTIME_COOKIE,
            host=self.host,
        ).encode('utf-8')
        response = self.make_request(header_bytes + payload)
        return response

    def post_table_fold(self, table_id):
        CONTENT_TYPE_FORM = 'application/x-www-form-urlencoded'
        headers = """\
POST /json/table/{table_id}/fold HTTP/1.1\r
Content-Type: {content_type}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
        header_bytes = headers.format(
            table_id=table_id,
            content_type=CONTENT_TYPE_FORM,
            cookie=self.RUNTIME_COOKIE,
            host=self.host,
        ).encode('utf-8')
        response = self.make_request(header_bytes)
        return response

    # New method to handle check action
    def post_table_check(self, table_id):
        CONTENT_TYPE_FORM = 'application/x-www-form-urlencoded'
        request = """\
POST /json/table/{table_id}/check HTTP/1.1\r
Content-Type: {content_type}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
        request_bytes = request.format(
            table_id=table_id,
            content_type=CONTENT_TYPE_FORM,
            cookie=self.RUNTIME_COOKIE,
            host=self.host
        ).encode('utf-8')
        response = self.make_request(request_bytes)
        return response

    def get_table_by_id(self, table_id):
        headers = """\
GET /json/table/{table_id} HTTP/1.1\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
        header_bytes = headers.format(
            table_id=table_id,
            cookie=self.RUNTIME_COOKIE,
            host=self.host,
        ).encode('utf-8')
        return self.make_request(header_bytes)


    def post_table_call(self, table_id):
        headers = """\
POST /json/table/{table_id}/call HTTP/1.1\r
Content-Type: {content_type}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
        header_bytes = headers.format(
            table_id=table_id,
            content_type=CONTENT_TYPE_FORM,
            cookie=self.RUNTIME_COOKIE,
            host=self.host,
        ).encode('utf-8')
        return self.make_request(header_bytes)

    def post_json_send(self, payload):
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
        return self.make_request(request_bytes)


    def get_json_send(self):
        request = """GET /json/send HTTP/1.1\r
Host:{host}\r
Cookie: {Cookie}\r
Connection: close\r
\r\n"""
        request_bytes = request.format(
            host=self.host,
            Cookie=self.RUNTIME_COOKIE
        ).encode('utf-8')
        return self.make_request(request_bytes)



    def post_json_table_join_confirm(self, table_id, payload):
        """
        Sendet eine POST-Anfrage zur Bestätigung der Teilnahme an einem Tisch.
        :param table_id: Die ID des Tisches.
        :param payload: Die zu sendenden Daten als Byte-String.
        :return: Die Antwort des Servers als Byte-String.
        """
        headers = """\
POST /json/table/{table_id}/join/confirm HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Cookie: {cookie}\r
Host: {host}\r
Connection: close\r
\r\n"""
        header_bytes = headers.format(
            table_id=table_id,
            content_type=self.CONTENT_TYPE_FORM,
            content_length=len(payload),
            cookie=self.RUNTIME_COOKIE,
            host=self.host
        ).encode('utf-8')
        request_bytes = header_bytes + payload
        header_string, response = self.make_request(request_bytes, return_header=True)
        return response

    def get_json_tables(self):
        """
        Sendet eine GET-Anfrage, um die Liste der Tabellen abzurufen.
        :return: Die Antwort des Servers.
        """
        request = "GET /json/tables HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        request_bytes = request.format(host=self.host).encode('utf-8')

        header_string, response = self.make_request(request_bytes, return_header=True)


        if header_string and not self.RUNTIME_COOKIE:
            header_json = parse_raw_header.header_to_json(header_string)
            if 'Cookie' in header_json:
                self.set_cookie(header_json['Cookie'])

        return response


    def get_json_tables(self):
        """
        Sendet eine GET-Anfrage, um die Liste der Tabellen abzurufen.
        :return: Die Antwort des Servers.
        """
        request = "GET /json/tables HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        request_bytes = request.format(host=self.host).encode('utf-8')

        header_string, response = self.make_request(request_bytes, return_header=True)


        if header_string and not self.RUNTIME_COOKIE:
            header_json = parse_raw_header.header_to_json(header_string)
            if 'Cookie' in header_json:
                self.set_cookie(header_json['Cookie'])

        return response

    def get_json_join(self):
        """
        Verarbeitet eine GET-Anfrage für Beitrittsinformationen und gibt Bilddaten zurück, falls vorhanden.
        """

        request = "GET /json/join HTTP/1.1\r\nHost: {host}\r\nCookie: {cookie}\r\nConnection: close\r\n\r\n"
        request_bytes = request.format(
            host=self.host,
            cookie=self.RUNTIME_COOKIE
        ).encode('utf-8')


        resp_bytes = handle_connections.request(
            request_bytes, self.host, self.port, self.tls, self.socks5, self.socks5_ip, self.socks5_port
        )


        header_string, image_data = parse_raw_header.resp_header_parse(resp_bytes, do_return=False, captcha=True)
        if header_string and image_data:
            return image_data
        else:
            return None

    def get_json_account(self):
            request_template = """GET /json/account HTTP/1.1\r
Host: {host}\r
Cookie: {cookie}\r
Connection: close\r
\r\n"""
            request = request_template.format(
                host=self.host,
                cookie=self.RUNTIME_COOKIE
            ).encode('utf-8')
            response = self.make_request(request)
            return response

    def get_json_cashout(self):
        request_template = """\
    GET /json/cashout HTTP/1.1\r
    Host: {host}\r
    Cookie: {cookie}\r
    Connection: close\r
    \r\n"""
        request = request_template.format(
            host=self.host,
            cookie=self.RUNTIME_COOKIE
        ).encode('ascii')  # Verwende 'ascii' wie in deinem Original-Code
        response = self.make_request(request)
        return response



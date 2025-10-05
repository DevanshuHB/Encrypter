import urllib.parse

class URLEncode:
    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        return urllib.parse.quote(input_data)

class URLDecode:
    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        return urllib.parse.unquote(input_data)

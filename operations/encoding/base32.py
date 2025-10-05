import base64

class Base32Encode:
    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        return base64.b32encode(input_data.encode('utf-8')).decode('utf-8')

class Base32Decode:
    def execute(self, input_data):
        try:
            return base64.b32decode(input_data).decode('utf-8', errors='ignore')
        except Exception:
            return "Invalid Base32 input"

class HexEncode:
    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        return input_data.encode('utf-8').hex()

class HexDecode:
    def execute(self, input_data):
        try:
            return bytes.fromhex(input_data).decode('utf-8', errors='ignore')
        except ValueError:
            return "Invalid hex input"

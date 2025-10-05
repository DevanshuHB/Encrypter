class ROT47Encode:
    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        result = []
        for char in input_data:
            ascii_code = ord(char)
            if 33 <= ascii_code <= 126:
                result.append(chr(33 + ((ascii_code + 14) % 94)))
            else:
                result.append(char)
        return ''.join(result)

class ROT47Decode:
    def execute(self, input_data):
        # ROT47 encoding is symmetric
        return ROT47Encode().execute(input_data)

class CaesarCipherEncode:
    def __init__(self, shift=3):
        self.shift = shift

    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        result = ''
        for char in input_data:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + self.shift) % 26 + base)
            else:
                result += char
        return result

class CaesarCipherDecode:
    def __init__(self, shift=3):
        self.shift = shift

    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        result = ''
        for char in input_data:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base - self.shift) % 26 + base)
            else:
                result += char
        return result

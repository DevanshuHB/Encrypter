import codecs

class ROT13Encode:
    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        return codecs.encode(input_data, 'rot_13')

class ROT13Decode:
    def execute(self, input_data):
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8', errors='ignore')
        return codecs.decode(input_data, 'rot_13')

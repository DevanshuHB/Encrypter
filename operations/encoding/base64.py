import base64
from operations.base_operation import BaseOperation

class Base64Encode(BaseOperation):
    """
    Base64 encoding operation.
    """

    def __init__(self):
        super().__init__("Base64 Encode", "Encode data using Base64 encoding")

    def execute(self, input_data):
        try:
            self.validate_input(input_data)
            if isinstance(input_data, str):
                input_data = input_data.encode('utf-8')
            encoded = base64.b64encode(input_data)
            return encoded.decode('utf-8')
        except Exception as e:
            return self.handle_exception(e)

class Base64Decode(BaseOperation):
    """
    Base64 decoding operation.
    """

    def __init__(self):
        super().__init__("Base64 Decode", "Decode Base64 encoded data")

    def execute(self, input_data):
        try:
            self.validate_input(input_data)
            if isinstance(input_data, str):
                input_data = input_data.encode('utf-8')
            decoded = base64.b64decode(input_data)
            return decoded.decode('utf-8')
        except Exception as e:
            return self.handle_exception(e)

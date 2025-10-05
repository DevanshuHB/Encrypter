import hashlib
from operations.base_operation import BaseOperation

class MD5Hash(BaseOperation):
    """
    MD5 hashing operation.
    """

    def __init__(self):
        super().__init__("MD5 Hash", "Generate MD5 hash of input data")

    def execute(self, input_data):
        try:
            self.validate_input(input_data)
            if isinstance(input_data, str):
                input_data = input_data.encode('utf-8')
            hash_obj = hashlib.md5(input_data)
            return hash_obj.hexdigest()
        except Exception as e:
            return self.handle_exception(e)

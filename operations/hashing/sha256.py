import hashlib
from operations.base_operation import BaseOperation

class SHA256Hash(BaseOperation):
    """
    SHA256 hashing operation.
    """

    def __init__(self):
        super().__init__("SHA256 Hash", "Generate SHA256 hash of input data")

    def execute(self, input_data):
        try:
            self.validate_input(input_data)
            if isinstance(input_data, str):
                input_data = input_data.encode('utf-8')
            hash_obj = hashlib.sha256(input_data)
            return hash_obj.hexdigest()
        except Exception as e:
            return self.handle_exception(e)

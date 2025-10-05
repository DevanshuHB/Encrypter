from abc import ABC, abstractmethod

class BaseOperation(ABC):
    """
    Abstract base class for all operations in Encrypter.
    Implements OOP principles and provides a common interface.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, input_data):
        """
        Execute the operation on the input data.
        Must be implemented by subclasses.
        """
        pass

    def validate_input(self, input_data):
        """
        Validate input data before processing.
        Can be overridden by subclasses for specific validation.
        """
        if not isinstance(input_data, (str, bytes)):
            raise ValueError("Input data must be string or bytes")

    def handle_exception(self, exception):
        """
        Handle exceptions during operation execution.
        Can be overridden by subclasses for specific error handling.
        """
        return f"Error in {self.name}: {str(exception)}"

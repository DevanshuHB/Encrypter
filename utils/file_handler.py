import os
import tempfile
from werkzeug.utils import secure_filename

class FileHandler:
    """
    Utility class for handling file operations.
    Includes file reading, writing, and validation.
    """

    ALLOWED_EXTENSIONS = {'txt', 'csv', 'json', 'xml', 'html', 'md', 'py', 'js', 'css'}

    @staticmethod
    def allowed_file(filename):
        """
        Check if file extension is allowed.
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileHandler.ALLOWED_EXTENSIONS

    @staticmethod
    def secure_filename(filename):
        """
        Secure the filename to prevent directory traversal attacks.
        """
        return secure_filename(filename)

    @staticmethod
    def read_file_content(file_path, mode='r'):
        """
        Read file content with proper error handling.
        """
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try reading as binary
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")

    @staticmethod
    def write_file_content(file_path, content, mode='w'):
        """
        Write content to file with proper error handling.
        """
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Error writing file: {str(e)}")

    @staticmethod
    def get_file_info(file_path):
        """
        Get file information (size, type, etc.).
        """
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'extension': os.path.splitext(file_path)[1],
                'filename': os.path.basename(file_path)
            }
        except Exception as e:
            return {'error': f"Error getting file info: {str(e)}"}

    @staticmethod
    def create_temp_file(content, suffix='.tmp'):
        """
        Create a temporary file with given content.
        Returns the file path.
        """
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
                f.write(content)
                return f.name
        except Exception as e:
            raise Exception(f"Error creating temp file: {str(e)}")

    @staticmethod
    def cleanup_temp_file(file_path):
        """
        Clean up temporary file.
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Warning: Could not delete temp file {file_path}: {e}")

    @staticmethod
    def validate_file_size(file, max_size=10*1024*1024):  # 10MB default
        """
        Validate file size.
        """
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        return size <= max_size

    @staticmethod
    def detect_file_type(content):
        """
        Simple file type detection based on content.
        """
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')

        content_lower = content.lower()

        if content_lower.startswith('<?xml') or content_lower.startswith('<'):
            return 'XML/HTML'
        elif content_lower.startswith('{') or content_lower.startswith('['):
            return 'JSON'
        elif ',' in content and '\n' in content:
            return 'CSV'
        elif 'def ' in content or 'import ' in content:
            return 'Python'
        elif 'function' in content or 'var ' in content:
            return 'JavaScript'
        else:
            return 'Text'

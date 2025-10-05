# Encrypter - CyberChef Clone

## Overview

Encrypter is a Python-based web application inspired by CyberChef. It allows users to perform various data transformation operations such as encoding, decoding, hashing, and encryption through a user-friendly web interface. Users can create and apply sequences of operations called "recipes" to transform input data.

## Features

- Flask backend with RESTful routes for main page, operation management, recipe application, and data analysis.
- Support for multiple encoding and hashing operations (Base64, Base32, Hex, URL, Caesar cipher, ROT13, ROT47, MD5, SHA256).
- Session-based recipe management with add/remove operations.
- File upload support for input data.
- Encryption strength analysis with visualization using matplotlib.
- User authentication with registration, login, and logout.
- Persistent recipe saving and history viewing.
- Responsive UI with clear layout and controls.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up MySQL database using the provided schema in `database/schema.sql`.
4. Configure database credentials in `app.py`.
5. Run the Flask app:
   ```
   python app.py
   ```

## Usage

- Access the main page at `http://localhost:5000/`.
- Register and login to save recipes and view history.
- Add operations to your recipe, input text or upload a file, and click "Bake!" to apply transformations.
- Use the data analysis page to analyze encryption strength of your recipes.
- Save recipes with names for future use and view them in your history.

## Screenshots

*(Add screenshots here showing the main page, data analysis page, login/register forms, and history page.)*

## Testing

- Basic manual testing has been performed for core features.
- Further thorough testing is recommended for all UI flows, backend endpoints, and edge cases.

## License

MIT License

## Contact

For questions or contributions, please contact the project maintainer.

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymysql
import threading
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from operations.encoding.base64 import Base64Encode, Base64Decode
from operations.hashing.md5 import MD5Hash
from operations.hashing.sha256 import SHA256Hash
from operations.hashing.md5_decoder import MD5Decoder
from operations.hashing.sha256_decoder import SHA256Decoder
from operations.encoding.rot13 import ROT13Encode, ROT13Decode
from operations.encoding.rot47 import ROT47Encode, ROT47Decode
from operations.encoding.url_encode import URLEncode, URLDecode
from operations.encoding.hex import HexEncode, HexDecode
from operations.encoding.base32 import Base32Encode, Base32Decode
from operations.encoding.caesar import CaesarCipherEncode, CaesarCipherDecode

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

from utils.data_analysis import DataAnalyzer, generate_pie_chart
from flask import request

# Database connection parameters
DB_HOST = 'localhost'
DB_USER = 'YOUR MYSQL USERNAME'
DB_PASSWORD = 'YOUR MYSQL PWD'
DB_NAME = 'encrypter'

def get_db_connection():
    return pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           password=DB_PASSWORD,
                           db=DB_NAME,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

# Initialize operations
operations = {
    'base64_encode': Base64Encode(),
    'base64_decode': Base64Decode(),
    'md5_hash': MD5Hash(),
    'md5_verify': MD5Decoder(),
    'sha256_hash': SHA256Hash(),
    'sha256_verify': SHA256Decoder(),
    'rot13_encode': ROT13Encode(),
    'rot13_decode': ROT13Decode(),
    'rot47_encode': ROT47Encode(),
    'rot47_decode': ROT47Decode(),
    'url_encode': URLEncode(),
    'url_decode': URLDecode(),
    'hex_encode': HexEncode(),
    'hex_decode': HexDecode(),
    'base32_encode': Base32Encode(),
    'base32_decode': Base32Decode(),
    'caesar_encode': CaesarCipherEncode(),
    'caesar_decode': CaesarCipherDecode()
}

@app.route('/')
def index():
    recipe = session.get('recipe', [])
    return render_template('index.html', recipe=recipe, input_data='', result='')

def analyze_strength(selected_ops):
    """
    Analyze the strength of the selected encryption and hashing operations.
    This is a heuristic implementation based on known algorithm strengths.
    """
    strength_score = 100
    details = []

    # Example heuristic rules
    weak_algorithms = ['md5_hash', 'md5_verify', 'caesar_encode', 'caesar_decode', 'rot13_encode', 'rot13_decode', 'rot47_encode', 'rot47_decode']
    strong_algorithms = ['sha256_hash', 'sha256_verify', 'base64_encode', 'base64_decode', 'base32_encode', 'base32_decode']

    for op in selected_ops:
        if op in weak_algorithms:
            strength_score -= 30
            details.append(f"{op} is considered weak or easily crackable.")
        elif op in strong_algorithms:
            strength_score += 10
            details.append(f"{op} is considered strong.")
        else:
            details.append(f"{op} strength is unknown or neutral.")

    # Clamp score between 0 and 100
    strength_score = max(0, min(100, strength_score))

    if strength_score >= 80:
        assessment = "Strong"
    elif strength_score >= 50:
        assessment = "Moderate"
    else:
        assessment = "Weak"

    return {
        'score': strength_score,
        'assessment': assessment,
        'details': details
    }

@app.route('/data-analysis', methods=['GET', 'POST'])
def data_analysis():
    operations_list = list(operations.keys())
    recipe = session.get('recipe', [])
    stats = []
    pie_chart = None
    error = None

    if request.method == 'POST':
        if 'add_operation' in request.form:
            operation = request.form.get('operation')
            if operation:
                recipe.append(operation)
                session['recipe'] = recipe
        elif 'analyze' in request.form:
            if not recipe:
                error = "No operations in recipe to analyze."
            else:
                strength = analyze_strength(recipe)
                stats = strength['details']
                pie_chart = generate_pie_chart(strength['score'])
    return render_template('data_analysis.html',
                           operations=operations_list,
                           recipe=recipe,
                           stats=stats,
                           pie_chart=pie_chart,
                           error=error)

@app.route('/add-operation', methods=['POST'])
def add_operation():
    operation = request.form.get('operation')
    if not operation:
        return redirect(url_for('index'))
    recipe = session.get('recipe', [])
    recipe.append(operation)
    session['recipe'] = recipe
    return redirect(url_for('index'))

@app.route('/apply-recipe', methods=['POST'])
def apply_recipe():
    recipe = session.get('recipe', [])
    # Check if this is a remove operation request
    if 'remove_op' in request.form:
        op_to_remove = request.form.get('remove_op')
        if op_to_remove in recipe:
            recipe.remove(op_to_remove)
        session['recipe'] = recipe
        return redirect(url_for('index'))

    input_text = request.form.get('input_text', '')
    input_file = request.files.get('input_file')
    if input_file and input_file.filename != '':
        input_text = input_file.read().decode('utf-8', errors='ignore')
    if not input_text:
        error = "No input data provided"
        return render_template('index.html', recipe=recipe, input_data='', result='', error=error)
    # For demonstration, just concatenate operation names and input
    result = input_text
    for op in recipe:
        if op in operations:
            result = operations[op].execute(result)
        else:
            result = f"Unknown operation: {op}"
            break
    return render_template('index.html', recipe=recipe, input_data=input_text, result=result)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error="Username already exists")
        password_hash = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/save-recipe', methods=['POST'])
def save_recipe():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    recipe = session.get('recipe', [])
    input_data = request.form.get('input_data', '')
    output_data = request.form.get('output_data', '')
    name = request.form.get('name', 'Unnamed Recipe')
    recipe_data = json.dumps(recipe)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (user_id, name, recipe_data, input_data, output_data) VALUES (%s, %s, %s, %s, %s)",
                   (user_id, name, recipe_data, input_data, output_data))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

import json

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, name, recipe_data, input_data, output_data, created_at FROM recipes WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    recipes = cursor.fetchall()
    conn.close()
    # Convert recipe_data JSON string back to list
    for r in recipes:
        r['recipe_data'] = json.loads(r['recipe_data'])
    return render_template('history.html', recipes=recipes)

from flask import flash

@app.route('/delete-recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    # Ensure the recipe belongs to the logged-in user
    cursor.execute("SELECT id FROM recipes WHERE id = %s AND user_id = %s", (recipe_id, user_id))
    recipe = cursor.fetchone()
    if recipe:
        cursor.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
        conn.commit()
        flash('Recipe deleted successfully.', 'success')
    else:
        flash('Recipe not found or unauthorized.', 'error')
    conn.close()
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)

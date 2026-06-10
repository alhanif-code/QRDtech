import bcrypt
from flask import Flask, redirect, render_template, request, jsonify, send_from_directory, url_for, session
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from config import Config
import mysql.connector
import qrcode
import io
import base64
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config["UPLOAD_FOLDER"]="images"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

mysql = MySQL(app)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
    
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM dataqr WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
    
        if existing_user:
            return jsonify({'status':'error','message': 'Email already registered'}), 400
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO dataqr (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        return jsonify({'status':'success','message': 'User registered successfully'}), 201
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'status':'error','message': 'All fields are required'}), 400
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM dataqr WHERE username = %s OR email = %s"
    cursor.execute(query, (username, email))
    user = cursor.fetchone()

    cursor.close()
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return jsonify({'status':'success','message': 'Login successful'}), 200
        else:
            return jsonify({'status':'error','message': 'Invalid credentials'}), 401
    else:
        return jsonify({'status':'error','message': 'Invalid credentials'}), 401
    

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'status':'success','message': 'Logged out successfully'}), 200

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('register'))
    return render_template('url-link.html')
        

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.get_json()
    name = data.get('name')
    url = data.get('url')
    filename = data.get('filename')

    qr = qrcode.make(url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return jsonify({
        'qr_code': img_base64,
        'name':name,
        'filename': filename
    })
    

@app.route('/drag-drop')
def drag_drop():
    return render_template('drag-drop.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get("myuserfile")
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    
    file_url = url_for("user_uploaded", filename=filename, _external=True)
    qr = qrcode.make(file_url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    os.remove(filepath)
    return jsonify({
            'qrcode': img_base64,
            'file_url': file_url,
            'filename': filename
        })
    
@app.route('/images/<filename>')
def user_uploaded(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    

from flask import Flask, render_template, request, redirect, url_for, flash, session
import cv2
import tensorflow as tf
import numpy as np
import os
import sqlite3
import json
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    # Results table
    c.execute('''CREATE TABLE IF NOT EXISTS user_results (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    predicted_category TEXT,
                    recommended_products TEXT,
                    improvement INTEGER
                )''')
    conn.commit()
    conn.close()

init_db()

# Load trained model
model = tf.keras.models.load_model("CNNF.model")
DATADIR = 'train'
CATEGORIES = os.listdir(DATADIR)

# Skin type suggestions
skin_tips = {
    "Acne": "Use gentle foaming cleanser twice a day, avoid touching your face, and apply salicylic acid or benzoyl peroxide treatments.",
    "Oily": "Use oil-free moisturizer, lightweight sunscreen, and control excess oil with mattifying products.",
    "Dry": "Use hydrating cleanser, rich moisturizer, and avoid harsh exfoliation. Apply nourishing serums regularly.",
    "Normal": "Maintain your routine with mild cleanser and moisturizer. Use sunscreen daily.",
    "Combination": "Balance oily and dry areas with gentle cleanser and targeted moisturizers."
}

# Sample product database (simulate random products)
PRODUCTS = {
    "Cleanser": [
        {"name":"Garnier Foaming Cleanser","price":200},
        {"name":"Neutrogena Acne Wash","price":350},
        {"name":"Cetaphil Gentle Cleanser","price":500}
    ],
    "Toner":[
        {"name":"Thayers Witch Hazel","price":400},
        {"name":"Pixi Glow Tonic","price":800}
    ],
    "Serum":[
        {"name":"Vitamin C Serum","price":700},
        {"name":"Hyaluronic Acid Serum","price":900}
    ],
    "Moisturizer":[
        {"name":"Neutrogena Oil-Free Moisturizer","price":450},
        {"name":"Nivea Soft Cream","price":300}
    ],
    "Sunscreen":[
        {"name":"La Roche-Posay SPF50","price":1200},
        {"name":"Garnier Light SPF30","price":250}
    ],
    "Treatment":[
        {"name":"Benzoyl Peroxide Gel","price":300},
        {"name":"Salicylic Acid Cream","price":400}
    ]
}

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Upload & predict
@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if 'file' not in request.files:
        flash('No file uploaded!', 'danger')
        return redirect(url_for('dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file!', 'danger')
        return redirect(url_for('dashboard'))
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Image preprocessing
    img_array = cv2.imread(file_path)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img_array = cv2.resize(img_array, (50, 50))
    img_array = np.array(img_array)/255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)
    predicted_category = CATEGORIES[predicted_index]

    # Recommend random products
    recommendations = {}
    import random
    for cat, prod_list in PRODUCTS.items():
        recommendations[cat] = random.choice(prod_list)

    # Improvement check (simplified: random for demo)
    improvement = random.randint(0,10)

    # Save to DB
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_results (user_id, predicted_category, recommended_products, improvement) VALUES (?,?,?,?)",
              (session['user_id'], predicted_category, json.dumps(recommendations), improvement))
    conn.commit()
    conn.close()

    flash('Prediction completed!', 'success')
    return redirect(url_for('dashboard'))

# Dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']

    max_budget = request.args.get('max_budget', type=int)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Last result
    c.execute("SELECT * FROM user_results WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    last_result = c.fetchone()
    last_suggestion = ""
    if last_result:
        products_json = last_result[3]
        if isinstance(products_json, str):
            try:
                products_json = json.loads(products_json)
            except:
                products_json = {}
        # Apply budget filter
        if max_budget:
            filtered_products = {}
            for cat, prod in products_json.items():
                filtered_products[cat] = prod  # keep all products
            last_result = (last_result[0], last_result[2], filtered_products, last_result[4])
        else:
            last_result = (last_result[0], last_result[2], products_json, last_result[4])
        last_suggestion = skin_tips.get(last_result[1], "Follow a dermatologist's advice for best results.")

    # All results
    c.execute("SELECT * FROM user_results WHERE user_id=? ORDER BY id DESC", (user_id,))
    all_results_raw = c.fetchall()
    all_results = []
    for res in all_results_raw:
        products = res[3]
        if isinstance(products, str):
            try:
                products = json.loads(products)
            except:
                products = {}
        all_results.append((res[0], res[2], products, res[4]))
    conn.close()
    return render_template('dashboard.html', last_result=last_result, all_results=all_results,
                           username=session['username'], last_suggestion=last_suggestion)

# Register
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,hashed_password))
            conn.commit(); conn.close()
            flash('Registration successful! Please log in.','success')
            return redirect(url_for('login'))
        except:
            flash('Username already exists!','danger')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?",(username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2],password):
            session['user_id']=user[0]
            session['username']=user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!','danger')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="vexxtor.env")

app = Flask(__name__)
app.secret_key = os.urandom(24)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

def verify_telegram_auth(data):
    check_hash = data.pop('hash')
    data_check_string = '\n'.join([f'{k}={data[k]}' for k in sorted(data)])
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_string = hashlib.new('sha256', data_check_string.encode(), secret_key).hexdigest()
    return hmac_string == check_hash

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html', bot_username=BOT_USERNAME)

@app.route('/auth', methods=["POST"])
def auth():
    data = request.form.to_dict()
    if verify_telegram_auth(data):
        session['user'] = {
            'id': data['id'],
            'first_name': data.get('first_name', ''),
            'username': data.get('username', '')
        }
        return redirect('/dashboard')
    return "Autentificare eșuată", 403

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

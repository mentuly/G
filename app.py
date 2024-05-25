from flask import Flask, request, render_template
import sqlite3
import hashlib
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# Функція для створення таблиці у базі даних SQLite3
def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)')
    conn.commit()
    conn.close()

# Функція для додавання нового користувача до бази даних
def add_user(username, password, email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, hashlib.sha256(password.encode()).hexdigest(), email))
    conn.commit()
    conn.close()

# Функція для надсилання електронного листа
def send_email(email):
    message = Mail(
        from_email='your_email@example.com', # Ваша електронна адреса
        to_emails=email,
        subject='Реєстрація в нашому додатку',
        html_content='<strong>Ви успішно зареєстровані в нашому додатку!</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY')) # API-ключ SendGrid
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

@app.route('/')
def index():
    create_table()
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    add_user(username, password, email)
    send_email(email)
    return 'Реєстрація пройшла успішно! Перевірте вашу електронну пошту.'

if __name__ == '__main__':
    app.run(debug=True)
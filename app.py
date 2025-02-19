import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# 連接到資料庫
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 首頁路由
@app.route('/')
def home():
    return render_template('home.html')

# 產品頁路由
@app.route('/product')
def product():
    return render_template('product.html')

# 品牌介紹頁路由
@app.route('/story')
def story():
    return render_template('story.html')


# 聯繫我們路由
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        line_id = request.form.get('line', None)
        message = request.form.get('message')

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO messages (name, phone, email, line_id, message) VALUES (?, ?, ?, ?, ?)',
            (name, phone, email, line_id, message)
        )
        conn.commit()
        conn.close()
        return '表單已提交！'

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

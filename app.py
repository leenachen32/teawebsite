import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

# 連接到 Railway MySQL 資料庫
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="shuttle.proxy.rlwy.net",  # 這是公共主機名稱
            user="root",  # MySQL 用戶名
            password="wgYGMmXZjiAubQptJGGevkbLIkUpjaiG",  # MySQL 密碼
            port=35087,  # 端口
            database="railway"  # 資料庫名稱
        )
        
        if connection.is_connected():
            print("成功連接到 MySQL 資料庫")
            return connection
        else:
            print("無法連接到資料庫")
            return None

    except mysql.connector.Error as e:
        print(f"連接錯誤: {e}")
        return None

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
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (name, phone, email, line_id, message) VALUES (%s, %s, %s, %s, %s)',
                (name, phone, email, line_id, message)
            )
            conn.commit()
            conn.close()
            return '表單已提交！'
        else:
            return '無法連接到資料庫，請稍後再試。'

    return render_template('contact.html')

if __name__ == '__main__':
    # 測試資料庫連接
    conn = get_db_connection()
    if conn:
        print("資料庫連接成功！")
    else:
        print("資料庫連接失敗！")
    
    app.run(host='0.0.0.0', port=5002, debug=True)

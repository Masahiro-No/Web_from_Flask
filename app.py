from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # สร้างออบเจ็กต์ของคลาส SQLAlchemy
bcrypt = Bcrypt(app) # สร้างออบเจ็กต์ของคลาส Bcrypt
migrate = Migrate(app, db) # สร้างออบเจ็กต์ของคลาส Migrate

login_manager = LoginManager() # สร้างออบเจ็กต์ของคลาส LoginManager
login_manager.init_app(app) # กำหนดให้ LoginManager ใช้กับออบเจ็กต์ของ Flask
login_manager.login_view = 'login' # กำหนดหน้าที่ใช้ในการเข้าสู่ระบบ


@login_manager.user_loader # ฟังก์ชันในการโหลดข้อมูลผู้ใช้
def load_user(user_id): # ฟังก์ชันรับค่า user_id
    return User.query.get(int(user_id))

class Comment(db.Model): # สร้างคลาส Comment สำหรับเก็บข้อมูลความคิดเห็น
    id = db.Column(db.Integer, primary_key=True) # สร้างคอลัมน์ id แบบ primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # สร้างคอลัมน์ user_id แบบ foreign key
    content = db.Column(db.Text, nullable=False) # สร้างคอลัมน์ content แบบ text
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp()) # สร้างคอลัมน์ timestamp แบบ datetime
    page = db.Column(db.String(50), nullable=False) # สร้างคอลัมน์ page แบบ string
    user = db.relationship('User', backref=db.backref('comments', lazy=True)) # สร้างความสัมพันธ์กับคลาส User

class User(db.Model, UserMixin): # สร้างคลาส User สำหรับเก็บข้อมูลผู้ใช้
    id = db.Column(db.Integer, primary_key=True) # สร้างคอลัมน์ id แบบ primary key
    username = db.Column(db.String(150), unique=True, nullable=False) # สร้างคอลัมน์ username แบบ string
    email = db.Column(db.String(150), unique=True, nullable=False) # สร้างคอลัมน์ email แบบ string
    password_hash = db.Column(db.String(256), nullable=False) # สร้างคอลัมน์ password_hash แบบ string

    def set_password(self, password): # ฟังก์ชันในการกำหนดรหัสผ่าน
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8') # กำหนดค่าให้กับคอลัมน์ password_hash

    def check_password(self, password): # ฟังก์ชันในการตรวจสอบรหัสผ่าน
        return bcrypt.check_password_hash(self.password_hash, password) # ตรวจสอบรหัสผ่าน

@app.route('/') # สร้างเส้นทาง URL สำหรับหน้าแรก
def home():
    return render_template("home.html")

@app.route('/about') # สร้างเส้นทาง URL สำหรับหน้าเกี่ยวกับ
def about():
    return render_template("about.html")

@app.route('/register', methods=['GET', 'POST']) # สร้างเส้นทาง URL สำหรับหน้าสมัครสมาชิก
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('อีเมลนี้ถูกใช้แล้ว!', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) # สร้างเส้นทาง URL สำหรับหน้าเข้าสู่ระบบ
def login():
    if request.method == 'POST': # ตรวจสอบว่ามีการส่งข้อมูลแบบ POST มาหรือไม่
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password): # ตรวจสอบว่ามีผู้ใช้นี้อยู่ในฐานข้อมูลหรือไม่
            login_user(user) # เรียกใช้ฟังก์ชัน login_user เพื่อเข้าสู่ระบบ
            flash('เข้าสู่ระบบสำเร็จ!', 'success')
            return redirect(url_for('dashboard')) # ส่งไปยังหน้า dashboard
        else:
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard') # สร้างเส้นทาง URL สำหรับหน้า dashboard
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/story') # สร้างเส้นทาง URL สำหรับหน้าเรื่องราว
@login_required
def story():
    return render_template('story.html', username=current_user.username)

@app.route('/Belebog', methods=['GET', 'POST']) # สร้างเส้นทาง URL สำหรับหน้า Belebog
@login_required # กำหนดให้ต้องเข้าสู่ระบบก่อนเข้าถึงหน้านี้
def Belebog(): 
    if request.method == 'POST': # ตรวจสอบว่ามีการส่งข้อมูลแบบ POST มาหรือไม่
        content = request.form.get('content') # รับค่า content จากฟอร์ม
        if content: # ตรวจสอบว่า content มีค่าหรือไม่
            new_comment = Comment(user_id=current_user.id, content=content, page='Belebog') # สร้างออบเจ็กต์ Comment และกำหนดค่าให้กับคอลัมน์ต่างๆ
            db.session.add(new_comment) # เพิ่มข้อมูลลงในฐานข้อมูล
            db.session.commit() # ยืนยันการเพิ่มข้อมูล
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('Belebog'))

    comments = Comment.query.filter_by(page='Belebog').order_by(Comment.timestamp.desc()).all() # ดึงข้อมูลความคิดเห็นจากฐานข้อมูล
    return render_template('Belebog.html', username=current_user.username, comments=comments) # ส่งข้อมูลไปยังหน้า Belebog


@app.route('/HertaStation', methods=['GET', 'POST']) # สร้างเส้นทาง URL สำหรับหน้า HertaStation
@login_required # กำหนดให้ต้องเข้าสู่ระบบก่อนเข้าถึงหน้านี้
def HertaStation(): 
    if request.method == 'POST': 
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='HertaStation') # เพิ่มคอลัมน์ page='HertaStation'
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('HertaStation'))

    comments = Comment.query.filter_by(page='HertaStation').order_by(Comment.timestamp.desc()).all() # ดึงข้อมูลความคิดเห็นจากฐานข้อมูลจากหน้า HertaStation
    return render_template('HertaStation.html', username=current_user.username, comments=comments) # ส่งข้อมูลไปยังหน้า HertaStation

@app.route('/AstralExpress', methods=['GET', 'POST']) # สร้างเส้นทาง URL สำหรับหน้า AstralExpress
@login_required
def AstralExpress():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='AstralExpress') # เพิ่มคอลัมน์ page='AstralExpress'
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('AstralExpress'))

    comments = Comment.query.filter_by(page='AstralExpress').order_by(Comment.timestamp.desc()).all() # ดึงข้อมูลความคิดเห็นจากฐานข้อมูลจากหน้า AstralExpress
    return render_template('AstralExpress.html', username=current_user.username, comments=comments) # ส่งข้อมูลไปยังหน้า AstralExpress

@app.route('/Xianzhou', methods=['GET', 'POST']) # สร้างเส้นทาง URL สำหรับหน้า Xianzhou
@login_required
def Xianzhou():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='Xianzhou') # เพิ่มคอลัมน์ page='Xianzhou'
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('Xianzhou'))

    comments = Comment.query.filter_by(page='Xianzhou').order_by(Comment.timestamp.desc()).all() # ดึงข้อมูลความคิดเห็นจากฐานข้อมูลจากหน้า Xianzhou
    return render_template('Xianzhou.html', username=current_user.username, comments=comments) # ส่งข้อมูลไปยังหน้า Xianzhou

@app.route('/Penacony', methods=['GET', 'POST']) # สร้างเส้นทาง URL สำหรับหน้า Penacony
@login_required
def Penacony():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='Penacony') # เพิ่มคอลัมน์ page='Penacony'
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('Penacony'))

    comments = Comment.query.filter_by(page='Penacony').order_by(Comment.timestamp.desc()).all() # ดึงข้อมูลความคิดเห็นจากฐานข้อมูลจากหน้า Penacony
    return render_template('Penacony.html', username=current_user.username, comments=comments) # ส่งข้อมูลไปยังหน้า Penacony

@app.route('/Amphoreus', methods=['GET', 'POST']) # สร้างเส้นทาง URL สำหรับหน้า Amphoreus
@login_required
def Amphoreus():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='Amphoreus') # เพิ่มคอลัมน์ page='Amphoreus'
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('Amphoreus'))

    comments = Comment.query.filter_by(page='Amphoreus').order_by(Comment.timestamp.desc()).all() # ดึงข้อมูลความคิดเห็นจากฐานข้อมูลจากหน้า Amphoreus
    return render_template('Amphoreus.html', username=current_user.username, comments=comments) # ส่งข้อมูลไปยังหน้า Amphoreus

@app.route('/logout') # สร้างเส้นทาง URL สำหรับออกจากระบบ
@login_required
def logout():
    logout_user() # เรียกใช้ฟังก์ชัน logout_user เพื่อออกจากระบบ
    flash('ออกจากระบบเรียบร้อย', 'info')
    return redirect(url_for('login')) # ส่งไปยังหน้า login

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

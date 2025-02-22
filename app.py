from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    page = db.Column(db.String(50), nullable=False)  # เพิ่มคอลัมน์นี้
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('เข้าสู่ระบบสำเร็จ!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/Belebog', methods=['GET', 'POST'])
@login_required
def Belebog():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='Belebog')
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('Belebog'))

    comments = Comment.query.filter_by(page='Belebog').order_by(Comment.timestamp.desc()).all()
    return render_template('Belebog.html', username=current_user.username, comments=comments)


@app.route('/HertaStation', methods=['GET', 'POST'])
@login_required
def HertaStation():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='HertaStation')
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('HertaStation'))

    comments = Comment.query.filter_by(page='HertaStation').order_by(Comment.timestamp.desc()).all()
    return render_template('HertaStation.html', username=current_user.username, comments=comments)

@app.route('/AstralExpress', methods=['GET', 'POST'])
@login_required
def AstralExpress():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='AstralExpress')
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('AstralExpress'))

    comments = Comment.query.filter_by(page='AstralExpress').order_by(Comment.timestamp.desc()).all()
    return render_template('AstralExpress.html', username=current_user.username, comments=comments)

@app.route('/Xianzhou', methods=['GET', 'POST'])
@login_required
def Xianzhou():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='Xianzhou')
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('Xianzhou'))

    comments = Comment.query.filter_by(page='Xianzhou').order_by(Comment.timestamp.desc()).all()
    return render_template('Xianzhou.html', username=current_user.username, comments=comments)

@app.route('/Penacony', methods=['GET', 'POST'])
@login_required
def Penacony():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='Penacony')
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('Penacony'))

    comments = Comment.query.filter_by(page='Penacony').order_by(Comment.timestamp.desc()).all()
    return render_template('Penacony.html', username=current_user.username, comments=comments)

@app.route('/Amphoreus', methods=['GET', 'POST'])
@login_required
def Amphoreus():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(user_id=current_user.id, content=content, page='Amphoreus')
            db.session.add(new_comment)
            db.session.commit()
            flash('แสดงความคิดเห็นสำเร็จ!', 'success')
            return redirect(url_for('Amphoreus'))

    comments = Comment.query.filter_by(page='Amphoreus').order_by(Comment.timestamp.desc()).all()
    return render_template('Amphoreus.html', username=current_user.username, comments=comments)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ออกจากระบบเรียบร้อย', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

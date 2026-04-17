<<<<<<< HEAD
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        new_user = User(username=request.form['username'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash("Invalid credentials")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            content=request.form['content'],
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)

    if post.user_id != current_user.id:
        flash("Not authorized!")
        return redirect(url_for('index'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get_or_404(id)

    if post.user_id != current_user.id:
        flash("Not authorized!")
        return redirect(url_for('index'))

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
=======
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        new_user = User(username=request.form['username'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash("Invalid credentials")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            content=request.form['content'],
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)

    if post.user_id != current_user.id:
        flash("Not authorized!")
        return redirect(url_for('index'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get_or_404(id)

    if post.user_id != current_user.id:
        flash("Not authorized!")
        return redirect(url_for('index'))

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
>>>>>>> 8b7f8b851f87f288d58226c292f2715f684e4f97
    app.run(debug=True)
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from random import choice, randint, shuffle
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# db = sqlite3.connect("posts.db")
# db.row_factory = sqlite3.Row
# cur = db.cursor()
# cur.execute("CREATE TABLE comments(id INTEGER PRIMARY KEY, post_id varchar(250) NOT NULL UNIQUE, "
#             "username varchar(250) NOT NULL UNIQUE, text varchar(250) NOT NULL)")
# db.commit()


login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_annonymous(self):
        return False

    def get_id(self):
        conn = sqlite3.connect("posts.db")
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("select * from user")
        user_list = curs.fetchall()
        for usr in user_list:
            if usr["email"] == self.email:
                # print("user found")
                user_id = usr["id"]
                # print("get id", user_id)
                return user_id

    def get_username(self):
        return self.username


@login_manager.user_loader
def load_user(user_id):
    # print(user_id)
    db = sqlite3.connect("posts.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from user where id = (?)", [user_id])
    user = cur.fetchone()
    if user is not None:
        return User(user["username"], user["password"], user["email"])
    else:
        return None


def generate_id():
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    rn_numbers = [choice(numbers) for char in range(randint(4, 8))]
    password_list = rn_numbers
    shuffle(password_list)
    gen_id = "".join(password_list)
    return gen_id


def fetch_user(username):
    u = username
    conn = sqlite3.connect("posts.db")
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute('select * from user where username = (?)', [str(u)])
    data = curs.fetchone()
    print("user found")
    return data


@app.route('/', methods=['GET', 'POST'])
def get_all_posts():
    posts = []
    db = sqlite3.connect("posts.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from blog_post")
    data_list = cur.fetchall()
    for item in data_list:
        entry = {
            "id": item[0],
            "title": item[1],
            "date": item[2],
            "body": item[3],
            "author": item[4],
            "img_url": item[5],
            "subtitle": item[6],
        }
        posts.append(entry)
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'), "pbkdf2:sha256")
        db = sqlite3.connect("posts.db")
        cur = db.cursor()
        if fetch_user(request.form.get('username')) is None:
            cur.execute(f"INSERT INTO user VALUES('{generate_id()}', '{username}', '{email}', '{password}')")
            db.commit()
            user = User(username, password, email)
            login_user(user, remember=True)
            return redirect(url_for('get_all_posts'))
        else:
            flash("User is already there.")
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        db = sqlite3.connect("posts.db")
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("select * from user")
        data_list = cur.fetchall()
        for user in data_list:
            if user["email"] == request.form.get('email'):
                if check_password_hash(user["password"], request.form.get('password')):
                    usr = User(user['username'], user['password'], user['email'])
                    login_user(usr, remember=True)
                    return redirect(url_for('get_all_posts'))
                else:
                    flash("Incorrect Password!")
            else:
                flash("User not Found!")
    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    form = CommentForm()
    if request.method == "POST":
        print(request.form.get("text"))
        print(type(request.form.get("username")))
        try:
            username = current_user.username
            # user_id = current_user.id
            text = request.form.get("text")
            db = sqlite3.connect("posts.db")
            cur = db.cursor()
            cur.execute(f"INSERT INTO comments VALUES('{generate_id()}', '{post_id}', '{username}', '{text}')")
            db.commit()
        except:
            username = "New User"
            # user_id = generate_id()
            text = request.form.get("text")
            db = sqlite3.connect("posts.db")
            cur = db.cursor()
            cur.execute(f"INSERT INTO comments VALUES('{generate_id()}', '{post_id}', '{username}', '{text}')")
            db.commit()
    requested_post = None
    posts = []
    db = sqlite3.connect("posts.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from blog_post")
    data_list = cur.fetchall()
    for item in data_list:
        entry = {
            "id": item[0],
            "title": item[1],
            "date": item[2],
            "body": item[3],
            "author": item[4],
            "img_url": item[5],
            "subtitle": item[6],
        }
        posts.append(entry)
    for blog_post in posts:
        if blog_post["id"] == post_id:
            requested_post = blog_post
    comments = []
    cur.execute("select * from comments where post_id = (?)", str(post_id))
    c_list = cur.fetchall()
    for item in c_list:
        entry = {
            "id": item[0],
            "post_id": item[1],
            "username": item[2],
            "text": item[3],
        }
        comments.append(entry)
    gravatar = Gravatar(app,
                        size=100,
                        rating='g',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)
    return render_template("post.html", post=requested_post, form=form, comments=comments, image=gravatar)


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=['GET', 'POST'])
def add_new_post():
    form = CreatePostForm()
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        author = request.form.get('author')
        img_url = request.form.get('img_url')
        today_date = datetime.today().date()
        data = request.form.get('body')
        print(title, data, today_date)
        db = sqlite3.connect("posts.db")
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("select * from blog_post")
        data_list = cur.fetchall()
        cur.execute(f"INSERT INTO blog_post VALUES('{len(data_list) + 1}', '{title}', '{today_date}', '{data}', '{author}', "
                    f"'{img_url}', '{subtitle}')")
        db.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    posts = []
    db = sqlite3.connect("posts.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from blog_post")
    data_list = cur.fetchall()
    for item in data_list:
        entry = {
            "id": item[0],
            "title": item[1],
            "date": item[2],
            "body": item[3],
            "author": item[4],
            "img_url": item[5],
            "subtitle": item[6],
        }
        posts.append(entry)
    for post in posts:
        if post["id"] == post_id:
            edit_form = CreatePostForm(
                title=post['title'],
                subtitle=post['subtitle'],
                img_url=post['img_url'],
                author=post['author'],
                body=post['body']
            )
            if request.method == 'POST':
                # print("data edited")
                cur.execute(
                    f"UPDATE blog_post SET title='{edit_form.title.data}', subtitle='{edit_form.subtitle.data}',"
                    f"author='{edit_form.author.data}', img_url='{edit_form.img_url.data}',"
                    f"body='{edit_form.body.data}' WHERE id='{post_id}' ")
                db.commit()
                return redirect(url_for("show_post", index=post_id))
            return render_template("make-post.html", form=edit_form, isEdit=True)
        else:
            pass


@app.route("/delete/<int:post_id>", methods=['GET', 'POST'])
def delete_post(post_id):
    db = sqlite3.connect("posts.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(f"DELETE from blog_post WHERE id='{post_id}' ")
    db.commit()
    return redirect(url_for("get_all_posts"))


if __name__ == "__main__":
    app.run(debug=True)

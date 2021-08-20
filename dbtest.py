import sqlite3
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# n_id = 58973
# db = sqlite3.connect("art.db")
# db.row_factory = sqlite3.Row
# cur = db.cursor()
# cur.execute("select * from user where username is ?", str("ryu"))
# cur.execute("select * from user where username = (?)", [n_id])
# user_list = cur.fetchone()
# print(user_list["username"])
# for user in user_list:
# print("id in list", user['id'])
# if user["id"] == user_id:
#     print("user loaded")
# return User(user["username"], user["password"], user["email"])
# else:
# print("user not loaded")
# return None
# cur.execute("CREATE TABLE supplier_groups(group_id integer PRIMARY KEY,group_name text NOT NULL)")
# cur.execute("CREATE TABLE suppliers(supplier_id integer PRIMARY KEY, supplier_name text NOT NULL,
# group_id integer NOT NULL, group_id INTEGER NOT NULL, FOREIGN KEY(group_id) REFERENCES supplier_groups(group_id) )")
# cur.executescript("""
# CREATE TABLE suppliers (
#     supplier_id   INTEGER PRIMARY KEY,
#     supplier_name TEXT    NOT NULL,
#     group_id      INTEGER NOT NULL,
#     FOREIGN KEY (group_id)
#        REFERENCES supplier_groups (group_id)
# );
# """)
# cur.executescript("""
# INSERT INTO supplier_groups (group_name)
# VALUES
#    ('Domestic'),
#    ('Global'),
#    ('One-Time');
# """)
# cur.executescript("""
#
# """)
# cur.execute("select * from supplier_groups where group_id = 2")
# data = cur.fetchone()
# print(data[0])
# db.commit()
# db = SQLAlchemy()
# class User(sqlalchemy.Base):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     name = db.Column(db.String(100))
#     posts = relationship("BlogPost", back_populates="author")
#     comments = relationship("Comment", back_populates="comment_author")

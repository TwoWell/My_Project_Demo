#coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mysql@localhost/myblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=False, nullable=False)
	pwd = db.Column(db.String(300), nullable=False)
	email = db.Column(db.String(120), unique=False, nullable=False)
	phone = db.Column(db.String(120), unique=False, nullable=False)
	age = db.Column(db.Integer, unique=False, nullable=False)
	face = db.Column(db.String(300), unique=False)
	jianjie = db.Column(db.TEXT)
	uuid = db.Column(db.String(300), unique=True, nullable=False)
	addtime = db.Column(db.DATETIME, index=True, default=datetime.now)
	albums = db.relationship('Album',backref='user')
	favors = db.relationship('AlbumFavor',backref='user')

	# def __init__(self,name=None,pwd=None,email=None,age=None,birthday=None,face=None):
	# 	self.name = name
	# 	self.pwd = pwd
	# 	self.email = email
	# 	self.phone = phone
	# 	self.age = age
	# 	self.birthday = birthday
	# 	self.face = face
	# 	self.info = info

	def __repr__(self):
		return '<User %r>' % self.name


class Album(db.Model):
	__tablename__ = 'album'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), unique=False, nullable=False)
	desc = db.Column(db.TEXT)
	photonum = db.Column(db.Integer, default=0)
	privacy = db.Column(db.String(20), default="public")
	clicknum = db.Column(db.Integer, default=0)
	favornum = db.Column(db.Integer, default=0)
	uuid = db.Column(db.String(300), unique=True, nullable=False)
	addtime = db.Column(db.DATETIME, index=True, default=datetime.now)
	tag_id = db.Column(db.Integer,db.ForeignKey('album_tag.id'))
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	favors = db.relationship('AlbumFavor',backref='album')
	photos = db.relationship('Photo',backref='album')

	def __repr__(self):
		return '<Album %r>' % self.title


class AlbumTag(db.Model):
	__tablename__ = 'album_tag'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=False, nullable=False)
	albums = db.relationship('Album',backref='album_tag')

	def __repr__(self):
		return '<AlbumTag %r>' % self.name


class AlbumFavor(db.Model):
	__tablename__ = 'albumFavor'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	album_id = db.Column(db.Integer,db.ForeignKey('album.id'))
	addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

	def __repr__(self):
		return '<AlbumFavor id:%r user_id:%r album_id:%r>' % (self.id,self.user_id,self.album_id)


class Photo(db.Model):
	__tablename__ = 'photo'
	id = db.Column(db.Integer, primary_key=True)
	origname = db.Column(db.String(255), unique=False, nullable=False) #原图文件名
	showname = db.Column(db.String(255), unique=False, nullable=False) #展示图文件名
	thumbname = db.Column(db.String(255), unique=False, nullable=False) #缩略图文件名
	album_id = db.Column(db.Integer,db.ForeignKey('album.id'))
	addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

	def __repr__(self):
		return '<Photo %r>' % self.id



if __name__ == '__main__':
	flag = 0
	if flag == 0:
		db.drop_all()
		db.create_all()
	if flag == 1:
		tag1 = AlbumTag(name='天朝')
		tag2 = AlbumTag(name='日韩')
		tag3 = AlbumTag(name='汽车')
		tag4 = AlbumTag(name='枪械')
		tag5 = AlbumTag(name='球星')
		tag6 = AlbumTag(name='游戏')
		db.session.add(tag1)
		db.session.add(tag2)
		db.session.add(tag3)
		db.session.add(tag4)
		db.session.add(tag5)
		db.session.add(tag6)
		db.session.commit()
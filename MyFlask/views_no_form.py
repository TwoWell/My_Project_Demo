# coding:utf-8

from flask import Flask,render_template,request,redirect,url_for,flash,get_flashed_messages,session
from model import User,db,app
from functools import wraps

# app = Flask(__name__)
app.config['SECRET_KEY'] = 'my name is aluba'


# 登录状态检查装饰器
def is_login_stat(func):
	@wraps(func)
	def decorated_function(*args,**kwargs):
		if "user_name" not in session:
			return redirect(url_for('user_login',next=request.url))
		return func(*args,**kwargs)
	return decorated_function


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/regist/',methods=['GET','POST'])
def user_regist():
	if request.method == 'POST':
		user = User()
		user.name = request.form['user_name']
		user.pwd = request.form['user_pwd']
		user.email = request.form['user_email']
		user.age = request.form['user_age']
		user.birthday = request.form['user_birthday']
		user.face = request.form['user_face']
		u = User.query.filter_by(name=user.name).first()
		if u:
			flash("用户名已经存在",category="regist_error")
			return render_template('user_no_form_regist.html')
		else:
			db.session.add(user)
			db.session.commit()
			flash("注册成功,请登录！",category="regist_success")
			return redirect(url_for('user_login',user_name=user.name))
	return render_template('user_no_form_regist.html')


@app.route('/login/',methods=['GET','POST'])
def user_login():
	if request.method == 'POST':
		username = request.form['user_name']
		userpwd = request.form['user_pwd']
		u = User.query.filter_by(name=username).first()
		if not u:
			flash("用户名不存在",category="login_username_error")
			return render_template('user_login.html')
		else:
			if u.pwd != userpwd:
				flash("密码错误",category="login_userpwd_error")
				return render_template('user_login.html')
			else:
				session['user_name'] = u.name
				# print(request.args)
				if not request.args.get('next'):
					return redirect(url_for('index'))
				else:
					return redirect(request.args['next'])
	return render_template('user_login.html')


@app.route('/logout/')
def logout():
	session.pop('user_name',None)
	if request.args.get('isdel'):
		flash("注销账号成功",category=request.args.get('isdel'))
		return redirect(url_for('index'))
	else:
		flash("退出成功",category="logout_success")
		return redirect(url_for('index'))


@app.route('/center/',methods=['GET','POST'])
@is_login_stat
def user_center():
	return render_template('user_center.html')


@app.route('/detail/',methods=['GET','POST'])
@is_login_stat
def user_detail():
	user = User.query.filter_by(name=session.get('user_name')).first()
	# print(user)
	return render_template('user_menu_template/user_detail.html',user=user)


@app.route('/pwd/',methods=['GET','POST'])
@is_login_stat
def user_pwd():
	if request.method == 'POST':
		old_pwd = request.form['old_pwd']
		new_pwd = request.form['new_pwd']
		user = User.query.filter_by(name=session.get('user_name')).first()
		if old_pwd == new_pwd:
			flash("新输入的密码和旧密码一致，请重新输入！",category="pwd_is_same")
			return render_template('user_menu_template/user_pwd.html')
		elif str(user.pwd) == str(old_pwd):
			user.pwd = str(new_pwd)
			db.session.add(user)
			db.session.commit()
			session.pop('user_name',None)
			flash("修改密码成功，请重新登录！",category="change_pwd_success")
			return redirect(url_for('user_login',user_name=user.name))
		else:
			flash("旧密码输入错误，请重新输入！",category="change_pwd_fail")
			return render_template('user_menu_template/user_pwd.html')
	return render_template('user_menu_template/user_pwd.html')


@app.route('/info/',methods=['GET','POST'])
@is_login_stat
def user_info():
	user = User.query.filter_by(name=session.get('user_name')).first()
	if request.method == 'POST':
		user.name = request.form['user_name']
		user.email = request.form['user_email']
		user.age = request.form['user_age']
		user.birthday = request.form['user_birthday']
		user.face = request.form['user_face']
		db.session.add(user)
		db.session.commit()
		# print(session.get('user_name'))是未修改前的user_name
		session['user_name'] = user.name
		flash("修改个人资料成功！",category="change_info_success")
		return redirect(url_for('user_info'))
	elif request.method == 'GET':
		return render_template('user_menu_template/user_info.html',user=user)
	else:
		flash("修改个人资料失败！",category="change_info_fail")
		return redirect(url_for('user_info'))


@app.route('/del/',methods=['GET','POST'])
@is_login_stat
def user_del():
	if request.method == 'POST':
		del_user = User.query.filter_by(name=session.get('user_name')).first()
		db.session.delete(del_user)
		db.session.commit()
		return redirect(url_for('logout',isdel="del_success"))
	return render_template('user_menu_template/user_del.html')


@app.route('/photo/',methods=['GET','POST'])
@is_login_stat
def user_photo():
	return render_template('user_menu_template/user_photo.html')


@app.route('/collection/',methods=['GET','POST'])
@is_login_stat
def user_collection():
	return render_template('user_menu_template/user_collection.html')


@app.route('/friend/',methods=['GET','POST'])
@is_login_stat
def user_friend():
	return render_template('user_menu_template/user_friend.html')


@app.route('/fans/',methods=['GET','POST'])
@is_login_stat
def user_fans():
	return render_template('user_menu_template/user_fans.html')


@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html',error=error),404


if __name__ == '__main__':
	app.run(debug=True)
# coding:utf-8
import os

import shutil,uuid,random
from functools import wraps
from flask_forms import RegistForm,LoginForm,PwdForm,InfoForm,AlbumInfoForm,AlbumUploadForm
from flask_uploads import UploadSet,IMAGES,configure_uploads
from flask import Flask,render_template,request,redirect,url_for,flash,get_flashed_messages,session

import utils
from model import db,app,User,AlbumTag,Album,Photo,AlbumTag,AlbumFavor
from utils import secure_filename_with_timestamp,create_thumbnail,create_show

# app = Flask(__name__)

#安全秘钥
app.config['SECRET_KEY'] = 'my name is aluba'

#文件上传路径配置、应用注册
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.path.dirname(__file__),"static/upload_files")
photoSet = UploadSet(name='photos',extensions=IMAGES)
configure_uploads(app,photoSet)


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


@app.route('/user/regist/',methods=['GET','POST'])
def user_regist():
	regist_form = RegistForm()
	# print(regist_form.validate_on_submit())
	# print(regist_form.user_name.errors)
	if regist_form.validate_on_submit():
		user = User()
		# user.name = request.form['user_name']
		# user.pwd = request.form['user_pwd']
		# user.email = request.form['user_email']
		# user.age = request.form['user_age']
		# user.birthday = request.form['user_birthday']
		# user.face = request.form['user_face']
		user.name = regist_form.data['user_name']
		user.pwd = regist_form.data['user_pwd']
		user.uuid = str(uuid.uuid4().hex)[0:10]
		user.email = regist_form.data['user_email']
		user.phone = regist_form.data['user_phone']
		user.age = regist_form.data['user_age']
		user.jianjie = regist_form.data['user_jianjie']
		# 也可以用 f = regist_form.user_face.data的方法获得头像文件对象
		f = request.files['user_face']
		# user.face = secure_filename(f.filename)，secure_filename不能防止文件名相同时出现覆盖问题
		user.face = secure_filename_with_timestamp(f.filename)
		# 检查用户上传的头像文件类型,不符合就不用查询数据库了，减少数据库开销
		# flask_wtf.file下的FileAllowed模块能集成实现
		# if not check_file_extension([f.filename],utils.ALLOWED_IMG_EXTENSION):
		# 	flash("上传的头像文件类型错误,请重新上传！",category="upload_img_error")
		# 	return render_template('user_regist.html',regist_form=regist_form)
		u = User.query.filter_by(name=user.name).first()
		if u:
			flash("用户名已经存在",category="regist_error")
			return render_template('user_regist.html',regist_form=regist_form)
		else:
			photoSet.save(storage=f,folder=user.name,name=user.face)
			db.session.add(user)
			db.session.commit()
			# print(os.getcwd()) 文件保存、上传的默认路径是当前工作路径
			# upload_folder_path = os.path.join(os.path.dirname(__file__),"static/upload_files",user.name)
			# if not os.path.exists(upload_folder_path):
			# 	os.mkdir(upload_folder_path)
			# 	# 修改文件读写权限
			# 	# os.makedirs(upload_path)
			# 	# os.chmod(upload_path,os.O_RDWR)
			# upload_path = os.path.join(upload_folder_path,user.face)
			# f.save(upload_path)
			f.close()
			flash("注册成功,请登录！",category="regist_success")
			return redirect(url_for('user_login',user_name=user.name))
	return render_template('user_regist.html',regist_form=regist_form)


@app.route('/user/login/',methods=['GET','POST'])
def user_login():
	login_form = LoginForm()
	if login_form.validate_on_submit():
		# username = request.form['user_name']
		# userpwd = request.form['user_pwd']
		username = login_form.data['user_name']
		userpwd = login_form.data['user_pwd']
		u = User.query.filter_by(name=username).first()
		if not u:
			flash("用户名不存在",category="login_username_error")
			return render_template('user_login.html',login_form=login_form)
		else:
			if u.pwd != userpwd:
				flash("密码错误",category="login_userpwd_error")
				return render_template('user_login.html',login_form=login_form)
			else:
				session['user_name'] = u.name
				session['user_id'] = u.id
				# print(request.args)
				if not request.args.get('next'):
					return redirect(url_for('index'))
				else:
					return redirect(request.args['next'])
	return render_template('user_login.html',login_form=login_form)


@app.route('/user/logout/')
def logout():
	session.pop('user_name',None)
	session.pop('user_id',None)
	if request.args.get('isdel'):
		flash("注销账号成功",category=request.args.get('isdel'))
		return redirect(url_for('index'))
	else:
		flash("退出成功",category="logout_success")
		return redirect(url_for('index'))


@app.route('/user/center/',methods=['GET','POST'])
@is_login_stat
def user_center():
	return render_template('user_center.html')


@app.route('/user/detail/',methods=['GET','POST'])
@is_login_stat
def user_detail():
	user = User.query.get(int(session['user_id']))
	# filter_by(name=session.get('user_name')).first() 因为登录后把user_id放入session了,所以用id索引比较快
	# print(user)
	face_url = photoSet.url(user.name + '/' + user.face)
	return render_template('user_menu_template/user_detail.html',user=user,face_url=face_url)


@app.route('/user/pwd/',methods=['GET','POST'])
@is_login_stat
def user_pwd():
	pwd_form = PwdForm()
	if pwd_form.validate_on_submit():
		old_pwd = pwd_form.data['old_pwd']
		new_pwd = pwd_form.data['new_pwd']
		user = User.query.get(int(session['user_id']))
		if old_pwd == new_pwd:
			flash("新输入的密码和旧密码一致，请重新输入！",category="pwd_is_same")
			return render_template('user_menu_template/user_pwd.html',pwd_form=pwd_form)
		elif str(user.pwd) == str(old_pwd):
			user.pwd = str(new_pwd)
			db.session.add(user)
			db.session.commit()
			session.pop('user_name',None)
			session.pop('user_id',None)
			flash("修改密码成功，请重新登录！",category="change_pwd_success")
			return redirect(url_for('user_login',user_name=user.name))
		else:
			flash("旧密码输入错误，请重新输入！",category="change_pwd_fail")
			return render_template('user_menu_template/user_pwd.html',pwd_form=pwd_form)
	return render_template('user_menu_template/user_pwd.html',pwd_form=pwd_form)


@app.route('/user/info/',methods=['GET','POST'])
@is_login_stat
def user_info():
	info_form = InfoForm()
	user = User.query.get(int(session['user_id']))
	# User.query.filter_by(name=session.get('user_name')).first()
	if info_form.validate_on_submit():
		old_name = user.name
		user.name = info_form.data['user_name']
		user.email = info_form.data['user_email']
		user.phone = info_form.data['user_phone']
		user.age = info_form.data['user_age']
		user.jianjie = info_form.data['user_jianjie']
		filestorage = info_form.user_face.data
		if filestorage !="":
			# print(filestorage)

			# flask_wtf.file下的FileAllowed模块能集成实现
			# if not check_file_extension([filestorage.filename],utils.ALLOWED_IMG_EXTENSION):
			# 	flash("上传的头像文件类型错误,请重新上传！",category="upload_img_error")
			# 	return render_template('user_menu_template/user_info.html',user=user,info_form=info_form)

			# 旧头像文件
			# img_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'],old_name,user.face)
			img_path = photoSet.path(filename=user.face,folder=old_name)
			# shutil.rmtree(path=img_path,ignore_errors=True)
			os.remove(path=img_path)
			# 新上传文件
			user.face = secure_filename_with_timestamp(filestorage.filename)
			# 把改好的文件名封装回filestorage，这样上传的文件名才是加工过的
			# filestorage.filename = user.face
			# new_img_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'],old_name,user.face)
			# filestorage.save(new_img_path)
			photoSet.save(storage=filestorage,folder=old_name,name=user.face)
			db.session.add(user)
			db.session.commit()
		else:
			pass
		# 如果用户修改了用户名，则修改上传文件夹名称
		if old_name != user.name:
			old_dirname = os.path.join(app.config['UPLOADED_PHOTOS_DEST'],old_name)
			new_dirname = os.path.join(app.config['UPLOADED_PHOTOS_DEST'],user.name)
			os.rename(old_dirname,new_dirname)
		# print(session.get('user_name'))是未修改前的user_name
		db.session.add(user)
		db.session.commit()
		session['user_name'] = user.name
		session['user_id'] = user.id
		flash("修改个人资料成功！",category="change_info_success")
		return redirect(url_for('user_detail'))
	elif request.method == 'GET':
		info_form.user_jianjie.data = user.jianjie
		return render_template('user_menu_template/user_info.html',user=user,info_form=info_form)
	else:
		# flash("修改个人资料失败！",category="change_info_fail")
		return render_template('user_menu_template/user_info.html',user=user,info_form=info_form)


@app.route('/user/del/',methods=['GET','POST'])
@is_login_stat
def user_del():
	if request.method == 'POST':
		del_user = User.query.get(int(session['user_id']))
		# User.query.filter_by(name=session.get('user_name')).first()
		# 注销时连同用户上传的静态资源一起删除
		del_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'],del_user.name)
		shutil.rmtree(del_path,ignore_errors=True)
		db.session.delete(del_user)
		db.session.commit()
		return redirect(url_for('logout',isdel="del_success"))
	return render_template('user_menu_template/user_del.html')


@app.route('/user/album/<int:page>',methods=['GET','POST'])
@is_login_stat
def user_album(page):
	albumtags = AlbumTag.query.all()
	tagid = request.args.get('tag','all')
	if tagid == 'all':
		albums = Album.query.filter(Album.user_id == session.get('user_id')).order_by(Album.addtime.desc()).paginate(page=page,per_page=3)
	else:
		# albums = Album.query.all()   全部人都能看不行,要加上权限
		albums = Album.query.filter(Album.user_id == session.get('user_id'),Album.tag_id == tagid).\
		order_by(Album.addtime.desc()).paginate(page=page,per_page=3)
	# albumcoverurls = []
	for album in albums.items:
		coverimg = album.photos[random.randint(0,len(album.photos)-1)].thumbname
		folder = album.user.name + '/' + album.title
		coverimgurl = photoSet.url(filename=folder + '/' + coverimg)
		# albumcoverurls.append(coverimgurl)
		# 可以动态向类添加属性，这样就不用构造一个空数组去存放封面图片的URL了，在HTML模板也不用jinja2的语法获取列表循环
		album.coverimgurl = coverimgurl
	return render_template('user_menu_template/user_album.html',albumtags=albumtags,albums=albums)


@app.route('/user/favor/album/<int:page>',methods=['GET','POST'])
@is_login_stat
def user_favor_album(page):
	albumtags = AlbumTag.query.all()
	tagid = request.args.get('tag','all')
	# 筛选当前登录用户收藏的相册
	# fav_albums = Album.query.filter(AlbumFavor.user_id==session.get('user_id'),Album.id == AlbumFavor.album_id).all()
	# print(fav_albums)
	if tagid == 'all':
		albums = Album.query.filter(AlbumFavor.user_id==session.get('user_id'),Album.id == AlbumFavor.album_id).order_by(Album.addtime.desc()).paginate(page=page,per_page=3)
	else:
		albums = Album.query.filter(Album.tag_id == tagid,AlbumFavor.user_id==session.get('user_id'),Album.id == AlbumFavor.album_id).\
		order_by(Album.addtime.desc()).paginate(page=page,per_page=3)
	# albumcoverurls = []
	for album in albums.items:
		coverimg = album.photos[random.randint(0,len(album.photos)-1)].thumbname
		folder = album.user.name + '/' + album.title
		coverimgurl = photoSet.url(filename=folder + '/' + coverimg)
		# albumcoverurls.append(coverimgurl)
		# 可以动态向类添加属性，这样就不用构造一个空数组去存放封面图片的URL了，在HTML模板也不用jinja2的语法获取列表循环
		album.coverimgurl = coverimgurl
	return render_template(
		'user_menu_template/user_favor_album.html',
		albumtags=albumtags,
		albums=albums
	)


@app.route('/user/friend/',methods=['GET','POST'])
@is_login_stat
def user_friend():
	return render_template('user_menu_template/user_friend.html')


@app.route('/user/fans/',methods=['GET','POST'])
@is_login_stat
def user_fans():
	return render_template('user_menu_template/user_fans.html')


@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html',error=error),404


@app.route('/album/create/',methods=['GET','POST'])
@is_login_stat
def album_create():
	albumInfo_form = AlbumInfoForm()
	if albumInfo_form.validate_on_submit():
		album_title = albumInfo_form.album_title.data
		exist_title_count = Album.query.filter(
			Album.user_id==session['user_id'],
			Album.title==album_title
		).count()
		if exist_title_count>=1:
			flash(message="已创建过该相册,可直接对其进行更新,无需再创建！",category="exist_album_title")
			return render_template('album_template/album_create.html',albumInfo_form=albumInfo_form)
		album_desc = albumInfo_form.album_desc.data
		album_privacy = albumInfo_form.album_privacy.data
		album_tag = albumInfo_form.album_tag.data
		album = Album(
			title=album_title,
			desc=album_desc,
			privacy=album_privacy,
			tag_id=album_tag,
			uuid=str(uuid.uuid4().hex)[0:10],
			user_id=int(session['user_id'])
		)
		db.session.add(album)
		db.session.commit()
		return redirect(url_for('album_upload'))
	return render_template('album_template/album_create.html',albumInfo_form=albumInfo_form)


@app.route('/album/upload/',methods=['GET','POST'])
@is_login_stat
def album_upload():
	albumUpload_form = AlbumUploadForm()
	albums = Album.query.filter_by(user_id=session['user_id']).all()
	albumUpload_form.album_title.choices = [(item.id,item.title) for item in albums]
	if albumUpload_form.validate_on_submit():
		flist = request.files.getlist('album_upload')
		# print(flist)
		for f_id,f_title in albumUpload_form.album_title.choices:
			# 判断下拉选择要上传图片的相册
			if f_id == albumUpload_form.album_title.data:
				album_title = f_title
		folder = session['user_name'] + "/" + album_title
		file_url = []
		for f in flist:
			fname = photoSet.save(storage=f,folder=folder,name=f.filename)
			# 展示、缩略图路径
			ts_path = photoSet.config.destination + '/' + folder
			# 创建并保存缩略图、展示图
			fname_thumbnail = create_thumbnail(path=ts_path,filename=f.filename,base_width=150)
			fname_show = create_show(path=ts_path,filename=f.filename,base_width=800)
			# print(fname_thumbnail)
			# 把产生的Photo对象保存到数据库
			photos = Photo(
				origname=f.filename,
				showname=fname_show,
				thumbname=fname_thumbnail,
				album_id=albumUpload_form.album_title.data
			)
			db.session.add(photos)
			db.session.commit()
			# 获取文件缩略图、展示图URL
			ft_url = photoSet.url(filename=folder + '/' + fname_thumbnail)
			fs_url = photoSet.url(filename=folder + '/' + fname_show)
			file_url.append(ft_url)
		album = Album.query.filter_by(id=albumUpload_form.album_title.data).first()
		album.photonum += len(flist)
		db.session.add(album)
		db.session.commit()
		message = "成功上传保存 %s 张图片; 当前相册共有 %s 张图片"%(str(len(flist)),album.photonum)
		flash(message=message,category="album_upload_success")
		# return redirect(url_for('album_upload'))
		return render_template('album_template/album_upload.html',albumUpload_form=albumUpload_form,file_url=file_url)
	return render_template('album_template/album_upload.html',albumUpload_form=albumUpload_form)


@app.route('/album/list/<int:page>',methods=['GET'])  #不提交任何数据，所以锁定GET方法
def album_list(page):
	albumtags = AlbumTag.query.all()
	tagid = request.args.get('tag','all')
	if tagid == 'all':
		albums = Album.query.filter(Album.privacy != 'private').order_by(Album.addtime.desc()).paginate(page=page,per_page=4)
	else:
		# albums = Album.query.all()   全部人都能看不行,要加上权限
		albums = Album.query.filter(Album.privacy != 'private',Album.tag_id == tagid).\
		order_by(Album.addtime.desc()).paginate(page=page,per_page=4)
	# albumcoverurls = []
	for album in albums.items:
		coverimg = album.photos[random.randint(0,len(album.photos)-1)].thumbname
		folder = album.user.name + '/' + album.title
		coverimgurl = photoSet.url(filename=folder + '/' + coverimg)
		# albumcoverurls.append(coverimgurl)
		# 可以动态向类添加属性，这样就不用构造一个空数组去存放封面图片的URL了，在HTML模板也不用jinja2的语法获取列表循环
		album.coverimgurl = coverimgurl
	return render_template('album_template/album_list.html',albumtags=albumtags,albums=albums)


@app.route('/album/browse/<int:id>',methods=['GET'])
def album_browse(id):
	# 查询当前相册和(如果已登录)当前用户是否存在收藏表(该用户是否收藏了该相册)
	favor_exitCount = AlbumFavor.query.filter_by(user_id=session.get('user_id'),album_id=id).count()
	album = Album.query.get_or_404(id)
	# 增加对应相册的浏览量(先提交数据库,不然后面临时创建的photo.url属性会影响提交结果)
	album.clicknum += 1
	db.session.add(album)
	db.session.commit()
	# 查询推荐相册(这里根据当前浏览的tag标签来推荐)
	recommend_albums = Album.query.filter(
		Album.tag_id == album.tag_id,
		Album.id != album.id,
		Album.user_id != session.get('user_id') # 不推荐当前用户的相册给自己
	).all()
	# 收藏相册展示相关,要判断用户是否登录
	favor_albums = []
	if session.get('user_id'):
		user = User.query.get_or_404(session.get('user_id'))
		for favor in user.favors:
			favor_albums.append(favor.album)
		for favalbum in favor_albums:
			favcoverimg = favalbum.photos[random.randint(0,len(favalbum.photos)-1)].thumbname
			favfolder = favalbum.user.name + '/' + favalbum.title
			favcoverimgurl = photoSet.url(filename=favfolder + '/' + favcoverimg)
			favalbum.favcoverimgurl = favcoverimgurl
	# 给每个推荐相册随机挑选一个相册封面
	for recommend_album in recommend_albums:
		coverimg = recommend_album.photos[random.randint(0,len(recommend_album.photos)-1)].thumbname
		folder = recommend_album.user.name + '/' + recommend_album.title
		coverimgurl = photoSet.url(filename=folder + '/' + coverimg)
		recommend_album.coverimgurl = coverimgurl
	userface_url = photoSet.url(filename=album.user.name + '/' + album.user.face)
	for photo in album.photos:
		photo_folder = album.user.name + '/' + album.title + '/'
		photo.url = photoSet.url(filename=photo_folder + photo.showname)
	return render_template(
		'album_template/album_browse.html',
		album=album,
		userface_url=userface_url,
		recommend_albums=recommend_albums,
		favor_exitCount=favor_exitCount,
		favor_albums=favor_albums
	)


@app.route('/album/favor/',methods=['GET','POST'])
def album_favor():
	aid = request.args.get('aid')
	uid = request.args.get('uid')
	act = request.args.get('act')
	if act == "add":
		# 用户不能收藏自己的相册
		album = Album.query.get_or_404(int(aid))
		if album.user_id == session.get('user_id'):
			res = {'ok':-1}
		else:
			# 查询是否已经收藏过了
			exitCount = AlbumFavor.query.filter_by(user_id=uid,album_id=aid).count()
			# 如果没有收藏过，则添加数据库记录
			if exitCount<1:
				albumfavor = AlbumFavor(album_id=aid,user_id=uid)
				db.session.add(albumfavor)
				db.session.commit()
				res = {'ok':1}
				album.favornum += 1
				db.session.add(album)
				db.session.commit()
			else:
				res = None
	if act == "del":
		del_albumfavor = AlbumFavor.query.filter_by(user_id=uid,album_id=aid).first_or_404()
		db.session.delete(del_albumfavor)
		db.session.commit()
		res = {'ok':2}
		album = Album.query.get_or_404(int(aid))
		album.favornum -= 1
		db.session.add(album)
		db.session.commit()
	import json
	return json.dumps(res)


if __name__ == '__main__':
	app.run(debug=True)
	# app.run(host='0.0.0.0',debug=True)
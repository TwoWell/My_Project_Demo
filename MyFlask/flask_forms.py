from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed # 新的文件表单控件使用,但是非空效果还是原来的小弹框展示
from flask_uploads import IMAGES
from wtforms import StringField,PasswordField,IntegerField,DateField,FileField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,NumberRange,Email,Regexp

from model import AlbumTag


tags = AlbumTag.query.all()

class RegistForm(FlaskForm):
	user_name = StringField(
		label="用户名",
		validators=[DataRequired(),
			Length(min=3,max=15,message="用户名长度在%(min)d到%(max)d个字符之间！")],
		render_kw = {
			"id":"user_name",
			"class":"form-control",
			"placeholder":"请输入用户名"
			}
		)

	user_pwd = PasswordField(
			label="密码",
			validators=[DataRequired(),
				Length(min=3,max=12,message="密码长度在%(min)d到%(max)d个字符之间！")],
			render_kw = {
				"id":"user_pwd",
				"class":"form-control",
				"placeholder":"请输入密码"
				}
			)

	user_email = StringField(
		label="邮箱",
		validators=[DataRequired(),
			Email(message="邮箱格式不对！")
		],
		render_kw = {
			"id":"user_email",
			"class":"form-control",
			"placeholder":"请输入邮箱"
			}
		)

	user_phone = StringField(
		label="手机号码",
		validators=[DataRequired(),
			Regexp("1[3,4,5,8]\d{9}",message="手机号码格式不正确！")],
		render_kw = {
			"id":"user_phone",
			"class":"form-control",
			"placeholder":"请输入手机号码"
			}
		)

	user_age = IntegerField(
		label="年龄",
		validators=[DataRequired(),
			NumberRange(min=18,max=60,message="年龄在%(min)d到%(max)d岁之间！")],
		render_kw = {
			"id":"user_age",
			"class":"form-control",
			"placeholder":"请输入年龄"
			}
		)

	user_face = FileField(
		label="头像",
		validators=[
			FileRequired(message="请上传头像文件！"),
			FileAllowed(IMAGES,"上传的头像文件类型错误,请重新上传！%s"%str(IMAGES))
		],
		render_kw = {
			"id":"user_face",
			"class":"form-control",
			"placeholder":"请选择头像"
			}
		)

	user_jianjie = TextAreaField(
		label="简介",
		render_kw = {
			"id":"user_jianjie",
			"class":"form-control",
			"style":"resize:none",
			"rows":"3",
			"placeholder":"请输入简介"
			}
		)

	submit = SubmitField(
		label="提交表单",
		render_kw = {
			"class":"btn btn-success",
			"value":"注册"
			}
		)


class LoginForm(FlaskForm):
	user_name = StringField(
		label="用户名",
		validators=[],
		render_kw = {
			"id":"user_name",
			"class":"form-control",
			"placeholder":"请输入用户名"
			}
		)

	user_pwd = PasswordField(
			label="密码",
			validators=[DataRequired()],
			render_kw = {
				"id":"user_pwd",
				"class":"form-control",
				"placeholder":"请输入密码"
				}
			)

	submit = SubmitField(
		label="提交表单",
		render_kw = {
			"class":"btn btn-success",
			"value":"登录"
			}
		)


class PwdForm(FlaskForm):
	old_pwd = PasswordField(
		label="用户旧密码",
		validators=[DataRequired(),
			Length(min=3,max=12,message="密码长度在%(min)d到%(max)d个字符之间！")],
		render_kw = {
			"id":"old_pwd",
			"class":"form-control",
			"placeholder":"请输入用户旧密码"
			}
		)

	new_pwd = PasswordField(
			label="用户新密码",
			validators=[DataRequired(),
				Length(min=3,max=12,message="密码长度在%(min)d到%(max)d个字符之间！")],
			render_kw = {
				"id":"new_pwd",
				"class":"form-control",
				"placeholder":"请输入用户新密码"
				}
			)

	submit = SubmitField(
		label="提交表单",
		render_kw = {
			"class":"btn btn-success",
			"value":"修改"
			}
		)


class InfoForm(FlaskForm):
	user_name = StringField(
		label="用户名",
		validators=[DataRequired(),
			Length(min=3,max=15,message="用户名长度在%(min)d到%(max)d个字符之间！")],
		render_kw = {
			"id":"user_name",
			"class":"form-control",
			"placeholder":"请输入用户名"
			}
		)

	user_email = StringField(
		label="邮箱",
		validators=[DataRequired(),
			Email(message="邮箱格式不对！")
		],
		render_kw = {
			"id":"user_email",
			"class":"form-control",
			"placeholder":"请输入邮箱"
			}
		)

	user_phone = StringField(
		label="手机号码",
		validators=[DataRequired(),
			Regexp("1[3,4,5,8]\d{9}",message="手机号码格式不正确！")],
		render_kw = {
			"id":"user_phone",
			"class":"form-control",
			"placeholder":"请输入手机号码"
			}
		)

	user_age = IntegerField(
		label="年龄",
		validators=[DataRequired(),
			NumberRange(min=18,max=60,message="年龄在%(min)d到%(max)d岁之间！")],
		render_kw = {
			"id":"user_age",
			"class":"form-control",
			"placeholder":"请输入年龄"
			}
		)

	user_face = FileField(
		label="头像",
		validators=[
			FileAllowed(IMAGES,"上传的头像文件类型错误,请重新上传！%s"%str(IMAGES))
		],
		render_kw = {
			"id":"user_face",
			"class":"form-control",
			"placeholder":"请选择头像"
			}
		)

	user_jianjie = TextAreaField(
		label="简介",
		render_kw = {
			"id":"user_jianjie",
			"class":"form-control",
			"style":"resize:none",
			"rows":"3",
			"placeholder":"请输入简介"
			}
		)

	submit = SubmitField(
		label="提交表单",
		render_kw = {
			"class":"btn btn-success",
			"value":"修改"
			}
		)


class AlbumInfoForm(FlaskForm):
	album_title = StringField(
		label="相册标题",
		validators=[DataRequired()],
		render_kw = {
			"id":"album_title",
			"class":"form-control",
			"placeholder":"请输入相册标题"
			}
		)

	album_desc = TextAreaField(
		label="相册描述",
		render_kw = {
			"id":"album_desc",
			"class":"form-control",
			"style":"resize:none",
			"rows":"3",
			"placeholder":"请输入相册描述"
			}
		)

	album_privacy = SelectField(
		label="相册浏览权限",
		validators=[DataRequired()],
		coerce=str,
		choices=[('public','所有人'),('private','仅自己'),('protect-1','粉丝'),('protect-2','相册收藏者')],
		render_kw = {
			"id":"album_privacy",
			"class":"form-control"
			}
		)

	album_tag = SelectField(
		label="相册类别",
		validators=[DataRequired()],
		coerce=int,
		choices=[(tag.id,tag.name) for tag in tags],#从数据库获取下拉选项
		render_kw = {
			"id":"album_tag",
			"class":"form-control"
			}
		)

	submit = SubmitField(
		label="提交表单",
		render_kw = {
			"class":"form-control btn btn-primary",
			"value":"确认提交"
			}
		)


class AlbumUploadForm(FlaskForm):
	album_title = SelectField(
		validators=[DataRequired()],
		coerce=int,
		# choices=[(album.id,album.title) for album in albums],#从数据库获取下拉选项
		render_kw = {
			"id":"album_title",
			"class":"form-control"
			}
		)

	album_upload = FileField(
		validators=[
			FileRequired(message="请选择文件上传！"),
			FileAllowed(IMAGES,"上传的文件类型错误,请重新上传！%s"%str(IMAGES))
		],
		render_kw = {
			"id":"album_upload",
			"class":"form-control",
			"multiple":"multiple",
			"placeholder":"请选择上传文件"
			}
		)

	submit = SubmitField(
		label="提交表单",
		render_kw = {
			"class":"form-control btn btn-primary",
			"value":"开始上传"
			}
		)
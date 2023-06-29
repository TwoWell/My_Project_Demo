# coding:utf-8

from django.http import HttpResponseRedirect
# 如果用户没有登录，无法访问个人信息等相关需要登录后的页面
def login(func):
	def login_func(request,*args,**kwargs):
		if request.session.has_key('user_id'):
			return func(request,*args,**kwargs)
		else:
			red = HttpResponseRedirect('/user/login/')
			red.set_cookie('url',request.get_full_path())
			return red
	return login_func
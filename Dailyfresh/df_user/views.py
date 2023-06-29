# coding:utf-8

from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from . import user_decorator
from .models import *
from hashlib import sha1

def register(request):
	context = {'title':'用户注册'}
	return render(request,'df_user/register.html',context)


def register_exist(request):
	uname = request.GET.get('uname')
	count = UserInfo.objects.filter(uname=uname).count()
	return JsonResponse({'count':count})


def login(request):
	context = {'title':'用户登录'}
	return render(request,'df_user/login.html',context)


def logout(request):
	request.session.flush()
	return redirect('/')


@user_decorator.login
def user_center_info(request):
	user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
	context = {
		'title':'用户中心',
		'user_email':user_email,
		'user_name':request.session['user_name']
	}
	return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def user_center_order(request):
	context = {
		'title':'全部订单',
		'user_name':request.session['user_name']
	}
	return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def user_center_site(request):
	context = {
		'title':'收货地址',
		'user_name':request.session['user_name']
	}
	return render(request,'df_user/user_center_site.html',context)


@user_decorator.login
def cart(request):
	context = {
		'title':'我的购物车',
		'user_name':request.session['user_name']
	}
	return render(request,'df_goods/cart.html',context)


@user_decorator.login
def place_order(request):
	context = {
		'title':'提交订单',
		'user_name':request.session['user_name']
	}
	return render(request,'df_goods/place_order.html',context)


def register_handle(request):
	# 接受用户输入
	post = request.POST
	uname = post.get('user_name')
	upwd = post.get('pwd')
	upwd2 = post.get('cpwd')
	uemail = post.get('email')

	# 密码错误返回注册页
	if upwd != upwd2:
		return redirect('/user/register/')

	# 密码加密
	s1 = sha1()
	s1.update(upwd.encode('utf-8'))
	upwd3 = s1.hexdigest()

	# 创建数据库信息
	user = UserInfo()
	user.uname = uname
	user.upwd = upwd3
	user.uemail = uemail
	user.save()

	# 注册成功，转到登录页面
	return redirect('/user/login/')
	

def login_handle(request):
	post = request.POST
	uname = post.get('username')
	upwd = post.get('pwd')
	users = UserInfo.objects.filter(uname=uname)
	if len(users) == 1:
		s1 = sha1()
		s1.update(upwd.encode('utf-8'))
		if s1.hexdigest() == users[0].upwd:
			url = request.COOKIES.get('url','/')
			red = HttpResponseRedirect(url)
			request.session['user_id']=users[0].id
			request.session['user_name']=uname
			return red
		else:
			context = {
				'title':'用户登录',
				'error_name':0,
				'error_pwd':1,
				'uname':uname,
				'upwd':upwd
			}
			return render(request,'df_user/login.html',context)
	else:
		context = {
			'title':'用户登录',
			'error_name':1,
			'error_pwd':0,
			'uname':uname,
			'upwd':upwd
		}
		return render(request,'df_user/login.html',context)
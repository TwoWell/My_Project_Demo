from django.shortcuts import render

def detail(request):
	context = {'title':'详情页'}
	return render(request,'df_goods/detail.html',context)


def index(request):
	context = {'title':'首页'}
	return render(request,'df_goods/index.html',context)


def list(request):
	context = {'title':'商品页'}
	return render(request,'df_goods/list.html',context)
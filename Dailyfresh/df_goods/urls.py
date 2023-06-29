from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^detail/$',views.detail),
	url(r'^$',views.index),
	url(r'^list/$',views.list),
]
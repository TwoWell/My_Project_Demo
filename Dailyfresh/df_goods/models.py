# coding:utf-8

from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
	ttile = models.CharField(max_length=20)
	isDelete = models.BooleanField(default=False)
	class Meta:
		db_table = 'TypeInfo'


class GoodsInfo(models.Model):
	gtitle = models.CharField(max_length=20)
	gpic = models.ImageField(upload_to='df_goods')
	gprice = models.DecimalField(max_digits=5,decimal_places=2)
	isDelete = models.BooleanField(default=False)
	gunit = models.CharField(max_length=20,default='500g')
	gclick = models.IntegerField()
	gjianjie = models.CharField(max_length=200)
	gkucun = models.IntegerField()
	# 是否推荐（广告）
	gadv = models.BooleanField(default=False)
	gcontent = HTMLField()
	gtype = models.ForeignKey(TypeInfo,on_delete=models.PROTECT)
	class Meta:
		db_table = 'GoodsInfo'
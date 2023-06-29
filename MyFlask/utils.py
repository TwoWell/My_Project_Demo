# coding:utf-8
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image

# 工具类模块，增加各种小功能


# 修改文件名称（不使用文件名安全函数），确保上传、保存文件时文件名不同，防止覆盖
def change_filename_with_timestamp_uuid(filename):
	# 分离文件扩展名和其余部分
	file_info = os.path.splitext(filename)
	filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + file_info[-1]
	return filename


# 修改文件名称（使用文件名安全函数），确保上传、保存文件时文件名不同，防止覆盖
def secure_filename_with_timestamp(filename):
	fname = secure_filename(filename)
	file_info = os.path.splitext(fname)
	filename = file_info[0] + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + file_info[-1]
	return filename


# 检查上传文件的文件后缀名是否符合要求（flask_wtf.file下的FileAllowed模块能集成实现）
# ALLOWED_IMG_EXTENSION = set(['png','jpg','jpeg','gif','bmp'])
# ALLOWED_VIDEO_EXTENSION = set(['mp4','avi','flv','mkv'])
# ALLOWED_AUDIO_EXTENSION = set(['mp3','m4a'])

# def check_file_extension(filename_list,allowed_extensions):
# 	for fname in filename_list:
# 		check_stat = '.' in fname and fname.rsplit('.',1)[1] in allowed_extensions
# 		if not check_stat:
# 			return False
# 	return True


# PIL工具处理JPG格式的图片有点问题，无法修改图片尺寸
def create_thumbnail(path,filename,base_width=150):
	imgname,ext = os.path.splitext(filename)
	newfilename = imgname + '_thumbnail_' + ext   # 缩略图文件名
	img = Image.open(os.path.join(path,filename))
	if img.size[0] > base_width:
		w_percent = float(base_width/float(img.size[0]))
		h_size = int(float(img.size[1] * w_percent))
		img = img.resize((base_width,h_size),Image.ANTIALIAS)
	img.save(os.path.join(path,newfilename))
	return newfilename


def create_show(path,filename,base_width=800):
	imgname,ext = os.path.splitext(filename)
	newfilename = imgname + '_show_' + ext   # 展示（放大）图文件名
	img = Image.open(os.path.join(path,filename))
	if img.size[0] < base_width:
		w_percent = float(base_width/float(img.size[0]))
		h_size = int(float(img.size[1] * w_percent))
		img = img.resize((base_width,h_size),Image.ANTIALIAS)
	img.save(os.path.join(path,newfilename))
	return newfilename
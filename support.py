from os import walk#帮助我们访问不同的文件夹
import pygame

def import_folder(path):
	surface_list = []

	for _, __, img_files in walk(path):#可以print一下，然后发现只有第三个数据是我们需要的列表，因此前面两个随便命名
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()#后面这个是使得这组图片便于操作
			surface_list.append(image_surf)

	return surface_list

def import_folder_dict(path):
	surface_dict = {}

	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_dict[image.split('.')[0]] = image_surf

	return surface_dict
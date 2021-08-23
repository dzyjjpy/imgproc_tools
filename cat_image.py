# -*- coding: utf-8 -*-
# Function: Concat two folder images
# Input:  folder1, folder2
# Output: folder3 (include the cat images for folder1 and folder2)
# Author: Jia Peiyang  Date: 2020/05/27
# Usage:
#         python cat_image.py --src_dir /media/sdc/jiapy/experiments/img_dir/res_deeplabv3plus/  \
#					--dst_dir /media/sdc/jiapy/experiments/img_dir/res_hrnet/          \
#					--res_dir /media/sdc/jiapy/experiments/img_dir/deeplabv3plus_hrnet48_comp/  \

import os
import cv2
import argparse
from tqdm import tqdm
import logging

logging.basicConfig(format=' %(asctime)s - %(message)s ', datefmt='%d-%b-%y %H:%M:%S', filename=None, level=logging.INFO)
logger = logging.getLogger(__name__)

def get_args():
	parser = argparse.ArgumentParser(description='concat image in two folders')
	parser.add_argument('--src_dir', default=None, type=str, required=True, help='img directory or pred mask directory')
	parser.add_argument('--dst_dir', default=None, type=str, required=True, help='mask directory or pred mask directory')
	parser.add_argument('--res_dir', default=None, type=str, required=True, help='result cat directory')
	parser.add_argument('--cat_direction', default="h", type=str, required=False, help='concat direction, v: vertival or h: horizontal')
	parser.add_argument('--name_suffix', default=".png", type=str, required=False, help='dst_dir images suffix, mask: .png, imig: .jpg')
	args = parser.parse_args()
	return args

def cat_image(image_old_path, image_new_path, save_path, cat_dir="h", name_suffix=".png"):
	"""
	:param image_old_path:  img directory or pred mask directory
	:param image_new_path:  mask directory or pred mask directory
	:param save_path: result cat directory
	:param cat_dir: concat direction, v: vertival or h: horizontal
	:param name_suffix: dst_dir images suffix, mask: .png, imig: .jpg
	:return:
	"""
	if image_old_path == None or image_new_path == None:
		logger.info("pls check mask or image path")
	files = os.listdir(image_old_path)

	for file in tqdm(files):
		logger.info("----processing {} ".format(file))
		image_old = cv2.imread(os.path.join(image_old_path, file))
		assert 1 == file.count("."), "----pls check, file name has multiple dot----"
		image_new = cv2.imread(os.path.join(image_new_path, file.split(".")[0] + name_suffix))

		text_remark_old = image_old_path.split("\\")[-1]  #"Ground Truth"
		text_remark_new = image_new_path.split("\\")[-1]  #"Prediction"
		cv2.putText(image_old, text_remark_old, (5, 50), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
		cv2.putText(image_new, text_remark_new, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

		save_file_path = os.path.join(save_path, file)
		if "h" == cat_dir:
			# cv2.hconcat: horizontal direction, two images must have same height
			image_cat = cv2.hconcat((image_old, image_new))
			cv2.imwrite(save_file_path, image_cat)
		elif "v" == cat_dir:
			# cv2.vconcat: vertical direction, two images must have same width
			image_cat = cv2.vconcat((image_old, image_new))
			cv2.imwrite(save_file_path, image_cat)
		else:
			logger.error(" ----cat_direction is not correct----".format(cat_dir))
			return -1
	return 0

def main():
	args = get_args()
	logger.info(args)
	mask_old_path = args.src_dir
	image_new_path = args.dst_dir
	res_path = args.res_dir
	cat_direction = args.cat_direction
	suffix = args.name_suffix

	if os.path.exists(res_path):
		logger.info("----res_path directory {} exist~ ----".format(res_path))
	else:
		logger.info("----res_path directory {} not exist~ ----\n ----create folders----".format(res_path))
		os.mkdir(res_path)
	logger.info("mask_old_path {} ".format(mask_old_path))

	# img: ".jpg" , mask: ".png"
	cat_image(mask_old_path, image_new_path, res_path, cat_dir=cat_direction, name_suffix=suffix)



if __name__ == '__main__':
	main()
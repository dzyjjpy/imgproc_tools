# -*- coding: utf-8 -*-
"""     Statistical Calculation for Datasets Directory
        @Func:  calculate mean, std, average resolution for datasets folder
        @Author: P.Y. Jia   Date: 2021.05.13
        python calc_stat.py --data_path G:/projects/testSky/img/
"""

import os
import cv2
import numpy as np
from tqdm import tqdm
import argparse
import logging

# "cal_stat_0513.txt"
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename=None, level=logging.INFO)
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(description='calculate mean, std, average resolution')
    parser.add_argument('--data_path', default=None, type=str, required=True, help='datasets root path.')
    args = parser.parse_args()
    return args

def compute(path):
    file_names = os.listdir(path)
    per_image_Rmean = []
    per_image_Gmean = []
    per_image_Bmean = []
    per_image_Width_mean = []
    per_image_Height_mean = []

    for file_name in tqdm(file_names):
        file_path = os.path.join(path, file_name)
        assert os.path.exists(file_path), "file path {} not exist".format(file_path)
        img = cv2.imread(file_path, 1)
        logger.info("img.shape {} ".format(img.shape))

        img_width = img.shape[1]
        img_height = img.shape[0]
        per_image_Width_mean.append(img_width)
        per_image_Height_mean.append(img_height)

        per_image_Bmean.append(np.mean(img[:, :, 0])) # B
        per_image_Gmean.append(np.mean(img[:, :, 1])) # G
        per_image_Rmean.append(np.mean(img[:, :, 2])) # R

    R_mean = np.mean(per_image_Rmean)/255
    G_mean = np.mean(per_image_Gmean)/255
    B_mean = np.mean(per_image_Bmean)/255
    stdR = np.std(per_image_Rmean)/255
    stdG = np.std(per_image_Gmean)/255
    stdB = np.std(per_image_Bmean)/255
    width_mean = np.mean(per_image_Width_mean)
    height_mean = np.mean(per_image_Height_mean)

    return R_mean, G_mean, B_mean, stdR, stdG, stdB, width_mean, height_mean

if __name__ == '__main__':
    args = get_args()
    path = args.data_path
    logger.info("    datasets path is: {}".format(path))
    R_mean, G_mean, B_mean, stdR, stdG, stdB, width_mean, height_mean = compute(path)
    logger.info("\nR_mean= {:.3f} \nG_mean= {:.3f} \nR_mean={:.3f} \nstdR ={:.3f} \nstdG = {:.3f} \nstdB = {:.3f} \nwidth_mean ={:.1f} \nheight_mean ={:.1f}"
                .format(R_mean, G_mean, B_mean, stdR, stdG, stdB, width_mean, height_mean))

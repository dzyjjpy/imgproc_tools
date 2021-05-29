# -*- coding: utf-8 -*-
# Perceptron Fish Camera Sky Semantic Segmentation
# convert matting mask(0~255) to binary mask(0 or 255)
# P.Y. Jia  2021.05.12
# python convert_binary_seg.py --dir_path G:/projects/imgproc_tools/testSky/mask --res_path G:/projects/imgproc_tools/testSky/binary_mask

import os
import cv2
import numpy as np
import argparse
from tqdm import tqdm
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename=None, level=logging.WARN)
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(description="Convert matting mask to binary mask")
    parser.add_argument('--dir_path', type=str, required=True, help="directory path: matting mask")
    parser.add_argument('--res_path', type=str, required=True, help="result path: save binary mask)")
    args = parser.parse_args()
    print(args)
    return args

def convert_binary_seg(matting_mask, res_file_path, isSave=True):
    if matting_mask is None:
        print("matting mask is empty")
    binary_mask = None
    n_channel =  (np.atleast_3d(matting_mask)).shape[2]
    if 1 == n_channel:
        binary_mask = matting_mask.copy()
        binary_mask[matting_mask < 128] = 0
        binary_mask[matting_mask >= 128] = 255
    elif 3 == n_channel:
        binary_mask = matting_mask.copy()[:, :, 2] # Red Channel BGR
        binary_mask[matting_mask[:, :, 2] < 128] = 0
        binary_mask[matting_mask[:, :, 2] >= 128] = 255

    if True == isSave:
        cv2.imwrite(res_file_path, binary_mask)
        logger.info("save binary mask{}".format(res_file_path))
    return binary_mask

def main():
    logger.info('     Start convert matting mask to binary mask     ')
    args = get_args()
    mask_path = args.dir_path
    res_path = args.res_path
    logger.info('     mask matting path: {}      '.format(mask_path))
    files = os.listdir(mask_path)
    logger.info('     Start convert matting mask to binary mask     ')
    for file in tqdm(files):
        file_path = os.path.join(mask_path, file)
        assert os.path.exists(file_path), "file not exist, pls check"
        mask_matting = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        logger.info("mask_matting's shape{}".format(mask_matting.shape))
        res_file = os.path.join(res_path, file)
        if os.path.exists(res_path) == False:
            logger.info("res_path not exist! Create directory".format(res_path))
            os.mkdir(res_path)
        mask_binary = convert_binary_seg(mask_matting, res_file, isSave=True)

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
# P.Y. Jia  2021.05.31
# python img_resize.py --img_path img/ --resize_path resize/ --shape 512

from PIL import Image
import numpy as np
import cv2
import os
from tqdm import tqdm
import argparse
import logging

logging.basicConfig(format=' %(asctime)s - %(message)s ', datefmt='%d-%b-%y %H:%M:%S', filename=None, level=logging.WARN)
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(description="Resize image to specific size")
    parser.add_argument('--img_path', type=str, required=True, help="image path")
    parser.add_argument('--resize_path', type=str, required=True, help="resize path")
    parser.add_argument('--h', type=int, required=True, help="resize height")
    parser.add_argument('--w', type=int, required=True, help="resize width")
    args = parser.parse_args()
    print(args)
    return args

def image_resize(img_path, resize_path, shape):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    img_resize = cv2.resize(img, shape)
    cv2.imwrite(resize_path, img_resize)

def main():
    args = get_args()
    img_path = args.img_path
    resize_path = args.resize_path
    resize_shape = (args.w, args.h)  # w, h

    if os.path.exists(resize_path):
        logger.info("resize path exist")
    else:
        os.mkdir(resize_path)
        logger.info("creat resize path: {}".format(resize_path))
    if os.path.exists(resize_path):
        logger.info("resize path {} not exist, create automatically".format(resize_path))
    if os.path.exists(img_path):
        files = os.listdir(img_path)
        for file in tqdm(files):
            img_file_path = os.path.join(img_path, file)
            resize_file_path = os.path.join(resize_path, file)
            image_resize(img_file_path, resize_file_path, shape=resize_shape)
    else:
        logger.info("img_path {} not exist".format(img_path))

if __name__ == "__main__":
    main()


import os
import cv2
import numpy as np
import argparse
from tqdm import tqdm
import shutil
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename=None, level=logging.WARN)
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(description="Convert matting mask to binary mask")
    parser.add_argument('--mask_path', type=str, required=True, help="sky mask directory")
    parser.add_argument('--img_path', type=str, required=True, help="all the images to clean")
    parser.add_argument('--bg_path', type=str, required=True, help="path for saving image that sky pixels ratio less than e.g. 5%")
    parser.add_argument('--sky_path', type=str, required=True, help="path for saving image that sky pixels ratio more than e.g. 30%")
    parser.add_argument('--bg_ratio', type=float, default=0.05, help="bg ratio, default: 0.05")
    parser.add_argument('--sky_ratio', type=float, default=0.30, help="sky_ratio, default: 0.30 ")
    args = parser.parse_args()
    print(args)
    return args

def sky_select(file_name, mask_path, img_path, no_sky_path, sky_path, bg_ratio, sky_ratio, move=True):
    file_mask = os.path.join(mask_path, file_name)
    mask = cv2.imread(file_mask, cv2.IMREAD_UNCHANGED)
    if mask is None:
        return
    total_pixels = mask.shape[0] * mask.shape[1]
    sky_pixels_num = ((mask == 255).sum())
    #bg_pixels_num = ((mask == 0).sum())
    ratio_sky = sky_pixels_num / float(total_pixels)

    file_name_no_suffix = file_name.split(".")[0]
    if ratio_sky < bg_ratio:
        # cp file to no_sky_path
        img_file = os.path.join(img_path, file_name_no_suffix + ".jpg")
        no_sky_file = os.path.join(no_sky_path, file_name_no_suffix + ".jpg")
        if True == move:
            # move to sky_path
            shutil.move(img_file, no_sky_file)
        else:
            # copy file to sky_path
            shutil.copyfile(img_file, no_sky_file)

    if ratio_sky > sky_ratio:
        img_file = os.path.join(img_path, file_name_no_suffix + ".jpg")
        sky_file = os.path.join(sky_path, file_name_no_suffix + ".jpg")
        if True == move:
            # move to sky_path
            shutil.move(img_file, sky_file)
        else:
            # copy file to sky_path
            shutil.copyfile(img_file, sky_file)

def main():
    args = get_args()
    mask_path = args.mask_path
    img_path = args.img_path
    no_sky_path = args.bg_path
    sky_path = args.sky_path
    bg_ratio = args.bg_ratio
    sky_ratio = args.sky_ratio
    if not os.path.exists(no_sky_path):
        os.mkdir(no_sky_path)
    if not os.path.exists(sky_path):
        os.mkdir(sky_path)

    files = os.listdir(mask_path)

    for file in tqdm(files):
        logger.info("----processing {} ----".format(file))
        if os.path.exists(os.path.join(img_path, file.split(".")[0]+".jpg")):
            sky_select(file, mask_path, img_path, no_sky_path, sky_path, bg_ratio, sky_ratio)
        else:
            logger.info("----{} has no relative original image----".format(file))
            continue


if __name__ == "__main__":
    main()
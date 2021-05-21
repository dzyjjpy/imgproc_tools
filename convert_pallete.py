# -*- coding: utf-8 -*-
# P.Y. Jia  2021.05.12
# python convert_pallete.py --mask_path masks/ --pallete_path pallete/

from PIL import Image
import numpy as np
import cv2
import os
from tqdm import tqdm
from enum import Enum
import argparse
import logging

logging.basicConfig(format=' %(asctime)s - %(message)s ', datefmt='%d-%b-%y %H:%M:%S', filename=None, level=logging.INFO)
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(description="Convert bianry mask/pallete mask")
    parser.add_argument('--mask_path', type=str, required=True, help="directory path: matting or binary mask")
    parser.add_argument('--pallete_path', type=str, required=True, help="result path: pallete mask)")
    args = parser.parse_args()
    print(args)
    return args

davis_palette = np.repeat(np.expand_dims(np.arange(0, 256), 1), 3, 1).astype(np.uint8)
davis_palette[:22, :] = [
                         [0, 0, 0], [128, 0, 0], [0, 128, 0], [128, 128, 0],
                         [0, 0, 128], [128, 0, 128], [0, 128, 128], [128, 128, 128],
                         [64, 0, 0], [191, 0, 0], [64, 128, 0], [191, 128, 0],
                         [64, 0, 128], [191, 0, 128], [64, 128, 128], [191, 128, 128],
                         [0, 64, 0], [128, 64, 0], [0, 191, 0], [128, 191, 0],
                         [0, 64, 128], [128, 64, 128]
                        ]

def imwrite_indexed(filename, array, color_palette):
    """ Save indexed png."""
    if np.atleast_3d(array).shape[2] != 1:
        raise Exception("Saving indexed PNGs requires 2D array.")

    im = Image.fromarray(array)
    im.putpalette(color_palette.ravel())
    im.save(filename, format='PNG')

def convert_pallete(mask_path, pallete_path):
    """
    :param mask_path:  matting mask(0~255) or binary mask(0, 255) path
    :param pallete_path:  pallete mask with P mode
    :return: None
    """
    logger.info('     mask matting path: {}      '.format(mask_path))
    files = os.listdir(mask_path)
    logger.info('     Start convert matting mask to binary mask     ')
    for file in tqdm(files):
        file_path = os.path.join(mask_path, file)
        assert os.path.exists(file_path), "file not exist, pls check"
        mask_binary = Image.open(file_path)
        #mask_matting = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        logger.info("mask_matting's shape{}".format(np.array(mask_binary).shape))
        n_channel = np.atleast_3d(np.array(mask_binary)).shape[2]
        mask_binary_8bit = None
        if 1 == n_channel:
            mask_binary_8bit = np.array(mask_binary)
        elif 3 == n_channel:
            mask_binary_8bit = np.array(mask_binary)[:, :, 0]
        elif 4 == n_channel:
            mask_binary_8bit = np.array(mask_binary)[:, :, 0]  # PAY Attention
        else:
            logger.debug("mask binary shape not equal to 1 or 3 or 4")

        res_file = os.path.join(pallete_path, file)
        if os.path.exists(pallete_path) == False:
            logger.info("res_path not exist! Create directory".format(pallete_path))
            os.mkdir(pallete_path)
        dst_pallete = mask_binary_8bit.copy()
        # elems = list(set(dst_pallete.flatten().tolist()))
        # assert len(elems) == 2 or len(elems) == 1, (f"mask format incorrect!")  # add background ONLY

        dst_pallete[mask_binary_8bit >= 127] = 1
        dst_pallete[mask_binary_8bit < 127] = 0
        imwrite_indexed(res_file, dst_pallete, davis_palette)

def convert_binary(pallete_path, binary_path):
    """
    :param pallete_path: pallete path with P mode
    :param binary_path: binary mask(ONLY 0 or 255)
    :return: None
    """
    logger.info('     pallete matting path: {}      '.format(pallete_path))
    files = os.listdir(pallete_path)
    logger.info('     Start convert pallete to binary mask     ')
    for file in tqdm(files):
        file_path = os.path.join(pallete_path, file)
        assert os.path.exists(file_path), "file not exist, pls check"
        pallete = Image.open(file_path)

        n_channel = np.atleast_3d(np.array(pallete)).shape[2]
        if 1 == n_channel:
            logger.info("pallete's shape{}".format(np.array(pallete).shape))
            pallete_array_8bit = np.array(pallete)
        elif 3 == n_channel:
            pallete_array_8bit = np.array(pallete)[:, :, 0] # R channel

        res_file = os.path.join(binary_path, file)
        if os.path.exists(binary_path) == False:
            logger.info("binary_path not exist! Create directory".format(binary_path))
            os.mkdir(binary_path)
        #print(set(pallete_array_8bit.flatten()))
        cv2.imwrite(res_file, (pallete_array_8bit/128)*255) #

def main():
    logger.info('     Start convert mask (binary/pallete)     ')
    args = get_args()
    mask_path = args.mask_path
    pallete_path = args.pallete_path

    # # convert matting mask or binary mask to pallete
    # convert_pallete(mask_path, pallete_path)
    # logger.warning("convert binary to pallete complete")

    # convert pallete to binary mask
    convert_binary(pallete_path, mask_path)
    logger.warning("convert pallete to binary complete")


if __name__ == "__main__":
    main()


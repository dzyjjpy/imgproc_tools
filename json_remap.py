"""
Get hands crop images from hand gesture detetection annotations
"""

import json
import os
import cv2
import shutil
import random
from tqdm import tqdm
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Convert matting mask to binary mask")
    parser.add_argument('--img_path', type=str, required=True, help="image path")
    parser.add_argument('--ann_path', type=str, required=True, help="annotation path")
    parser.add_argument('--res_path', type=str, required=True, help="result path")
    parser.add_argument('--mode', type=str, required=True, help="crop mode: original:no expand, expand:expand, reduce:inner")
    args = parser.parse_args()
    print(args)
    return args


def expand_random(img_ori, bbox_ori, expand_sigma):
    height, width, channels = img_ori.shape
    x0, y0, w, h = bbox_ori

    delta_x1 = abs(random.gauss(0, w*expand_sigma))
    delta_y1 = abs(random.gauss(0, h*expand_sigma))
    delta_x2 = abs(random.gauss(0, w*expand_sigma))
    delta_y2 = abs(random.gauss(0, h*expand_sigma))

    x1 = int(x0 - delta_x1)
    y1 = int(y0 - delta_y1)
    x2 = int((x0 + w) + delta_x2)
    y2 = int((y0 + h) + delta_y2)

    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 >= width:
        x2 = width - 1
    if y2 >= height:
        y2 = height - 1

    img_expand = img_ori[y1:y2, x1:x2]
    return img_expand

def reduce_random(img_ori, bbox_ori, expand_sigma):
    height, width, channels = img_ori.shape
    x0, y0, w, h = bbox_ori

    delta_x1 = abs(random.gauss(0, w*expand_sigma))
    delta_y1 = abs(random.gauss(0, h*expand_sigma))
    delta_x2 = abs(random.gauss(0, w*expand_sigma))
    delta_y2 = abs(random.gauss(0, h*expand_sigma))

    x1 = int(x0 + delta_x1)
    y1 = int(y0 + delta_y1)
    x2 = int((x0 + w) - delta_x2)
    y2 = int((y0 + h) - delta_y2)

    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 >= width:
        x2 = width - 1
    if y2 >= height:
        y2 = height - 1

    img_expand = img_ori[y1:y2, x1:x2]
    return img_expand

if __name__ == "__main__":
    args = get_args()
    img_path = args.img_path
    ann_path = args.ann_path
    res_path = args.res_path
    mode = args.mode
    if os.path.exists(res_path):
        pass
    else:
        os.mkdir(res_path)

    files = os.listdir(ann_path)
    for file in tqdm(files):
        ann_file_path = os.path.join(ann_path, file)
        with open(ann_file_path, "r") as load_file:
            load_dict = json.load(load_file)

            info_dict = load_dict["info"]
            images_dict = load_dict["images"]
            annotations_dict = load_dict["annotations"]
            categories_dict = load_dict["categories"]

            bbox_num = 0
            for anno in tqdm(annotations_dict):
                image_id = anno["image_id"]
                bbox_id = anno["category_id"]
                # if 1 == bbox_id:  ##ONLY work for hand gesture crop with head annotations
                #     continue
                # print("bbox id ", bbox_id)
                # if bbox_id > 1 :
                #     continue
                label = categories_dict[bbox_id - 1]["name"]  # 08.06 -2
                bbox = anno["bbox"]  # x1, y1, x2, y2
                x1, y1, w, h = bbox
                for image in images_dict:
                    if image_id == image["id"]:
                        image_name = image["file_name"]
                # image_name = images_dict["id" == image_id]["file_name"]
                image_file_path = os.path.join(img_path, image_name)

                img = cv2.imread(image_file_path)
                if img is None:
                    print(image_file_path)
                    continue
                if w*h < 1500:
                    continue

                assert mode in ["original", "expand", "reduce"], "pls check, mode must be original or expand"
                if mode == "original":
                    if x1 < 0:
                        x1 = 0
                    if y1 < 0:
                        y1 = 0
                    # print(x1, y1, w, h)
                    img_hand = img[int(y1):int(y1 + h), int(x1):int(x1 + w)]
                    # print(x1, y1, w, h)
                if mode == "expand":
                    img_hand = expand_random(img_ori=img, bbox_ori=bbox, expand_sigma=0.1)
                if mode == "reduce":
                    img_hand = reduce_random(img_ori=img, bbox_ori=bbox, expand_sigma=0.05)

                bbox_num = bbox_num + 1

                # label parsing
                res_file_path = os.path.join(res_path,
                                             image_name.split(".jpg")[0] + "_" + str(label) + "_" + str(
                                                 bbox_num) + ".jpg")
                cv2.imwrite(res_file_path, img_hand)

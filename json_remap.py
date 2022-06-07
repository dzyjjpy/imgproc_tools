"""
Get hands crop images from hand gesture detetection annotations
"""

import json
import os
import cv2
import shutil
from tqdm import tqdm
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Convert matting mask to binary mask")
    parser.add_argument('--img_path', type=str, required=True, help="image path")
    parser.add_argument('--ann_path', type=str, required=True, help="annotation path")
    parser.add_argument('--res_path', type=str, required=True, help="result path")
    # parser.add_argument('--xml_path', type=str, required=True, help="xml annotation path")
    args = parser.parse_args()
    print(args)
    return args


if __name__ == "__main__":
    args = get_args()
    img_path = args.img_path
    ann_path = args.ann_path
    res_path = args.res_path
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
                if 1 == bbox_id:
                    continue
                # print("bbox id ", bbox_id)
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
                img_hand = img[y1:y1 + h, x1:x1 + w]
                bbox_num = bbox_num + 1

                # label parsing
                res_file_path = os.path.join(res_path,
                                             image_name.split(".jpg")[0] + "_" + str(label) + "_" + str(
                                                 bbox_num) + ".jpg")
                cv2.imwrite(res_file_path, img_hand)

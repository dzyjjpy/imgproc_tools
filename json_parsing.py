"""
Function: convert kdxf's pig objects json annotations to Pascal VOC
python json_parsing.py --img_path mask_img/img_dir --ann_path mask_img/ann_dir --xml_path mask_img/xml

"""

import json
import os
import numpy as np
import shutil
from tqdm import tqdm
import cv2
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Convert matting mask to binary mask")
    parser.add_argument('--img_path', type=str, required=True, help="image path")
    parser.add_argument('--ann_path', type=str, required=True, help="json annotation path")
    parser.add_argument('--xml_path', type=str, required=True, help="xml annotation path")
    args = parser.parse_args()
    print(args)
    return args


def write_xml_header(xml_file, file, width, height):
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(file.split(".")[0]) + '.jpg' + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')


def write_xml_context(xml_file, labels, x1, y1, x2, y2):
    xml_file.write('    <object>\n')
    xml_file.write('        <name>' + str(labels) + '</name>\n')
    xml_file.write('        <pose>Unspecified</pose>\n')
    xml_file.write('        <truncated>0</truncated>\n')
    xml_file.write('        <difficult>0</difficult>\n')
    xml_file.write('        <bndbox>\n')
    xml_file.write('            <xmin>' + str(x1) + '</xmin>\n')
    xml_file.write('            <ymin>' + str(y1) + '</ymin>\n')
    xml_file.write('            <xmax>' + str(x2) + '</xmax>\n')
    xml_file.write('            <ymax>' + str(y2) + '</ymax>\n')
    xml_file.write('        </bndbox>\n')
    xml_file.write('    </object>\n')


def find_min_rect(points):
    assert points, "points is None, pls check"
    x1 = 10000
    y1 = 10000
    x2 = -1
    y2 = -1
    for point in points:
        x1 = min(x1, point[0])
        y1 = min(y1, point[1])
        x2 = max(x2, point[0])
        y2 = max(y2, point[1])
    box = x1, y1, x2, y2
    return box


# from .json(kdxf format) to .xml(Pascal VOC Format)
def convert_json_2_xml(img_path, ann_path, xml_path):
    assert os.path.exists(img_path) and os.path.exists(ann_path), "pls check img_path or ann_path exist or not"
    print("----img_path: ", img_path, ",     ----ann_path", ann_path)

    files = os.listdir(ann_path)
    for file in tqdm(files):
        ann_file_path = os.path.join(ann_path, file)
        img_file_path = os.path.join(img_path, file.split(".")[0] + ".jpg")
        # res_file_path = os.path.join(res_path, file.split(".")[0] + ".jpg")

        img = cv2.imread(img_file_path)
        height, width, channels = img.shape

        # write xml files
        xml_file = open((xml_path + '/' + file.split(".")[0] + '.xml'), 'w')
        write_xml_header(xml_file, file, width, height)

        with open(ann_file_path, "r") as load_file:
            load_dict = json.load(load_file)
            # img_name = load_dict["imagePath"]

            for i in range(len(load_dict["shape"])):
                labels = load_dict["shape"][i]["label"]
                boxes = load_dict["shape"][i]["boxes"]
                points = load_dict["shape"][i]["points"]  # all the value is None

                # processing segmentation format annotations to VOC xml format
                if boxes is None:
                    # shutil.copy(img_file_path, mask_path)
                    # shutil.copy(ann_file_path, mask_path)
                    box = None
                    box = find_min_rect(points)
                    x1, y1, x2, y2 = box
                    # cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=1)
                    # cv2.polylines(img, np.array([points]), 1, color=(255, 0, 0), thickness=2)
                    # cv2.fillPoly(img, np.array([points], np.int32), color=(255, 0, 0))
                    write_xml_context(xml_file, labels, x1, y1, x2, y2)
                # processing bboxes format annotations to VOC xml format
                else:
                    # shutil.copy(img_file_path, box_path)
                    # shutil.copy(ann_file_path, box_path)
                    # print(boxes)
                    x1, y1, x2, y2 = boxes
                    # cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=1)
                    write_xml_context(xml_file, labels, x1, y1, x2, y2)

            xml_file.write('</annotation>')
        cv2.imwrite("res_file_path.jpg", img)


if __name__ == "__main__":
    args = get_args()
    img_path = args.img_path
    ann_path = args.ann_path
    xml_path = args.xml_path

    if os.path.exists(xml_path):
        pass
    else:
        os.mkdir(xml_path)

    convert_json_2_xml(img_path, ann_path, xml_path)

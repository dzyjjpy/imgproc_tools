"""
Get hands crop images from head bbox annotation's expand
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
    parser.add_argument('--xml_path', type=str, required=True, help="xml path")
    args = parser.parse_args()
    print(args)
    return args


def expand_bbox(box, height, width, left, right, top, down):
    x0, y0, w, h = box
    x1 = x0 + w
    y1 = y0 + h
    x0 = x0 - w * left
    y0 = y0 - h * top
    x1 = x1 + w * right
    y1 = y1 + h * down
    if x0 < 0:
        x0 = 0
    if y0 < 0:
        y0 = 0
    if x1 > width:
        x1 = width
    if y1 > height:
        y1 = height
    return [int(x0), int(y0), int(x1), int(y1)]


def refine_bbox(bbox_expand, bbox_new):
    """
    :param bbox_expand: head expand bbox
    :param bbox_new: new hand bbox annotation
    :return: the refine bbox_new, solve the orders occasions
    """
    x0_expand, y0_expand, x1_expand, y1_expand = bbox_expand
    x0, y0, w, h = bbox_new
    x1 = x0 + w
    y1 = y0 + h
    if x0 < x0_expand:
        x0 = 0
    # if x1 < x0_expand:
    #     x1 = 0
    if y0 < y0_expand:
        y0 = 0
    # if y1 < y0_expand:
    #     y0 = 0
    if x1 > x1_expand:
        x1 = x1_expand
    if y1 > y1_expand:
        y1 = y1_expand
    return [x0 - x0_expand, y0 - y0_expand, x1 - x0_expand, y1 - y0_expand]


def is_outside(bbox_expand, bbox_new):
    """
    :param bbox_expand: head expand bbox
    :param bbox_new: new hand bbox annotation
    :return: bool status that bbox_new is outside bbox_expand or not
    """
    if bbox_expand and bbox_new:
        x0_expand, y0_expand, x1_expand, y1_expand = bbox_expand
        x0, y0, w, h = bbox_new
        x1 = x0 + w
        y1 = y0 + h
        is_outside = False
        if x1 < x0_expand or x0 > x1_expand:
            is_outside = True
        if  (y1 < y0_expand or y0 > y1_expand):
            is_outside = True
        # if (x0 >= x0_expand and x1 < x1_expand) and (y1 < y0_expand or y0 > y1_expand):
        #     is_outside = True
        return is_outside

def write_xml_header(xml_file, file_name, width, height):
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(file_name.split(".")[0]) + '.jpg' + '</filename>\n')
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

if __name__ == "__main__":
    args = get_args()
    img_path = args.img_path
    ann_path = args.ann_path
    res_path = args.res_path
    xml_path  = args.xml_path
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    if not os.path.exists(xml_path):
        os.mkdir(xml_path)


    files = os.listdir(ann_path)
    for file in files:
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
                    # print("bbox id ", bbox_id)
                    label = categories_dict[bbox_id - 1]["name"]  # 08.06 -2
                    bbox = anno["bbox"]  # x1, y1, x2, y2
                    for image in images_dict:
                        if image_id == image["id"]:
                            image_name = image["file_name"]
                    image_file_path = os.path.join(img_path, image_name)
                    if not os.path.exists(image_file_path):
                        print("--------img file path", image_file_path)
                    img = cv2.imread(image_file_path)
                    if img is None:
                        print("--------img file path", image_file_path)
                        continue
                    height, width, _ = img.shape
                    bbox_expand = expand_bbox(bbox, height, width, left=2, right=2, top=0.5, down=2)
                    x0, y0, x1, y1 = bbox_expand
                    # print("----head expand box: ", bbox_expand)
                    img_crop = img[y0:y1, x0:x1]


                    write_bbox = False
                    bbox_num = bbox_num + 1
                    file_name = image_name.split(".jpg")[0] + "_" + str("hand") + "_" + str(bbox_num) + ".jpg"
                    dst_xml_file = os.path.join(xml_path, file_name.split(".")[0] + ".xml")
                    xml_file = open(dst_xml_file, 'w')
                    write_xml_header(xml_file, file_name, x1-x0, y1-y0)

                    for anno_new in annotations_dict:
                        if anno_new["image_id"] == image_id:
                            bbox_id_new = anno_new["category_id"]
                            if bbox_id_new != 1:
                                # print(anno_new)
                                bbox_new = anno_new["bbox"]
                                # print("----bbox new: ", bbox_new)
                                if is_outside(bbox_expand, bbox_new):
                                    # ignore all the bbox outside bbox_expand
                                    pass
                                else:
                                    bbox_new_refine = refine_bbox(bbox_expand, bbox_new)
                                    x0_refine, y0_refine, x1_refine, y1_refine = bbox_new_refine

                                    ## show refine bbox in head expand crop image
                                    # cv2.rectangle(img_crop, (x0_refine, y0_refine), (x1_refine, y1_refine), color=(255, 0, 0), thickness=1)
                                    # cv2.imshow("img_crop.jpg", img_crop)
                                    # cv2.waitKey(3000)

                                    # label parsing
                                    res_file_path = os.path.join(res_path, file_name)
                                    cv2.imwrite(res_file_path, img_crop)
                                    write_xml_context(xml_file, "hand", x0_refine, y0_refine, x1_refine, y1_refine)
                                    write_bbox = True
                    xml_file.write("</annotation>")
                    xml_file.close()
                    if False == write_bbox:
                        os.remove(dst_xml_file)
                    #
                    # bbox_num = bbox_num + 1
                    # # label parsing
                    # res_file_path = os.path.join(res_path, image_name.split(".jpg")[0] + "_" + str("hand") + "_" + str(bbox_num) + ".jpg")
                    # cv2.imwrite(res_file_path, img_crop)

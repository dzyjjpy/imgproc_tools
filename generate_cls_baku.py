"""
Function: list all the files's name in one text file
e.g.:
@params: img_path: res_img/
@params: txt_path: test.txt
python list_file_names.py --img_path res_img/ --txt_path test.txt  --no_suffix
"""

import os
from tqdm import tqdm
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="write all the file's name to text file")
    parser.add_argument('--img_path', type=str, default="res_img/", required=True, help=" image directory path")
    parser.add_argument('--txt_path', type=str, default="test.txt", required=True, help="result path: save binary mask)")
    parser.add_argument('--no_suffix', action="store_true", help="image names with no suffix")
    args = parser.parse_args()
    print(args)
    return args

def add_cls_gt_label(file_name, train_txt):
    # class_names = ['_palm_', '_ok_', '_L_', '_V_', '_rock_', '_other_']
    class_names = ['_baby_', '_adult_', '_kids_', '_unknow_']
    for i, class_name in enumerate(class_names):
        if class_name in file_name:
            train_txt.write(" " + str(i))

def write_file_names(img_path, txt_path, no_suffix=False):
    """
    :param img_path: directory folder, e.g. res_img/
    :param txt_path: txt file path for saving file names, e.g. train_voc.txt
    :return: None
    """
    train_txt = open(txt_path, "w")
    files = os.listdir(img_path)

    for file in tqdm(files):
        if True == no_suffix:
            train_txt.write(file.split(".")[0])  # prefix name
        else:
            train_txt.write("3/"+file) # full name
        add_cls = True
        if add_cls == True:
            add_cls_gt_label(file, train_txt)
        # train_txt.write(" " + str(0))
        train_txt.write("\n")

def write_baku(root_path, txt_path):
    assert os.path.exists(root_path), "-----root_path not exist-----"

    train_txt = open(txt_path, "w")

    subdirs = os.listdir(root_path)
    for subdir in subdirs:
        subdir_path = os.path.join(root_path, subdir)
        if os.path.isdir(subdir_path):
            files = os.listdir(subdir_path)
            for file in files:
                file_path = os.path.join(subdir_path, file)
                train_txt.write(os.path.join(subdir, file))
                train_txt.write(" " + str(subdir))
                train_txt.write("\n")




if __name__ == "__main__":
    args = get_args()
    img_path = args.img_path
    txt_path = args.txt_path
    no_suffix_bool = args.no_suffix # remove file name's suffix or not

    # write_file_names(img_path, txt_path, no_suffix_bool)

    write_baku(img_path, txt_path)

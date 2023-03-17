
import os
import shutil
from tqdm import tqdm

# dir_root = "test"
# dir_root = "H:\cls_hand/train_0317/train_0317/train_0610_reduce_rename"
# suffix_str = "_20220610reduce" # "_20220608pexpand"

# dir_root = "images/right"
dir_root = r"H:\sky_seg\seg_sky_benchmark_1202\images"
# suffix_str = "other_20220617_collect_5817" # "_20220608pexpand"

mix_dir = r"H:\sky_seg\seg_sky_benchmark_1202\images_mix"
if not os.path.exists(mix_dir):
    os.makedirs(mix_dir)

dirs = os.listdir(dir_root)
# cls_names = ['palm', 'ok', 'L', 'V', 'rock', 'other']
cls_names = ["baby", "adult", "kids", "unknow"]
count = 0
for dir in dirs:
    dir_path = os.path.join(dir_root, dir)
    files = os.listdir(dir_path)
    for file in tqdm(files):
        if file.endswith(".jpg"):
            # file_new = file.split(".jpg")[0] + "_" + str(dir) + "_" + ".jpg"
            # file_new = "cls_gesture_20221109" + "_" + str(cls_names[int(dir)]) + "_" + str(count) + ".jpg"
            # file_new = "cls_baku_benchmark_1013_clean_20221116" + "_" + str(cls_names[int(dir)]) + "_" + str(count) + ".jpg"
            file_new = dir + "_" + file
            count = count + 1
            # file_new = file.split(".jpg")[0] + "_20220608pexpand.jpg"
            # file_new = file.split(".jpg")[0] + suffix_str + ".jpg"
            file_ori_path = os.path.join(dir_path, file)
            file_new_path = os.path.join(dir_path, file_new)
            os.rename(file_ori_path, file_new_path)


            # move all subdir to one mix_dir
            shutil.copyfile(os.path.join(dir_path, file_new), os.path.join(mix_dir, file_new))
            shutil.copyfile(file_new_path, os.path.join(mix_dir, file_new))

        if file.endswith(".mp4"):
            file_new = file.split(".jpg")[0] + "_" + str(dir) + "_" + ".mp4"
            file_ori_path = os.path.join(dir_path, file)
            file_new_path = os.path.join(dir_path, file_new)
            os.rename(file_ori_path, file_new_path)
            # shutil.copyfile(os.path.join(dir_path, file_new), os.path.join(mix_dir, file_new))
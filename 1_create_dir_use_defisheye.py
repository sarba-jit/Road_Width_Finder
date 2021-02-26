#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
##############COMMAND TO RUN THE PROGRAM#################
# python 1_create_dir_use_defisheye.py <OUTPUT_DIRECTORY> <IMAGE_PATH> <PATH_TO_MAPPING_DICTIONARY>
# python 1_create_dir_use_defisheye.py Image_Output Images_360/pano_0002_000040.jpg Mapping_Dictionary/combined_dict.pkl
#########################################################
"""

import os
import sys
import subprocess
from defisheye import Defisheye
import glob
import re
import cv2
from manual_width import ManualWidth

def output_dir(OUTPUT_FOLDER):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)


def generate_defisheye_image(OUTPUT_FOLDER, 
							IMAGE_FILE,
							dtype = 'stereographic',
							format = 'fullframe',
							fov = 180,
							pfov = 90):
	obj = Defisheye(IMAGE_FILE, dtype=dtype, format=format, fov=fov, pfov=pfov)
	image_path = IMAGE_FILE.split('/')[-1]
	final_path = os.path.join(OUTPUT_FOLDER,image_path)
	obj.convert(final_path)
	return final_path

if __name__== '__main__':
    output_dir(sys.argv[1])
    defisheyed_image_path = generate_defisheye_image(sys.argv[1],sys.argv[2])
    image = cv2.imread(defisheyed_image_path)
    width_finder = ManualWidth(image, sys.argv[3])
    width_finder.get_manual_width()
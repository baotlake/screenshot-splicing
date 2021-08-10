#! python3
import sys
import os
from PIL import Image
from core import find_max_subsequence, calc_entropy
from image import get_vertical_color

if len(sys.argv) <= 2:
    print('At least two pictures are required!')
    print(f'Usage: {sys.argv[0]} image1.png image2.png ...')
    sys.exit(0)

imageList = sys.argv[1:]
allExist = True

for path in imageList:
    if not os.path.exists(path):
        print(f'Path: "{path}" does not exist!')
        allExist = False

if not allExist:
    sys.exit(0)


i = 0
image_list = []
# Convert image into grayscale
# 剪裁头尾
header_height = 100
footer_height = 100
for path in imageList:
    i += 1
    img = Image.open(path)
    # 转换为灰度图片
    img = img.convert('L')
    # 剪裁头尾, header_height & footer_height
    img = img.crop((0, header_height, img.width, img.height - footer_height))
    img.save(f'./tmp/1-{i}.png')
    image_list.append(img)


# 选取x in x_list "列" 的像素进行对比
# x_list = [1 , 100, 500, 600, 800 ]
x_list = [110]
last_color_list = []
current_color_list = []

for x in x_list:
    last_color_list.append(get_vertical_color(image_list[0], x))

for j in range(1, len(image_list)):
    for x in x_list:
        current_color_list.append(get_vertical_color(image_list[j], x))

    same_sequence = []
    for a in range(0, len(last_color_list)):
        same_sequence.append(find_max_subsequence(last_color_list[a], current_color_list[a]))


    print(same_sequence)
    last_color_list = current_color_list


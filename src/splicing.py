#! python3
import sys
import os
from PIL import Image
from src.core import find_coincide
from src.image import get_vertical_color
import time

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
    else:
        print(f'{os.path.basename(path)}')

if not allExist:
    sys.exit(0)

i = 0
origin_image_list = []
image_list = []
# Convert image into grayscale
# 剪裁头尾
header_height = 400
footer_height = 400
for path in imageList:
    i += 1
    img = Image.open(path)
    origin_image_list.append(img)
    # 转换为灰度图片
    img = img.convert('L')
    # 剪裁头尾, header_height & footer_height
    img = img.crop((0, header_height, img.width, img.height - footer_height))
    img.save(f'./tmp/1-{i}.png')
    image_list.append(img)

# 选取x in x_list "列" 的像素进行对比
# x_list = [1 , 100, 500, 600, 800 ]
x_list = [10]

last_color_list = []
current_color_list = []

# 取 x = n 列的像素
x = 210
last_color_list = get_vertical_color(image_list[0], x)
last_color_list_index = 0

img1 = image_list[0]
img2 = image_list[1]

# header
origin_img1 = origin_image_list[0]
top = header_height

long_img = Image.new('RGB', (origin_img1.width, origin_img1.height * 15))
header = origin_img1.crop((0, 0, origin_img1.width, top))
long_img.paste(header, (0, 0, origin_img1.width, top))

long_img.save(f'./tmp/2-0.png')

# 第一张图
img1_content = origin_img1.crop((0, header_height, origin_img1.width, origin_img1.height - footer_height))
long_img.paste(img1_content, (0, top, img1_content.width, top + img1_content.height))
top += img1_content.height

long_img.save(f'./tmp/2-1.png')

for i in range(1, len(image_list)):
    print('i -> ', i, last_color_list_index)
    t1 = time.time()
    current_color_list = get_vertical_color(image_list[i], x)
    shift = find_coincide(last_color_list, current_color_list)
    origin_img = origin_image_list[i]
    offset = shift - origin_img.height
    top += shift
    t2 = time.time()
    print('i -> time ', t2 - t1, t2, t1)

    img_content = origin_img.crop((0, header_height, origin_img.width, origin_img.height - footer_height))
    long_img.paste(img_content, (0, top - img_content.height, img_content.width, top))

    last_color_list = current_color_list
    last_color_list_index = i

    long_img.save(f'./tmp/2-{i + 1}.png')

# footer
footer_img = origin_image_list[-1]
footer = footer_img.crop((0, footer_img.height - footer_height, footer_img.width, footer_img.height))
top += footer.height
long_img.paste(footer, (0, top - footer.height, footer.width, top))

long_img.save(f'./tmp/2-end.png')

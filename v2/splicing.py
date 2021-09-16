#! python
import os
import sys
import cv2
import numpy as np
from PIL import Image

from v2.core import sampling, translation_y, predict_translation_y

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} video.mp4')
    sys.exit(0)

config = {
    'header': 0.16,
    'footer': 0.14,
}

capture = cv2.VideoCapture(sys.argv[1])
success, array = capture.read()

if not success:
    print(f'Read video: "{sys.argv}" failed!')
    sys.exit(0)

size = (array.shape[1], array.shape[0])
crop_header = int(size[1] * config['header'])
crop_footer = int(size[1] * config['footer'])

long_image = array[0: crop_header, ]

# 接缝 一行红色像素
seam = np.broadcast_to(np.array([[[0, 0, 255]]], dtype='uint8'), shape=(1, array.shape[1], 3))
# print('seam shape ', seam.shape)

column = sampling(array[crop_header:-crop_footer, ])
array2 = None
column2 = None
offset_y = 0

frame_count = 1
while success:
    success, array2 = capture.read()
    if not success:
        break
    frame_count += 1

    # if frame_count % 3 != 0:
    #     continue

    column2 = sampling(array2[crop_header:-crop_footer, ])
    # print(column, column2)
    # 顺序计算重合度
    # offset_y, diff = translation_y(column, column2)
    # 计算重合度，由预测值逐渐向两边比较，性能优化
    offset_y, diff = predict_translation_y(column, column2, offset_y)
    print('frame', frame_count, '\toffset', offset_y, '\tdiff', diff)

    if offset_y < 0:
        pass
        long_image = np.vstack((long_image[: offset_y, ], seam))  # 显示接缝
        long_image = np.vstack((long_image[: offset_y, ], array[crop_header:crop_header + offset_y, ]))
    else:
        pass
        long_image = np.vstack((long_image, seam))  # 显示接缝
        long_image = np.vstack((long_image, array[crop_header:crop_header + offset_y, ]))

    array = array2
    column = column2

if offset_y < 0:
    long_image = np.vstack((long_image[: offset_y, ], seam))  # 显示接缝
    long_image = np.vstack((long_image[: offset_y, ], array[crop_header:, ]))
else:
    long_image = np.vstack((long_image, seam))  # 显示接缝
    long_image = np.vstack((long_image, array[crop_header:, ]))

print('❇️  frame:', frame_count)

# cv.VideoCapture().read() BGR
img = Image.fromarray(long_image[:, :, [2, 1, 0]], 'RGB')
root_path = os.path.abspath(os.path.join(__file__, '../../'))
img.save(f'{root_path}/tmp/v2_splicing.png')

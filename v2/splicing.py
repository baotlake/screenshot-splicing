#! python
import os
import sys
import cv2
import numpy as np
from PIL import Image

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} video.mp4')
    sys.exit(0)

config = {
    'header': 0.35,
    'footer': 0.2,
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


# 采样函数
def sampling(array, array2):
    return (
        np.dot(array[:, 213, :], [0.2989, 0.5870, 0.1140]),
        np.dot(array2[:, 213, :], [0.2989, 0.5870, 0.1140])
    )


# 计算最佳偏移值
def translation_y(column, column2):
    min_diff_y = (
        0,
        np.average(np.abs(column - column2))
    )
    for i in range(1, column.shape[0] - 90):
        diff_array = np.abs(column[i:] - column2[:-i])
        average_diff = np.average(diff_array)
        # print('diff ', average_diff)
        if average_diff < 1:
            # print('break ', i)
            return i
        if average_diff < min_diff_y[1]:
            min_diff_y = (i, average_diff)

    return min_diff_y[0]


array2 = np.array([], dtype='uint8')
frame_count = 1
while success:
    success, array2 = capture.read()
    frame_count += 1

    if not success:
        break
    column, column2 = sampling(
        array[crop_header:-crop_footer, ],
        array2[crop_header:-crop_footer, ]
    )
    # print(column, column2)

    offset_y = translation_y(column, column2)
    print('offset_y: ', offset_y)
    long_image = np.vstack((long_image, array[crop_header:crop_header + offset_y, ]))
    array = array2

# long_image = np.vstack((long_image, array2[: crop_header, ]))
print('❇️  frame:', frame_count)

# cv.VideoCapture().read() BGR
img = Image.fromarray(long_image[:, :, [2, 1, 0]], 'RGB')
root_path = os.path.abspath(os.path.join(__file__, '../../'))
img.save(f'{root_path}/tmp/v2_splicing.png')

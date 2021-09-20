#! python
import sys
import time

import ffmpeg
import numpy as np
from PIL import Image

from core import sampling_yuv, predict_translation_y, predict

config = {
    'header': 0.1,
    'footer': 0.09,
    'idea_offset': 0.35,
}

t_0 = time.time()

video_path = sys.argv[1]
probe = ffmpeg.probe(video_path)
video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
width = int(video_info['width'])
height = int(video_info['height'])
pixels = height * width * 3

t_1 = time.time()

out, err = (
    ffmpeg
        .input(video_path)
        .output('pipe:', format='rawvideo', pix_fmt='yuv444p')
        .run(capture_stdout=True)
)
video = np.frombuffer(out, np.uint8) \
    .reshape([-1, 3, height, width])

t_2 = time.time()

crop_header = int(height * config['header'])
crop_footer = int(height * config['footer'])
frame_count = 1
num_frames = video.shape[0]
array = video[0, ][0]
# print('array shape', array.shape)
array2 = None
column = sampling_yuv(array[crop_header:-crop_footer, ])
# print('column shape', column.shape)
column2 = None
offset_y = 0
predict_y = 0

drop_frames = 0
content_height = int(height * (1 - config['header'] - config['footer']))
idea_offset = content_height * config['idea_offset']
print('idea_offset ', idea_offset)

result_list = []
while frame_count < num_frames:
    array2 = video[frame_count, ][0]
    frame_count += 1

    column2 = sampling_yuv(array2[crop_header:-crop_footer, ])
    offset_y, diff = predict_translation_y(column, column2, predict_y)
    print('frame', frame_count, f'+{drop_frames}', '\tpredict', predict_y, '\toffset', offset_y, '\tdiff', diff)

    result_list.append((frame_count, offset_y, diff))
    array = array2
    column = column2
    # break
    drop_frames, predict_y = predict(result_list[-3:], idea_offset)
    frame_count += drop_frames

t_3 = time.time()
print('Calc Offset', t_3 - t_2)

seam = np.broadcast_to(np.array([[[255, 255, 255]]], dtype='uint8'), shape=(1, array.shape[1], 3))
long_image = np.array([], dtype='uint8').reshape([0, width, 3])
temp_image = np.dstack((video[0][0], video[0][1], video[0][2]))[0: -crop_footer, ]

for i in range(0, len(result_list)):
    frame, offset, diff = result_list[i]

    image = np.dstack((video[frame - 1][0], video[frame - 1][1], video[frame - 1][2]))[crop_header: -crop_footer]
    image = np.vstack((seam, image))  # 显示接缝
    temp_image = np.vstack((temp_image[: offset - image.shape[0], ], image))
    if temp_image.shape[0] > 10000:
        long_image = np.vstack((long_image, temp_image[0:5000, ]))
        temp_image = temp_image[5000:, ]

long_image = np.vstack((long_image, temp_image))

t_4 = time.time()
print('Stitching', t_4 - t_3)

footer = np.dstack((video[-1][0], video[-1][1], video[-1][2]))[-crop_footer:, ]
long_image = np.vstack((long_image, footer))
# print('long_image shape', long_image.shape)
MAX_HEIGHT = 60000
for i in range(0, (long_image.shape[0] // MAX_HEIGHT) + 1):
    part = long_image[i * MAX_HEIGHT: (i + 1) * MAX_HEIGHT, ]
    img = Image.fromarray(part, 'YCbCr')
    img.save(f'../tmp/v3_{i + 1}.jpg')

t_5 = time.time()
print('Save Image', t_5 - t_4)

print(f'\nprobe {t_1 - t_0} \t ffmpeg {t_2 - t_1}')
print(f'calc {t_3 - t_2} \t stitching {t_4 - t_3}')
print(f'save {t_5 - t_4} \t total {t_5 - t_1}')

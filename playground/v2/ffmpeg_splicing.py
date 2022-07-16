#! python
import os
import sys
import numpy as np
from PIL import Image
import ffmpeg
import time
from core import sampling, predict_translation_y

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} video.mp4')
    sys.exit(0)

config = {
    'header': 0.16,
    'footer': 0.14,
}

t_0 = time.time()
probe = ffmpeg.probe(sys.argv[1])
video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
width = int(video_info['width'])
height = int(video_info['height'])

t_1 = time.time()
out, err = (
    ffmpeg
        .input(sys.argv[1])
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run(capture_stdout=True)
)

video = (
    np.frombuffer(out, np.uint8)
        .reshape([-1, height, width, 3])
)

t_2 = time.time()

array = video[0, ]
crop_header = int(height * config['header'])
crop_footer = int(height * config['footer'])

long_image = array[0: crop_header, ]
# 接缝 一行红色像素
seam = np.broadcast_to(np.array([[[0, 0, 255]]], dtype='uint8'), shape=(1, array.shape[1], 3))

column = sampling(array[crop_header:-crop_footer, ])
array2 = None
column2 = None
offset_y = 0

frame_count = 1
num_frames = video.shape[0]

while frame_count < num_frames:
    array2 = video[frame_count, ]
    frame_count += 1

    column2 = sampling(array2[crop_header:-crop_footer, ])
    offset_y, diff = predict_translation_y(column, column2, offset_y)
    print('frame', frame_count, '\toffset', offset_y, '\tdiff', diff)

    if offset_y < 0:
        pass
        # long_image = np.vstack((long_image[: offset_y, ], seam))  # 显示接缝
        long_image = np.vstack((long_image[: offset_y, ], array[crop_header:crop_header + offset_y, ]))
    else:
        pass
        # long_image = np.vstack((long_image, seam))  # 显示接缝
        long_image = np.vstack((long_image, array[crop_header:crop_header + offset_y, ]))

    array = array2
    column = column2

if offset_y < 0:
    # long_image = np.vstack((long_image[: offset_y, ], seam))  # 显示接缝
    long_image = np.vstack((long_image[: offset_y, ], array[crop_header:, ]))
else:
    # long_image = np.vstack((long_image, seam))  # 显示接缝
    long_image = np.vstack((long_image, array[crop_header:, ]))

t_3 = time.time()

print('❇️  frame:', frame_count)
print(f'⏱ probe {t_1 - t_0} ffmpeg {t_2 - t_1}  other {t_3 - t_2} total {t_3 - t_1}')

img = Image.fromarray(long_image, 'RGB')
root_path = os.path.abspath(os.path.join(__file__, '../../'))
img.save(f'{root_path}/tmp/v2_ffmpeg_splicing.png')

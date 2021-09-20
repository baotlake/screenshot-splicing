import sys
import cv2
from PIL import Image

capture = cv2.VideoCapture(sys.argv[1])

frame_count = 1
success, image = capture.read()

while success:
    success, image = capture.read()
    frame_count += 1

    # 截帧调试
    if frame_count in [1840,1841,1832,1831,1721,1720,415,414]:
        img = Image.fromarray(image[:, :, [2, 1, 0]], 'RGB')
        img.save(f'../tmp/{frame_count}.png')

print('frame count', frame_count)

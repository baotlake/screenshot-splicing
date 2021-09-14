#! python3
import sys
import cv2
import imutils
import os
from PIL import Image

if len(sys.argv) <= 2:
    print('At least two pictures are required!')
    print(f'Usage: {sys.argv[0]} image1.png image2.png ...')
    sys.exit(0)

imagePaths = sys.argv[1:]
images = []
root_path = os.path.abspath(os.path.join(__file__, '../../'))

# loop over the image paths, load each one, and add them to our
# images to stitch list
cropPaths = []
i = 1
for imagePath in imagePaths:
    img = Image.open(imagePath)
    header_height = 400
    footer_height = 400
    img = img.crop((0, header_height, img.width, img.height - footer_height))
    tmp_path = f'{root_path}/tmp/crop-{i}.png'
    img.save(tmp_path)
    i += 1
    cropPaths.append(tmp_path)

print('----------')
for path in cropPaths:
    image = cv2.imread(path)
    image = imutils.rotate_bound(image, 90)
    images.append(image)


stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
status, pano = stitcher.stitch(images)

if status != cv2.Stitcher_OK:
    print('failed!')
    sys.exit(-1)
pano = imutils.rotate_bound(pano, 270)
cv2.imwrite(f'{root_path}/tmp/scans_output.png', pano)
print('done.')

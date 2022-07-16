import ffmpeg
import numpy as np
from PIL import Image
from os import path


def get_dimension(video_path: str):
    probe = ffmpeg.probe(video_path)
    stream = next(
        stream for stream in probe['streams'] if stream['codec_type'] == 'video')

    return (int(stream['width']), int(stream['height']))


def get_video(video_path: str, pix_fmt='yuv444p', quiet=False):
    buffer, err = ffmpeg.input(video_path).output(
        'pipe:', format='rawvideo', pix_fmt=pix_fmt
    ).run(capture_stdout=True, quiet=quiet)

    return buffer


def save_image(array: np.ndarray, file_path: str, max_height=65000, mode='YCbCr'):
    path_dir = path.dirname(file_path)
    filename = path.basename(file_path)

    if filename.endswith('.jpg'):
        filename = filename[:-4]

    # print(path_dir, filename)

    for i in range(0, array.shape[0] // max_height + 1):
        part = array[i * max_height: (i+1) * max_height]
        img = Image.fromarray(part, mode)
        img_name = filename + ('' if i < 1 else '_' + str(i)) + '.jpg'
        img_path = path.join(path_dir, img_name)
        img.save(img_path)

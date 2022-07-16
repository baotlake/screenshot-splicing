#! python3
import time
import click
import numpy as np
from os import path

from core import calc_overlaps, splice
from util import get_dimension, get_video, save_image


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.option('--crop-top', default=0.15, help='top crop height of the image, such as a fixed header',)
@click.option('--crop-bottom', default=0.15, help='bottom crop height of the image, such as a fixed footer')
@click.option('--expect-offset', default=0.3)
@click.option('-o', '--output', 'output', help='output path')
@click.option('-t', '--transpose', 'transpose', is_flag=True, help='for horizontal scrolling')
@click.option('--seam-width', 'seam_width', default=0, help='for debugging, show seams, set seam width')
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
def run(src, crop_top=0.15, crop_bottom=0.15, expect_offset=0.3, output=None, transpose=False, seam_width=0, verbose=False):
    w, h = get_dimension(src)
    if transpose:
        w, h = h, w

    def parse_abs(v: float) -> int: return int(v * h) if v < 1 else int(v)
    crop_top = parse_abs(crop_top)
    crop_bottom = parse_abs(crop_bottom)
    expect_offset = parse_abs(expect_offset)

    buffer = get_video(src, quiet=not verbose)
    shape = [-1, 3, h, w] if not transpose else [-1, 3, w, h]
    video = np.frombuffer(buffer, np.uint8).reshape(shape)
    if transpose:
        video = video.transpose(0, 1, 3, 2)

    results = calc_overlaps(video, crop_top, crop_bottom, expect_offset, None, verbose)
    panorama = splice(video, results, crop_top, crop_bottom, seam_width)
    if transpose:
        panorama = panorama.transpose(1, 0, 2)

    output = output or path.basename(src)

    save_image(panorama, output)


if __name__ == '__main__':
    run()

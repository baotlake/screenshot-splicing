#! python3
import time
import click
import numpy as np
from os import path

from core import calc_overlaps, splice
from util import get_dimension, get_video, save_image


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.option('--crop-top', default=0.15)
@click.option('--crop-bottom', default=0.15)
@click.option('--expect-offset', default=0.3)
@click.option('-o', '--output', 'output')
def run(src, crop_top=0.15, crop_bottom=0.15, expect_offset=0.3, output=None):
    w, h = get_dimension(src)

    def parse_abs(v: float) -> int: return int(v * h) if v < 1 else int(v)
    crop_top = parse_abs(crop_top)
    crop_bottom = parse_abs(crop_bottom)
    expect_offset = parse_abs(expect_offset)

    buffer = get_video(src)
    video = np.frombuffer(buffer, np.uint8).reshape([-1, 3, h, w])

    results = calc_overlaps(video, crop_top, crop_bottom, expect_offset)
    panorama = splice(video, results, crop_top, crop_bottom)

    output = output or path.basename(src)

    save_image(panorama, output)


if __name__ == '__main__':
    run()

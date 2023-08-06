from typing import Iterable, Optional

import numpy as np
import skimage.color
import skimage.io

from lomosplit.utils import consecutive, rotate, pad_vertical


def process_image(
        file: str,
        luminosity_percentile: int,
        rotate_image: Optional[str],
        rotate_frame: Optional[str],
        frame_min_height: Optional[int],
        frame_max_height: Optional[int],
        adjust_to_max_height: bool
) -> Iterable[np.ndarray]:
    image = skimage.io.imread(file)

    if rotate_image == 'auto':
        if image.shape[0] > image.shape[1]:
            rotate_image = 'left'
        else:
            rotate_image = None

    if rotate_frame == 'auto':
        rotate_frame = 'right'

    if rotate_image is not None:
        image = rotate(image, how=rotate_image)

    luminosity_hist = skimage.color.rgb2gray(image).mean(axis=0)
    threshold = np.percentile(luminosity_hist, luminosity_percentile)

    mask = luminosity_hist > threshold
    mask_where = np.where(mask)[0]
    parts = consecutive(mask_where)
    height_to_adjust = max(parts, key=len)

    if frame_max_height is not None:
        height_to_adjust = frame_max_height

    for part in parts:
        frame = image[:, part, :]

        if rotate_frame is not None:
            frame = rotate(frame, how=rotate_frame)

        if frame_min_height is not None and frame.shape[0] < frame_min_height:
            continue

        if frame_max_height is not None and frame.shape[0] > frame_max_height:
            continue

        if adjust_to_max_height:
            frame = pad_vertical(frame, height_to_adjust)

        yield frame


def process_batch(
        files: Iterable[str],
        *args,
        **kwargs
) -> Iterable[np.ndarray]:
    for file in files:
        yield from process_image(file, *args, **kwargs)

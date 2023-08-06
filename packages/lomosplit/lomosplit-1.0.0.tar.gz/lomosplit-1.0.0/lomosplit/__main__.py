import argparse
import os
import sys

import skimage.io

from lomosplit.image import process_batch
from lomosplit.utils import get_grouped_images


def main():
    parser = argparse.ArgumentParser(
        description='Utility for splitting LomoKino film scans'
    )

    parser.add_argument(
        'input',
        help='Input image or folder with images'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        dest='quiet',
        help='Do not print anything'
    )

    parser.add_argument(
        '-o', '--output',
        action='store',
        dest='output',
        default=None,
        help='Output folder to store results'
    )

    parser.add_argument(
        '--template',
        action='store',
        dest='template',
        default='frame_{idx:d}',
        help='Frame filename template without extension'
    )

    parser.add_argument(
        '--format',
        action='store',
        dest='format',
        default='jpg',
        help='Frame format (jpg, jpeg or png)'
    )

    parser.add_argument(
        '--luminosity-percentile',
        action='store',
        dest='luminosity_percentile',
        type=int,
        default=10,
        help='Luminosity percentile used to split frames'
    )

    parser.add_argument(
        '--rotate-image',
        action='store',
        dest='rotate_image',
        default='auto',
        help='Rotate image before processing (left, right or auto)'
    )

    parser.add_argument(
        '--rotate-frame',
        action='store',
        dest='rotate_frame',
        default='auto',
        help='Rotate frame before processing (left, right or auto)'
    )

    parser.add_argument(
        '--frame-min-height',
        action='store',
        dest='frame_min_height',
        type=int,
        default=100,
        help='Minimal frame height'
    )

    parser.add_argument(
        '--frame-max-height',
        action='store',
        dest='frame_max_height',
        type=int,
        default=None,
        help='Maximal frame height'
    )

    parser.add_argument(
        '--adjust-to-max-height',
        action='store_true',
        dest='adjust_to_max_height',
        help='Adjust each frame to maximum frame height (per image)'
    )

    args = parser.parse_args()

    input_path = os.path.normpath(os.path.abspath(args.input))

    if not os.path.exists(args.input):
        print(f'{input_path} does not exist')
        sys.exit(1)

    if os.path.isdir(input_path):
        grouped_images = get_grouped_images(input_path)

        if not grouped_images:
            print(f'{input_path} contains no images')
            sys.exit(1)
    else:
        grouped_images = [('', [os.path.basename(input_path)])]
        input_path = os.path.dirname(input_path)

    if args.output is not None:
        if os.path.exists(args.output):
            print(f'{args.output} already exists')
            sys.exit(2)

        output_path = os.path.normpath(os.path.abspath(args.output))
    else:
        for idx in range(100):
            output_path = os.path.abspath(os.path.join(os.getcwd(), f'lomosplit-output-{idx}'))

            if not os.path.exists(output_path):
                break
        else:
            print('Can not find appropriate name for output folder, please specify it')
            sys.exit(3)

    if args.format not in ('jpg', 'jpeg', 'png'):
        print('Frame format must be jpg, jpeg or png')
        sys.exit(3)

    template = f'{args.template}.{args.format}'

    for path, files in grouped_images:
        os.makedirs(os.path.join(output_path, path), exist_ok=True)

        for idx, frame in enumerate(process_batch(
                map(lambda x: os.path.join(input_path, path, x), files),
                luminosity_percentile=args.luminosity_percentile,
                rotate_image=args.rotate_image,
                rotate_frame=args.rotate_frame,
                frame_min_height=args.frame_min_height,
                frame_max_height=args.frame_max_height,
                adjust_to_max_height=args.adjust_to_max_height
        )):
            output_file = os.path.normpath(os.path.join(
                output_path,
                path,
                template.format(idx=idx)
            ))

            if not args.quiet:
                print(output_file)

            skimage.io.imsave(output_file, frame)


if __name__ == '__main__':
    main()

"""
This script provides functionality to overlay multiple images with optional downscaling.
It uses the Python Imaging Library (PIL) to manipulate images and combine them into a single output.
"""

import argparse
import sys
from PIL import Image

def overlay_two_images(base_image: Image.Image, overlay_image: Image.Image, downscale: float = 1.0) -> Image.Image:
    # Ensure both images are in RGBA mode to preserve alpha channel
    base_image = base_image.convert("RGBA")
    overlay_image = overlay_image.convert("RGBA")

    # Downscale the overlay image if necessary
    if 0 < downscale < 1:
        new_size = (int(overlay_image.width * downscale), int(overlay_image.height * downscale))
        overlay_image = overlay_image.resize(new_size, Image.LANCZOS)

    # Create a copy of the base image to overlay on
    combined_image = base_image.copy()

    # Calculate position to center the overlay image on the base image
    position = ((base_image.width - overlay_image.width) // 2, (base_image.height - overlay_image.height) // 2)

    # Paste the overlay image onto the combined image
    combined_image.paste(overlay_image, position, overlay_image)

    return combined_image


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='combine.py')
    parser.add_argument('-i', '--images', required=True, type=str, nargs="+", help="Path to the images to combine, should be more than one")
    parser.add_argument('-d', '--downscale', required=False, type=float, nargs="*", help="Downscaling factor (1, .5, etc). If used it must match the number of images - 1")
    parser.add_argument('-o', '--output_file', required=True, type=str, help="Path to file where final combined images is stored")

    args = parser.parse_args()

    # make sure inputs match
    downscaling = []
    if(args.downscale):
        # if they don't match, exit
        if(len(args.downscale) != len(args.images) - 1):
            print(f"Number of image pairs ({len(args.images)}) does not equal downscale parameters ({len(args.downscale)})")
            sys.exit(2)
        else:
            downscaling = args.downscale
    else:
        # set to 1 for all
        downscaling = [1.0 for i in args.images]

    # combine the first two images
    combined_image = overlay_two_images(Image.open(args.images[0]).convert("RGBA"),
                                        Image.open(args.images[1]).convert("RGBA"),
                                        downscale=downscaling[0])

    if(len(args.images) > 2):
        for i in range(2, len(args.images)):
            combined_image = overlay_two_images(combined_image,
                                                Image.open(args.images[i]),
                                                downscale=downscaling[i - 1])

    # save the output
    print(f"Saving file to {args.output_file}")
    combined_image.save(args.output_file)

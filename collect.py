"""
This script searches for PNG images within a specified directory and its subdirectories.
It copies images that match target sizes to a designated destination folder, ensuring no
filename conflicts by generating unique filenames when necessary.
"""

import argparse
import os
from PIL import Image
import shutil
from typing import Tuple, List

# Define the target size and file extension
FILE_EXTENSION: str = '.png'

def get_unique_filename(destination_folder: str, filename: str) -> str:
    """
    Generate a unique filename by appending a counter if the filename already exists.

    :param destination_folder: The folder where the file will be copied.
    :param filename: The original filename.
    :return: A unique filename that does not exist in the destination folder.
    """
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(destination_folder, new_filename)):
        new_filename = f"{base}({counter}){extension}"
        counter += 1
    return new_filename


def find_and_copy_images(root_folder: str, destination_root_folder: str, target_size: Tuple[int, int]) -> None:
    """
    Search for images of a specific size and copy them to the destination folder.

    :param root_folder: The root directory to start searching for images.
    :param destination_root_folder: The destination root folder to download images to
    :param target_size: A tuple representing the target size (width, height).
    """
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(FILE_EXTENSION):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        if img.size == target_size:
                            folder = f"{target_size[0]}x{target_size[1]}"
                            destination_size_folder = os.path.join(destination_root_folder, folder)
                            unique_filename = get_unique_filename(destination_size_folder, file)
                            destination_path = os.path.join(destination_size_folder, unique_filename)

                            # Create the target size folder if it doesn't exist
                            if not os.path.exists(os.path.dirname(destination_path)):
                                os.makedirs(os.path.dirname(destination_path))

                            shutil.copy(file_path, destination_path)
                            print(f"Copied: {file_path} to {destination_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='collect.py')
    parser.add_argument('-p', '--icon_path', required=True, type=str, help=r"Path to Factorio icons, if using Steam this is Steam/steamapps/common/Factorio/data")
    parser.add_argument('-d', '--destination_folder', default="icons", type=str, help="Folder where icons will be copied to")

    args = parser.parse_args()

    # Create the destination folder if it doesn't exist
    if not os.path.exists(args.destination_folder):
        os.makedirs(args.destination_folder)

    # Start the search from the specified directory with target sizes
    target_sizes: List[Tuple[int, int]] = [(120, 64), (128, 64), (192, 128), (480, 256)]
    for target_size in target_sizes:
        find_and_copy_images(args.icon_path.replace("\\", "/"), args.destination_folder, target_size)

    print("Search and copy completed.")

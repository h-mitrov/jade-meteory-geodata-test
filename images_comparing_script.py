import os
from typing import Tuple

import numpy as np
import pandas as pd
from PIL import Image

OUTPUT_FILE_NAME = 'output.csv'
LATITUDE_LABEL = 'lat'
LONGTITUDE_LABEL = 'lon'
VALUE_LABEL = 'value'


def get_coordinates_of_given_elem_for_array(image_path: str, elem_to_find: int) -> np.ndarray:
    """
    Converts an image into a np.ndarray, returns coordinates
    of all pixels, containing needed value.
    """
    image_as_array = np.array(Image.open(image_path))
    return np.argwhere(image_as_array == elem_to_find)


def get_differences_of_two_arrays(array_1: np.ndarray, array_2: np.ndarray) -> Tuple[set, set]:
    """
    Returns set of tuples, containing coordinates of points,
    that are present in array_1, but not present in array_2.
    """
    set_1 = set((tuple(elem) for elem in array_1.tolist()))
    set_2 = set((tuple(elem) for elem in array_2.tolist()))

    disappeared_points = set_1.difference(set_2)
    new_points = set_2.difference(set_1)

    return disappeared_points, new_points


def write_results_to_csv(points: set, value: str, append_to_existing: bool) -> None:
    """
    Saves the results to a new csv file or appends to an existing one.
    """
    dataframe = pd.DataFrame(points, columns=[LATITUDE_LABEL, LONGTITUDE_LABEL])
    dataframe[VALUE_LABEL] = value

    if not append_to_existing:
        dataframe.to_csv(OUTPUT_FILE_NAME, index=False)
    elif os.path.exists(OUTPUT_FILE_NAME):
        dataframe.to_csv(OUTPUT_FILE_NAME, mode='a', index=False, header=False)
    else:
        raise FileNotFoundError('Something went wrong. No csv file found to append to.')


def compare_two_images(first_image_path: str, second_image_path: str, elem_to_find: int) -> None:
    """
    Main function. Compares two images, locates the coordinates
    of pixels with needed value, writes the result to csv.
    """
    try:
        old_coordinates = get_coordinates_of_given_elem_for_array(image_path=first_image_path,
                                                                  elem_to_find=elem_to_find)

        new_coordinates = get_coordinates_of_given_elem_for_array(image_path=second_image_path,
                                                                  elem_to_find=elem_to_find)

        disappeared_points, new_points = get_differences_of_two_arrays(array_1=old_coordinates, array_2=new_coordinates)

        write_results_to_csv(points=disappeared_points, value='-1', append_to_existing=False)
        write_results_to_csv(points=new_points, value='+1', append_to_existing=True)

        print('Success! Output file written to the same folder.')
    except Exception as exc:
        print(f'An exception occured. Details: {exc}')


if __name__ == '__main__':
    compare_two_images(first_image_path='2016-01-01_city_label.tiff',
                       second_image_path='2021-01-01_city_label.tiff',
                       elem_to_find=104)

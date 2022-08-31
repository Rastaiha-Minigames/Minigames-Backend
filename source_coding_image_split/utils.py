import base64

import cv2

from source_coding_image_split.constants import HALF_MATRIX, IMAGE, ZERO_MATRIX


def convert_cv2_image_to_base64_URI(image):
    _, buffer = cv2.imencode(".jpg", image)
    string = base64.b64encode(buffer).decode()
    return f"data:image/jpg;base64,{string}"


def remove_n_least_significant_bits_from_pixels(image, bits):
    bits = int(bits)
    return image & (((2**bits)-1) << (8-bits))


def downsample_image(image, scale_factor):
    original_dimensions = (image.shape[1], image.shape[0])
    scaled_dimensions = (
        int(image.shape[1]*scale_factor), int(image.shape[0]*scale_factor))
    resized_image = cv2.resize(
        image, scaled_dimensions, interpolation=cv2.INTER_LANCZOS4)
    image = cv2.resize(resized_image, original_dimensions)
    return image


def change_intensity(image, coefficient):
    return (image*coefficient).astype(image.dtype)


def merge_YCbCr(Y, Cb, Cr):
    merge = cv2.cvtColor(cv2.merge([Y, Cr, Cb]), cv2.COLOR_YCrCb2BGR)
    Y = cv2.cvtColor(cv2.merge(
        [Y, HALF_MATRIX, HALF_MATRIX]),
        cv2.COLOR_YCrCb2BGR)
    Cr = cv2.cvtColor(cv2.merge(
        [HALF_MATRIX, Cr, HALF_MATRIX]),
        cv2.COLOR_YCrCb2BGR)
    Cb = cv2.cvtColor(cv2.merge(
        [HALF_MATRIX, HALF_MATRIX, Cb]),
        cv2.COLOR_YCrCb2BGR)
    return {
        'Y': convert_cv2_image_to_base64_URI(Y),
        'Cb': convert_cv2_image_to_base64_URI(Cb),
        'Cr': convert_cv2_image_to_base64_URI(Cr),
        'Merge': convert_cv2_image_to_base64_URI(merge),
    }


def merge_RGB(R, G, B):
    merge = cv2.merge([B, G, R])
    B = cv2.merge([B, ZERO_MATRIX, ZERO_MATRIX])
    G = cv2.merge([ZERO_MATRIX, G, ZERO_MATRIX])
    R = cv2.merge([ZERO_MATRIX, ZERO_MATRIX, R])
    return {
        'B': convert_cv2_image_to_base64_URI(B),
        'G': convert_cv2_image_to_base64_URI(G),
        'R': convert_cv2_image_to_base64_URI(R),
        'Merge': convert_cv2_image_to_base64_URI(merge),
    }

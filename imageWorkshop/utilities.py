# import re
# import cv2
# import base64
# import numpy as np
# FRACTION_REGEX = re.compile(r'^([-+]?\d+)\/?(\d*)$')
#
#
# def convertToFloat(fractionString):
#     try:
#         return float(fractionString)
#     except ValueError:
#         if FRACTION_REGEX.match(fractionString):
#             numerator, denomerator = FRACTION_REGEX.match(
#                 fractionString).groups()
#             if denomerator is None:
#                 return int(numerator)
#             return int(numerator)/int(denomerator)
#         return 0
#
#
# def dataURItoCV2Image(data):
#     nparray = np.fromstring(data.decode('base64'), np.uint8)
#     image = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
#     return image
#
#
# def CV2ImageToDataURI(image):
#     _, encoded_img = cv2.imencode('.jpg', image)
#     data = base64.b64encode(encoded_img).decode("utf-8")
#     return data

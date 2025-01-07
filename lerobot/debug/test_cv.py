import cv2
import sys


import logging
import time
import traceback
from contextlib import nullcontext
from copy import copy
from functools import cache

import cv2
import torch
import tqdm
from deepdiff import DeepDiff
from termcolor import colored

from lerobot.common.datasets.image_writer import safe_stop_image_writer




print("cv2 path:", cv2.__file__)
print("cv2 version:", cv2.__version__)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    cv2.imshow("test", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()

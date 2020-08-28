# Written by Vincent Xue
# Copyright (c) 2020 Vincent Xue

from functools import wraps
import cv2
import numpy as np

# MACRO
PATH_MODELS = './weights'
MODEL_VERSION = '/naiveNN_v1'

C_NUM = 6  # total number of classes
GESTURE_CLASSES = ('left', 'right', 'back', 'enter', 'idle', 'nothing')

FONT = cv2.FONT_HERSHEY_SIMPLEX
SIZE = 0.5
FX = 10
FY = 350
FH = 18


def log_decorator(func):
    @wraps(func)
    def log(*args, **kwargs):
        try:
            print(">>> Executing:", func.__name__)
            return func(*args, **kwargs)
        except Exception as e:
            print(">>> Error: %s" % e)

    return log

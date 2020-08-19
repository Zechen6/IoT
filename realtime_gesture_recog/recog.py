import cv2
import torch
import numpy as np

import global_vars
import models
from filters import skinMask,greyMask
from models import load_model, predict_gesture
from utils import *


class recognizer:
    def __init__(self):
        # CNN
        self.model = load_model()
        if torch.cuda.is_available():
            self.gpu = True
            self.model.cuda()
        self.prediction_frequency = 10  # each 10 images arise a prediction
        self.prediction_count = 0
        self.camera_height = 300
        self.camera_width = 300

    def get_hand_img(self, raw_img, x, y,fix=True):
        '''
        cut the part of img having hand.
        raw_img: ndarray, (255,255,3)
        x,y: right wrist coordinate
        '''
        if not fix:
            if x - self.camera_width // 2 < 0:
                x0 = 0
            elif x + self.camera_width // 2 > raw_img.shape[1]:
                x0 = raw_img.shape[1] - self.camera_width
            else:
                x0 = x - self.camera_width

            if y - self.camera_height*2  < 0:
                y0 = 0
            # elif y + self.camera_height  > raw_img.shape[0]:
                # y0 = raw_img.shape[0] - self.camera_height
            else:
                y0 = x - self.camera_height*2
        else:
            x0, y0 = 350,300

        # img = greyMask(raw_img, x0, y0, self.camera_width, self.camera_height)
        img = skinMask(raw_img, x0, y0, self.camera_width, self.camera_height)

        return img

    def recognize(self, img):
        gesture = predict_gesture(self.model, img,
                                  self.gpu, verbose=True)
        return gesture

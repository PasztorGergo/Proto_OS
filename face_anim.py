#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
import time, math, random, threading, os, sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import RPi.GPIO as GPIO
#from pilmoji import Pilmoji

class IEmotion:
  eyearray = []
  moutharray = []
  name = None

  def __init__(self, eye, mouth, name):
    self.eyearray = eye
    self.moutharray = mouth
    self.name = name
  
  def getName(self):
    return self.name

#vars
matrix = None

#emotions
happy = IEmotion([
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc1, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x03, 0x01, 0x80, 0x00, 0x00, 0x00, 0x18, 0x00, 0x0c, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x08, 0x00, 0x30, 0x00, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0xc0, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x03, 0xff, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],                
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x1e, 0x80, 0x00, 0x00, 0x00, 0x18, 0x00, 0x01, 0xf0, 0x80, 0x00, 0x00, 0x00, 0x08, 0x00, 0x0f, 0x00, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x78, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x01, 0xc0, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x03, 0xff, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],  #  3
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x1f, 0xc0, 0x00, 0x00, 0x00, 0x08, 0x00, 0x01, 0xf0, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x03, 0xff, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],  #  4
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x03, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],  #  5
    ], [
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3c, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xfe, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x7f, 0xf0, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00, 0x03, 0xff, 0x80, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x1f, 0xff, 0x80, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xfc, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3c, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xf0, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0xff, 0xff, 0x80, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x7f, 0xfe, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00, 0x03, 0xff, 0xe0, 0x00, 0x3f, 0x00, 0x00, 0x00, 0x01, 0xff, 0xff, 0xfc, 0x7e, 0x00, 0x00, 0x00, 0x00, 0x07, 0xff, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7f, 0xff, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xc0, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x3c, 0xe0, 0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x38, 0x60, 0x00, 0x00, 0x00, 0x7f, 0x00, 0x00, 0x70, 0x70, 0x00, 0x00, 0x01, 0xff, 0x00, 0x00, 0xff, 0xff, 0xc0, 0x00, 0x0f, 0xff, 0x00, 0x00, 0xff, 0xff, 0xff, 0x01, 0xff, 0xff, 0x00, 0x00, 0x00, 0x7f, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x07, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x03, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xff, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    ], "happy")
default = IEmotion([
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x01, 0xe0, 0x00, 0x00, 0x00, 0x70, 0x00, 0x38, 0x00, 0x20, 0x00, 0x00, 0x00, 0x18, 0x00, 0x0e, 0x00, 0x60, 0x00, 0x00, 0x00, 0x08, 0x00, 0x03, 0x80, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0xe0, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x1c, 0x03, 0xc0, 0x00, 0x00, 0x00, 0x18, 0x00, 0x07, 0x80, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0xe0, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x38, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x17, 0x80, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x18, 0x7c, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x07, 0x07, 0xc0, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0xe0, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x38, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x1f, 0x80, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ]
    ],[
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x0f, 0x80, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x0d, 0xe0, 0x70, 0x00, 0x00, 0x3c, 0x00, 0x00, 0x0c, 0xf1, 0xf8, 0x00, 0x00, 0x78, 0x00, 0x00, 0x1c, 0x3f, 0xde, 0x00, 0x01, 0xe0, 0x00, 0x00, 0x18, 0x1f, 0x0f, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x18, 0xfc, 0x03, 0xc0, 0x07, 0x00, 0x00, 0x00, 0x3b, 0xf0, 0x01, 0xf0, 0x1e, 0x00, 0x00, 0x00, 0x3f, 0x80, 0x00, 0x7c, 0x3c, 0x00, 0x00, 0x00, 0x3e, 0x00, 0x00, 0x1f, 0xf0, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x07, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x0f, 0x80, 0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x0d, 0xe0, 0xf8, 0x00, 0x00, 0x7e, 0x00, 0x00, 0x0c, 0xff, 0xfc, 0x00, 0x00, 0x7c, 0x00, 0x00, 0x1c, 0x3f, 0xff, 0x00, 0x01, 0xf8, 0x00, 0x00, 0x18, 0x1f, 0xff, 0x80, 0x07, 0xf0, 0x00, 0x00, 0x18, 0xfc, 0x0f, 0xe0, 0x0f, 0xe0, 0x00, 0x00, 0x3b, 0xf0, 0x03, 0xf8, 0x3f, 0xc0, 0x00, 0x00, 0x3f, 0x80, 0x01, 0xfe, 0xfe, 0x00, 0x00, 0x00, 0x3e, 0x00, 0x00, 0x7f, 0xfc, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x1f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0xff, 0x00, 0x00, 0x0f, 0x00, 0x07, 0x00, 0x7f, 0xff, 0x00, 0x00, 0x0f, 0xc0, 0x3f, 0xc1, 0xff, 0xff, 0x00, 0x00, 0x0d, 0xff, 0xff, 0xe7, 0xff, 0xff, 0x00, 0x00, 0x0c, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x1c, 0x3f, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x18, 0x1f, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x18, 0xfc, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x3b, 0xf0, 0x3f, 0xff, 0xff, 0xfc, 0x00, 0x00, 0x3f, 0x80, 0x1f, 0xff, 0xff, 0xf0, 0x00, 0x00, 0x3e, 0x00, 0x07, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x30, 0x00, 0x00, 0xff, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    ], "default")
tired = IEmotion([
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x01, 0xe0, 0x00, 0x00, 0x00, 0x70, 0x00, 0x38, 0x00, 0x20, 0x00, 0x00, 0x00, 0x18, 0x00, 0x8e, 0x00, 0x60, 0x00, 0x00, 0x00, 0x08, 0x00, 0x43, 0x80, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x30, 0xe0, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8e, 0x38, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x61, 0x8f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0xc0, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x38, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x1c, 0x03, 0xc0, 0x00, 0x00, 0x00, 0x18, 0x00, 0x87, 0x80, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x40, 0xe0, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x30, 0x38, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8e, 0x0f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x61, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0xc0, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x38, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x17, 0x80, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x18, 0x7c, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x87, 0x07, 0xc0, 0x00, 0x00, 0x00, 0x08, 0x00, 0x40, 0xe0, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x30, 0x38, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8e, 0x0f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x61, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0xc0, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x38, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x80, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x40, 0x1f, 0x80, 0x00, 0x00, 0x00, 0x08, 0x00, 0x30, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x61, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0xc0, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x38, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ]
    ],[
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x23, 0xc0, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x60, 0x78, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x00, 0x40, 0x0f, 0x80, 0x00, 0x00, 0x30, 0x00, 0x00, 0xc0, 0xf8, 0x78, 0x00, 0x00, 0x60, 0x00, 0x00, 0x87, 0x00, 0x0f, 0x80, 0x01, 0xc0, 0x00, 0x01, 0x3c, 0x00, 0x00, 0xf8, 0x03, 0x00, 0x00, 0x01, 0xe0, 0x00, 0x00, 0x0f, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
      [],
    ], "tired")
eyes_closed = IEmotion([
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
    ],
    [
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x1b, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x06, 0x00, 0x11, 0x80, 0x07, 0x00, 0x1e, 0x00, 0x0c, 0x00, 0x10, 0xc0, 0x0d, 0x80, 0x33, 0x80, 0x18, 0x00, 0x10, 0x60, 0x18, 0xc0, 0x20, 0xe0, 0x30, 0x00, 0x10, 0x30, 0x30, 0x60, 0x60, 0x30, 0x60, 0x00, 0x10, 0x0c, 0x60, 0x38, 0xc0, 0x1c, 0xc0, 0x00, 0x11, 0xff, 0xc0, 0x0d, 0x80, 0x07, 0x80, 0x00, 0x1f, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
      [],
      []
    ], "eyes_closed")
angry = IEmotion([
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xc0, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xe8, 0x00, 0x00, 0x00, 0x70, 0x00, 0xfc, 0x00, 0x18, 0x00, 0x00, 0x00, 0x18, 0x00, 0xc7, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x60, 0x0f, 0xc0, 0x00, 0x00, 0x00, 0x08, 0x00, 0x18, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x80, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xc0, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xe8, 0x00, 0x00, 0x00, 0x70, 0x00, 0xff, 0x00, 0x18, 0x00, 0x00, 0x00, 0x18, 0x00, 0xc1, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x70, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x1c, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xc0, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xc0, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xe8, 0x00, 0x00, 0x00, 0x70, 0x00, 0xf8, 0x00, 0x18, 0x00, 0x00, 0x00, 0x18, 0x00, 0x3f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x07, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
    ],[
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0xc0, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x60, 0x02, 0x00, 0x00, 0x00, 0x00, 0x03, 0x80, 0x38, 0x06, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x00, 0x0c, 0x04, 0x00, 0x00, 0x00, 0x01, 0xf0, 0x00, 0x06, 0x0c, 0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x03, 0x08, 0x00, 0x00, 0x00, 0xe4, 0x00, 0x00, 0x01, 0x90, 0x00, 0x00, 0x0f, 0x88, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x0c, 0x18, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x03, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00],
      [],
      []
    ], "angry")
furious = IEmotion([
      [0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x10, 0x00, 0x60, 0x00, 0x00, 0x01, 0xff, 0xc3, 0xd0, 0x03, 0x30, 0xc0, 0x00, 0x01, 0x80, 0x70, 0x70, 0x01, 0x9b, 0x80, 0x00, 0x00, 0xc0, 0x0e, 0x00, 0x00, 0xce, 0x30, 0x70, 0x00, 0x40, 0x03, 0xc0, 0x00, 0x20, 0x60, 0x18, 0x00, 0x30, 0x00, 0x60, 0x00, 0x21, 0xc0, 0x08, 0x00, 0x0e, 0x00, 0x60, 0x01, 0xc3, 0x00, 0x08, 0x00, 0x03, 0x80, 0xc0, 0x06, 0x01, 0x80, 0x00, 0x00, 0x00, 0x7b, 0x00, 0x00, 0x78, 0xc0, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x01, 0xcc, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x10, 0x00, 0x60, 0x00, 0x00, 0x01, 0xf8, 0x03, 0xd0, 0x03, 0x30, 0xc0, 0x00, 0x01, 0x8f, 0x80, 0x70, 0x01, 0x9b, 0x80, 0x00, 0x00, 0xc0, 0xe0, 0x00, 0x00, 0xce, 0x30, 0x70, 0x00, 0x70, 0x3c, 0x00, 0x00, 0x20, 0x60, 0x18, 0x00, 0x18, 0x07, 0x00, 0x00, 0x21, 0xc0, 0x08, 0x00, 0x0e, 0x01, 0x80, 0x01, 0xc3, 0x00, 0x08, 0x00, 0x03, 0x80, 0xc0, 0x06, 0x01, 0x80, 0x00, 0x00, 0x00, 0xf0, 0xc0, 0x00, 0x78, 0xc0, 0x00, 0x00, 0x00, 0x1f, 0x80, 0x01, 0xcc, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x10, 0x00, 0x60, 0x00, 0x00, 0x01, 0xe0, 0x03, 0xd0, 0x03, 0x30, 0xc0, 0x00, 0x00, 0x7e, 0x00, 0x70, 0x01, 0x9b, 0x80, 0x00, 0x00, 0x3f, 0x80, 0x00, 0x00, 0xce, 0x30, 0x70, 0x00, 0x03, 0xe0, 0x00, 0x00, 0x20, 0x60, 0x18, 0x00, 0x00, 0xf8, 0x00, 0x00, 0x21, 0xc0, 0x08, 0x00, 0x00, 0x3c, 0x00, 0x01, 0xc3, 0x00, 0x08, 0x00, 0x00, 0x0e, 0x00, 0x06, 0x01, 0x80, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x78, 0xc0, 0x00, 0x00, 0x00, 0x01, 0x80, 0x01, 0xcc, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
    ],[
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x07, 0xc0, 0x00, 0x00, 0x01, 0x80, 0x02, 0x00, 0x04, 0x7f, 0x00, 0x00, 0x03, 0xc0, 0x06, 0x00, 0x06, 0x03, 0xe0, 0x00, 0x06, 0x60, 0x04, 0x00, 0x02, 0x02, 0x30, 0x00, 0x08, 0x30, 0x08, 0x00, 0x02, 0x06, 0x1c, 0x00, 0x30, 0x10, 0x18, 0x00, 0x03, 0x0c, 0x06, 0x00, 0x60, 0x18, 0x30, 0x00, 0x01, 0x18, 0x03, 0x80, 0xc0, 0x0c, 0x20, 0x00, 0x01, 0x10, 0x00, 0x41, 0x80, 0x02, 0x60, 0x00, 0x00, 0xa0, 0x00, 0x33, 0x00, 0x03, 0x40, 0x00, 0x00, 0x40, 0x00, 0x1e, 0x00, 0x01, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
      [],
      []
    ], "furious")
confused = IEmotion([
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x01, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0xf8, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x8c, 0x20, 0x00, 0x00, 0x00, 0x70, 0x00, 0x1b, 0x06, 0x30, 0x00, 0x00, 0x00, 0x18, 0x00, 0x12, 0x63, 0x10, 0x00, 0x00, 0x00, 0x08, 0x00, 0x12, 0xf1, 0x10, 0x00, 0x00, 0x00, 0x08, 0x00, 0x12, 0xf1, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0b, 0xe1, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x03, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x06, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x3c, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x13, 0xe0, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x02, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0xe3, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x80, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0b, 0x3e, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x23, 0x20, 0x00, 0x00, 0x00, 0x70, 0x00, 0x0a, 0x39, 0xa0, 0x00, 0x00, 0x00, 0x18, 0x00, 0x0a, 0x3c, 0xa0, 0x00, 0x00, 0x00, 0x08, 0x00, 0x0b, 0x3c, 0xa0, 0x00, 0x00, 0x00, 0x08, 0x00, 0x09, 0x18, 0xa0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x01, 0xa0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x83, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0xc6, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x7c, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xff, 0x80, 0x00, 0x00, 0x00, 0x00, ],
    ],[
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x1f, 0xc1, 0x8e, 0x00, 0x30, 0x00, 0x00, 0x00, 0x18, 0x7f, 0x03, 0xc0, 0x60, 0x00, 0x00, 0x00, 0x0c, 0x0c, 0x00, 0x79, 0x80, 0x00, 0x00, 0x00, 0x06, 0x18, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x03, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
      [],
      []
    ], "confused")
inquestitive = IEmotion([
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0e, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x80, 0x00, 0x00, 0x00, 0x70, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x03, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, ],
    ],[
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x80, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xe0, 0x08, 0x00, 0x00, 0x00, 0x38, 0x00, 0x0c, 0x3c, 0x18, 0x00, 0x00, 0x00, 0x2f, 0x80, 0x08, 0x04, 0x10, 0x00, 0x00, 0x00, 0x20, 0xe0, 0x10, 0x03, 0x30, 0x00, 0x00, 0x00, 0x20, 0x7f, 0xb0, 0x00, 0xe0, 0x00, 0x00, 0x00, 0x21, 0x80, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x37, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00],
      [],
    ], "inquestitive")
love = IEmotion([
      [0x00, 0xfc, 0x07, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x01, 0x87, 0x1c, 0x30, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0xf0, 0x10, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x40, 0x10, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x70, 0x01, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x18, 0x01, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x08, 0x01, 0x80, 0x00, 0x30, 0x00, 0x00, 0x00, 0x08, 0x00, 0xc0, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xb8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00,],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78, 0x03, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xce, 0x0e, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x83, 0xb8, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0xe0, 0x20, 0x00, 0x00, 0x00, 0x70, 0x00, 0x80, 0x00, 0x20, 0x00, 0x00, 0x00, 0x18, 0x00, 0xc0, 0x00, 0x60, 0x00, 0x00, 0x00, 0x08, 0x00, 0x60, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x08, 0x00, 0x30, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0e, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xb0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ],
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x19, 0xb3, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00, 0x10, 0xe1, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x10, 0x41, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x18, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xb0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  ],
    ],[
      [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x60, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x0c, 0x30, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x08, 0x18, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x0e, 0x0c, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x03, 0x86, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0xe1, 0x00, 0x06, 0x00, 0x30, 0x00, 0x00, 0x00, 0x19, 0x80, 0x07, 0x80, 0x60, 0x00, 0x00, 0x00, 0x07, 0xc0, 0x08, 0xc0, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x3c, 0x18, 0x70, 0x80, 0x00, 0x00, 0x00, 0x00, 0x07, 0xf0, 0x19, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
      [],
    ], "love")

HALL_EFFECT_PIN = 19
hall_effect_en = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(HALL_EFFECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


DO_AUTO_BLINKS = True
EMOTION = 0
BOOT_TIME = 10
IP = sys.argv[1]
FONTFACE = "Roboto-Regular.ttf"
patriotism = False
current_mouth_state = 0

FRAME_WIDTH = 64
FRAME_HEIGHT = 16
col = [6, 182, 212] #Color of pixels
current_eye_state = 0
update_ready = True

blink_time = 0.2
blink_timer = time.perf_counter()


emotions = [
  default,
  happy,
  tired,
  eyes_closed,
  angry,
  furious,
  "thinking",
  inquestitive,
  confused,
  love
]
#Functions down here

#Split a frame into its rows
def frame_to_rows(frame):
  size = int(FRAME_WIDTH/8)
  rows = []
  for i in range(0, len(frame), size):
    rows.append(frame[i:i+size])
  return rows

#Turn a row with single-bit pixels into a row with RGB pixels
def row_to_rgb(row, col_on, col_off):
  new_row = []
  for byte in row:
    for i in range(8):
      bit = byte >> 7-i & 1
      if bit == 1:
        new_row.append(col_on)
      else:
        new_row.append(col_off)
  return new_row

#Take pixel arrays and turn them into an image
def array_to_img(arr, on_col):
  arr2 = []
  for row in arr:
    arr2.append(row_to_rgb(row, on_col, [0,0,0]))
  return Image.fromarray(np.uint8(arr2)).convert("RGB")

#Take the current frame states and turn them into a image to send to the panels
def frames_to_img(eyeframe, mouthframe):
  global EMOTION
  eye = frame_to_rows(emotions[EMOTION].eyearray[eyeframe])
  mouth = frame_to_rows(emotions[EMOTION].moutharray[mouthframe])
  img = array_to_img(eye+mouth, col if EMOTION != 5 else [245,74,0]) #Generate base image

  img_out = Image.new('RGB', (img.width*2, img.height)) #Create image with size of both panels
  img_out.paste(ImageOps.mirror(img), (img.width,0)) #Gotta mirror one to make them face the right way
  img_out.paste(img, (0, 0))
  
  return img_out

#Mouth animation interrupt function

def init():
  global matrix
  global ring_thread
  
  options = RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  options.gpio_slowdown = 2
  options.hardware_mapping = 'adafruit-hat'
  matrix = RGBMatrix(options=options)

def clear_up():
  fp = open("db.txt", "w")
  fp.write("0\tTrue\tFalse")
  fp.close()
  matrix.Clear()
  GPIO.cleanup()

#Manually queue a blink for now
def start_blink():
  global blink_timer
  blink_timer = time.perf_counter()

#Calculate and check the current blink frames, allows for animations without a sleep command
def do_blink_update():
  global EMOTION
  global blink_timer
  global current_eye_state
  global update_ready
  global DO_AUTO_BLINKS
  blink_frames = len(emotions[EMOTION].eyearray)-1 #How many frames in the animation, 0 index'd for array access
  time_since_start = time.perf_counter() - blink_timer #Time since the start of the animation, goes negative if we haven't started yet
  if time_since_start < 0: #So we can queue blinks without things getting weird
    return
  interval = blink_time / (blink_frames if blink_frames > 0 else 1) #Interval between frames
  frame_counter = int((math.floor(time_since_start*(1/interval))/(1/interval))/interval) #Turn the time since start into the frame number with specified interval
  real_frame = 0 #Because we play it backwards afterwards, keep track of the real frame that we want to show
  
  #First loop forward, 2nd backward then nothing
  if frame_counter < blink_frames: #Going forward
    real_frame = frame_counter
  elif frame_counter < blink_frames*2: #Going backward
    real_frame = blink_frames - frame_counter%blink_frames #count back down instead of up
  elif frame_counter > blink_frames*2: #Animation is done
    real_frame = 0
    if DO_AUTO_BLINKS: #If we are using auto-blinks, queue next blink
      #For confused, and love emotions delay is lowered to create more dynamic animation
      delay = (random.randint(50, 70)/10) if EMOTION < 8 else 0.25
      blink_timer = time.perf_counter() + delay
  else: #Incase things get weird
    real_frame = 0
  
  #if we have a new frame, queue update
  if current_eye_state != real_frame:
    current_eye_state = real_frame
    update_ready = True #Tell main loop we have a new frame to display

def draw_hu_flag(img):
  draw = ImageDraw.Draw(img)
  draw.rectangle([(0,24),(12,26)], fill=(206, 41, 57))
  draw.rectangle([(0,27),(12,29)], fill=(255, 255, 255))
  draw.rectangle([(0,30),(12,32)], fill=(71, 112, 80))

  draw.rectangle([(FRAME_WIDTH*2 -12,24),(FRAME_WIDTH*2,26)], fill=(206, 41, 57))
  draw.rectangle([(FRAME_WIDTH*2 -12,27),(FRAME_WIDTH*2,29)], fill=(255, 255, 255))
  draw.rectangle([(FRAME_WIDTH*2 -12,30),(FRAME_WIDTH*2,32)], fill=(71, 112, 80))

def clear_hu_flag(img):
  draw = ImageDraw.Draw(img)
  draw.rectangle([(0,24),(12,32)], fill=(0, 0, 0))
  draw.rectangle([(FRAME_WIDTH*2 - 12 ,24),(FRAME_WIDTH*2,32)], fill=(0, 0, 0))

def loop():
  global update_ready
  global current_eye_state
  global EMOTION
  global patriotism
  global FRAME_WIDTH
  global FRAME_HEIGHT
  global hall_effect_en
  global current_mouth_state
  

  time.sleep(0.05)
  try:
    fp = open("db.txt")
    splited = fp.readline().split("\t")
    EMOTION = int(splited[0])
    hall_effect_en = eval(splited[1])
    patriotism = eval(splited[2])

    img = frames_to_img(current_eye_state, current_mouth_state) #Generate image from states
    
    if patriotism:
      draw_hu_flag()
    else:
      clear_hu_flag()

    matrix.SetImage(img) #Show em
    update_ready = False #Mark that we have finished with this update
  except IOError:
    clear_up()
    exit()

  if EMOTION != 6:
    if (GPIO.input(hall_effect_pin) == GPIO.HIGH and hall_effect_en):
      current_mouth_state = 1
    else:
      current_mouth_state = 0

    do_blink_update() #Run blink updater
    if update_ready: #If we have a new frame to display
      img = frames_to_img(current_eye_state, current_mouth_state) #Generate image from states
      if patriotism:
        draw_hu_flag()
      else:
        clear_hu_flag()
      matrix.SetImage(img) #Show em
      update_ready = False #Mark that we have finished with this update
""" else:
    fnt = ImageFont(FONTFACE, 24)
    txt = Image.new("RGB", (FRAME_WIDTH*2, FRAME_HEIGHT*2))
    with Pilmoji(txt) as pilmoji:
      pilmoji.text((0,0), "🤔", (0,0,0), fnt)
      pilmoji.text((FRAME_WIDTH,0), "🤔", (0,0,0), fnt)
    img_out = Image.new('RGB', (txt.width*2, txt.height))
    img_out.paste(txt)
    matrix.SetImage(img_out)"""

def Paste_text_frame(txt, img_out, pos1, pos2):
  img_out.paste(txt, pos1)
  img_out.paste(txt, pos2)

def Percentage_load(txt, fnt, d, img_out):
  for i in range(101):
    d.text((0,0), f"{i}%", font=fnt, fill=tuple(col))
    Paste_text_frame(txt, img_out, (txt.width-38,6), (txt.width,6))
    matrix.SetImage(img_out)
    time.sleep(BOOT_TIME/500)

    if i == 100: #Showing 100% for 2 sec
      time.sleep(2)

    #Clearing previous numbers except 100 so evading overlaps
    d.rectangle([(0,0), (FRAME_WIDTH, FRAME_HEIGHT*2)], (0,0,0))
    Paste_text_frame(txt, img_out, (txt.width-38,6), (txt.width,6))
    matrix.SetImage(img_out)

def Show_IP(img_out):
  txt = Image.new("RGB", (FRAME_WIDTH*2, FRAME_HEIGHT*2))
  d = ImageDraw.Draw(txt)
  splitted = IP.split(".")
  first_half = ".".join(splitted[0:2])
  second_half = ".".join(splitted[2:])
  print(first_half, second_half)

  fnt = ImageFont.truetype(FONTFACE, 12)
  d.text((0,0),first_half, font=fnt, fill=tuple(col))
  d.text((FRAME_WIDTH,0),second_half, font=fnt, fill=tuple(col))
  img_out.paste(txt,(0,0))
  matrix.SetImage(img_out)

def Proto_os_text(txt, d, img_out):
  fnt = ImageFont.truetype(FONTFACE, 8)
  title = "Proto_OS 1.0"
  for i in range(len(title)):
    d.text((0+(i*5),0), title[i], font=fnt, fill=tuple(col))
    Paste_text_frame(txt, img_out, (0,6), (txt.width,6))
    matrix.SetImage(img_out)
    time.sleep(BOOT_TIME/750)

def Separate_face_load(img_out):
  eye_array = frame_to_rows(emotions[EMOTION].eyearray[0]) 
  eye = array_to_img(eye_array, col)
  img_out.paste(ImageOps.mirror(eye), (eye.width,0))
  img_out.paste(eye, (0, 0))
  matrix.SetImage(img_out)

  time.sleep(0.5)
  mouth_arry = frame_to_rows(emotions[EMOTION].moutharray[0])
  img = array_to_img(eye_array+mouth_arry,col)
  img_out.paste(ImageOps.mirror(img), (img.width,0))
  img_out.paste(img, (0, 0))
  matrix.SetImage(img_out)
    
def Boot():
  txt = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT*2))
  fnt = ImageFont.truetype(FONTFACE, 16)
  d = ImageDraw.Draw(txt)
  img_out = Image.new('RGB', (txt.width*2, txt.height)) #Create image with size of both panels
  Percentage_load(txt, fnt, d, img_out)

  #Clearing the whole screen
  d.rectangle([(0,0), (FRAME_WIDTH, FRAME_HEIGHT*2)], (0,0,0))
  Paste_text_frame(txt, img_out, (0,0), (0,0))
  matrix.SetImage(img_out)

  Proto_os_text(txt, d, img_out)
  time.sleep(3)
  #Separate_face_load(img_out)
  d.rectangle([(0,0), (FRAME_WIDTH, FRAME_HEIGHT*2)], (0,0,0))
  Paste_text_frame(txt, img_out, (0,0), (txt.width,0))
  matrix.SetImage(img_out)

  Show_IP(img_out)
  time.sleep(10)


if __name__ == "__main__":
  init()
  Boot()
  while True:
    loop()
  clear_up()
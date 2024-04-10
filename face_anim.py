#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
import time, math, random, threading, os, sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import RPi.GPIO as GPIO

from emotions import emotions
#from pilmoji import Pilmoji


#vars
matrix = None

#Mouth-sync and Bonnet communication setup
HALL_EFFECT_PIN = 19  #Changing this you have to resolder the pins too
hall_effect_en = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(HALL_EFFECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #R_pull_up is 10k

default_db_values = "0\tTrue\tFalse\t0"
DO_AUTO_BLINKS = True
EMOTION = 0
IP = sys.argv[1]
FONTFACE = "Roboto-Regular.ttf"

FRAME_WIDTH = 64
FRAME_HEIGHT = 16
col = [6, 182, 212] #Color of pixels

current_mouth_state = 0
current_eye_state = 0
patriotism = False
update_ready = True

blink_time = 0.2
blink_timer = time.perf_counter()

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

#Setting database values to default, clearing GPIO setup and screen 
def clear_up():
  global default_db_values
  fp = open("db.txt", "w")
  fp.write(default_db_values)
  fp.close()
  matrix.Clear()
  GPIO.cleanup()

def do_mouth_update(is_forward):
  global current_mouth_state
  if is_forward and current_mouth_state < 3:
    current_mouth_state += 1
  elif (not is_forward) and current_mouth_state > 0:
    current_mouth_state -= 1

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
  #First LED matrix
  draw.rectangle([(0,24),(12,26)], fill=(206, 41, 57))
  draw.rectangle([(0,27),(12,29)], fill=(255, 255, 255))
  draw.rectangle([(0,30),(12,32)], fill=(71, 112, 80))

  #Second LED matrix
  draw.rectangle([(FRAME_WIDTH*2 -12,24),(FRAME_WIDTH*2,26)], fill=(206, 41, 57))
  draw.rectangle([(FRAME_WIDTH*2 -12,27),(FRAME_WIDTH*2,29)], fill=(255, 255, 255))
  draw.rectangle([(FRAME_WIDTH*2 -12,30),(FRAME_WIDTH*2,32)], fill=(71, 112, 80))

def default_side_lights(img):
  draw = ImageDraw.Draw(img)
  draw.rectangle([(0,24),(12,32)], fill=(255, 255, 255))
  draw.rectangle([(FRAME_WIDTH*2 - 12 ,24),(FRAME_WIDTH*2,32)], fill=(255, 255, 255))

def loop():
  global update_ready
  global current_eye_state
  global EMOTION
  global patriotism
  global FRAME_WIDTH
  global FRAME_HEIGHT
  global hall_effect_en
  global current_mouth_state
  global HALL_EFFECT_PIN
  

  time.sleep(0.025)  #Required for synchronization with the backend
  try:
    fp = open("db.txt")
    splited = fp.readline().split("\t")

    #Avoiding overindexing mouth and eye arrays
    if EMOTION != int(splited[0]):
      current_mouth_state = 0
      current_eye_state = 0

    EMOTION = int(splited[0])
    hall_effect_en = eval(splited[1])
    patriotism = eval(splited[2])

    img = frames_to_img(current_eye_state, current_mouth_state) #Generate image from state
    
    if patriotism:
      draw_hu_flag(img)
    else:
      default_side_lights(img)

    matrix.SetImage(img) #Show em
    update_ready = False #Mark that we have finished with this update
  except IOError:
    clear_up()
    exit()

  if len(emotions[EMOTION].moutharray) == 4:
    if (GPIO.input(HALL_EFFECT_PIN) == GPIO.HIGH and hall_effect_en):
      do_mouth_update(True) #Motuh opens
    else:
      do_mouth_update(False)  #Mouth closes
      
  do_blink_update() #Run blink updater
  if update_ready: #If we have a new frame to display
    img = frames_to_img(current_eye_state, current_mouth_state) #Generate image from states
    if patriotism:
      draw_hu_flag(img)
    else:
      clear_hu_flag(img)
    matrix.SetImage(img) #Show em
    update_ready = False #Mark that we have finished with this update

def Paste_text_frame(txt, img_out, pos1, pos2):
  img_out.paste(txt, pos1)
  img_out.paste(txt, pos2)

def draw_spinner(img_out):
  canvas = Image.new("RGB", (FRAME_WIDTH*2, FRAME_HEIGHT*2))
  d = ImageDraw.Draw(canvas)
  i = 0
  arc_size = 24
  image_x = (FRAME_WIDTH - arc_size) // 2
  image_y = (FRAME_HEIGHT*2 - arc_size) // 2
  while i < 20:
    d.rectangle([(0,0), (FRAME_WIDTH, FRAME_HEIGHT*2)], (0,0,0))
    Paste_text_frame(canvas, img_out, (0,0), (canvas.width,0))

    d.arc([(image_x,image_y),(image_x+arc_size,image_y+arc_size)], start=((i*30)%360), end=((90*(i+1))%360), fill=tuple(col), width=2)
    img_out.paste(canvas,(0,0))
    img_out.paste(canvas,(FRAME_WIDTH,0))
    matrix.SetImage(img_out)
    i += 1
    time.sleep(0.05)

def moving_text(fnt, title, color, img_out):
  canvas = Image.new("RGB", (FRAME_WIDTH*2, FRAME_HEIGHT*2))
  d = ImageDraw.Draw(canvas)
  for i in range(FRAME_WIDTH*2):
    d.rectangle([(0,0), (FRAME_WIDTH*2, FRAME_HEIGHT*2)], (0,0,0))
    d.text((2*(FRAME_WIDTH-i),(FRAME_HEIGHT*2 - 18) //2),title, font=fnt, fill=color)
    img_out.paste(canvas,(0,0))
    matrix.SetImage(img_out)
    time.sleep(0.04)

def check_server(txt, fnt, d, img_out,  succ_col, fail_col):
  function = "Server"
  with open("db.txt") as fp:
    splited = fp.readline().split("\t")
    if int(splited[3]) > 0:
      function += " : ON"
      moving_text(fnt, function, succ_col, img_out)
    else:
      function += " : OFF"
      moving_text(fnt, function, fail_col, img_out)

def check_hall_effect(txt, fnt, d, img_out, succ_col, fail_col):
  function = "Mouth-sync"
  if GPIO.input(HALL_EFFECT_PIN) == GPIO.LOW:
    function += " : ON"
    moving_text(fnt, function, succ_col, img_out)
  else:
    function += " : OFF"
    moving_text(fnt, function, fail_col, img_out)

def Show_IP(img_out, fnt, canvas):
  d = ImageDraw.Draw(canvas)
  first_half, second_half
  try:
    splitted = IP.split(".")
    first_half = ".".join(splitted[0:2])
    second_half = ".".join(splitted[2:])
  except:
    first_half = "0.0."
    second_half = "0.0"

  d.text((4,(FRAME_HEIGHT*2-18)//2),first_half, font=fnt, fill=tuple(col))
  d.text((FRAME_WIDTH+4,(FRAME_HEIGHT*2-18)//2),second_half, font=fnt, fill=tuple(col))
  img_out.paste(canvas,(0,0))
  matrix.SetImage(img_out)

def face_load(img_out):
  eye_array = frame_to_rows(emotions[EMOTION].eyearray[0])
  mouth_array = frame_to_rows(emotions[EMOTION].moutharray[0])
  img = array_to_img(eye_array+mouth_array,col)
  return img
    
def bar_loading(txt, fnt, d, img_out):
  for i in range(FRAME_WIDTH//2):
    d.rectangle([(i*2, 0),(i*2+1,32)], fill=tuple(col))
    img_out.paste(txt,(0,0))
    img_out.paste(ImageOps.mirror(txt),(FRAME_WIDTH,0))
    matrix.SetImage(img_out)
    time.sleep(abs(0.25-(i/100)))

  time.sleep(0.5)

  face_img = face_load(img_out)
  for i in range(FRAME_WIDTH//2):
    d.rectangle([(0, 0),(i*2+1,32)], fill=(0,0,0))
    img_out.paste(txt,(0,0))
    img_out.paste(ImageOps.mirror(txt),(FRAME_WIDTH,0))
    
    img_out.paste(face_img.crop((0,0,2*i,32)),(0,0))
    img_out.paste(ImageOps.mirror(face_img.crop((0,0,2*i,32))),((FRAME_WIDTH-i)*2,0))

    matrix.SetImage(img_out)
    time.sleep(0.05)

def clear_screens(canvas, img_out):
  d.rectangle([(0,0), (FRAME_WIDTH, FRAME_HEIGHT*2)], (0,0,0))
  Paste_text_frame(canvas, img_out, (0,0), (txt.width,0))
  matrix.SetImage(img_out)

def Boot():
  #vars
  txt = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT*2)) #Canvas object for boot animations
  fnt = ImageFont.truetype(FONTFACE, 16)
  sm_fnt = ImageFont.truetype(FONTFACE, 12)
  d = ImageDraw.Draw(txt) #For draw context
  succ_col = (82, 185, 99)
  fail_col = (206, 41, 57)
  img_out = Image.new('RGB', (txt.width*2, txt.height)) #Create image with size of both panels
  
  #EnginEar booting up
  lightning = Image.open("EnginEar_Logo.png").resize((20,28))
  d.text((4,2), "EnginEar\nbooting up", font=sm_fnt, fill=tuple(col))
  img_out.paste(txt, (0,0))
  img_out.paste(lightning, ((FRAME_WIDTH*2 + 20) // 2, (FRAME_HEIGHT*2 - 28) // 2))
  matrix.SetImage(img_out)
  time.sleep(5)

  #Server status
  draw_spinner(img_out)
  check_server(txt, fnt, d, img_out, succ_col, fail_col)
  
  #Motuh-sync status
  draw_spinner(img_out)
  check_hall_effect(txt, fnt, d, img_out, succ_col, fail_col)
  clear_screens(txt,img_out)

  Show_IP(img_out, sm_fnt, txt)
  time.sleep(5)

  #Face load
  bar_loading(txt, sm_fnt, d, img_out)
  clear_screens(txt,img_out)
  matrix.SetImage(face_load(img_out))


if __name__ == "__main__":
  init()
  Boot()
  while True:
    loop()
  clear_up()
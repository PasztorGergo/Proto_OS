#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
import time, math, random, threading, os, sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import RPi.GPIO as GPIO
import busio
import board
from canvas import Canvas
from emotions import emotions
from adafruit_apds9960.apds9960 import APDS9960
#from pilmoji import Pilmoji

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize APDS9960 sensor
apds = APDS9960(i2c)

# Enable proximity and gesture sensing
apds.enable_proximity = True

#vars
matrix = None

#Mouth-sync and Bonnet communication setup
HALL_EFFECT_PIN = 19  #Changing this you have to resolder the pins too

default_db_values = "0\tTrue\tFalse\t1"
DO_AUTO_BLINKS = True
EMOTION = 0
IP = sys.argv[1]
FONTFACE = "Roboto-Regular.ttf"

FRAME_WIDTH = 64
FRAME_HEIGHT = 16
col = [6, 182, 212] #Color of pixels
col_sec = [16,185,129] #Secondary color of pixels

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
def row_to_rgb(row, row_id, col_on_from, col_on_to,col_off):
  new_row = []
  for byte in row:
    for i in range(8):
      bit = byte >> 7-i & 1
      if bit == 1:
        r = int(col_on_from[0] + (col_on_to[0] - col_on_from[0]) * row_id / 31)
        g = int(col_on_from[1] + (col_on_to[1] - col_on_from[1]) * row_id / 31)
        b = int(col_on_from[2] + (col_on_to[2] - col_on_from[2]) * row_id / 31)
        new_row.append([r,g,b])
      else:
        new_row.append(col_off)
  return new_row

#Take pixel arrays and turn them into an image
def array_to_img(arr, on_col):
  global EMOTION
  arr2 = []
  for i in range(len(arr)):
    if patriotism and i < 11:
      arr2.append(row_to_rgb(arr[i], i, [206, 41, 57], [206, 41, 57],[0,0,0]))
    elif patriotism and i >= 11 and i <22:
      arr2.append(row_to_rgb(arr[i], i, [255, 255, 255], [255, 255, 255],[0,0,0]))
    elif patriotism and i >= 22:
      arr2.append(row_to_rgb(arr[i], i, [71, 112, 80], [71, 112, 80],[0,0,0]))
    else:
      arr2.append(row_to_rgb(arr[i], i,on_col, col_sec if EMOTION != 5 else [245,74,0],[0,0,0]))
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
  global default_db_values

  hall_effect_en = True
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(HALL_EFFECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #R_pull_up is 10k
  
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
  
  POLL_TIME = 0.025

  time.sleep(POLL_TIME)  #Required for synchronization with the backend
  try:
    fp = open("db.txt")
    splited = fp.readline().split("\t")
    next_emotion = EMOTION
    if(len(splited) > 1):
      next_emotion = int(splited[0]) 
      hall_effect_en = eval(splited[1])
      patriotism = eval(splited[2])
     #Avoiding overindexing mouth and eye arrays
    if EMOTION != next_emotion:
      current_mouth_state = 0
      current_eye_state = 0

    if apds.proximity > 190:
      current_mouth_state = 0
      current_eye_state = 0
      EMOTION = 3
    else:
      EMOTION = next_emotion

    img = frames_to_img(current_eye_state, current_mouth_state) #Generate image from state
    
    if patriotism:
      draw_hu_flag(img)
    else:
      default_side_lights(img)

    matrix.SetImage(img) #Show em
    update_ready = False #Mark that we have finished with this update
    fp.close()
  except IOError:
    #Couldn't read file in the current stage. Retry in the next one
    pass
  except:
    clear_up()
    exit()

  if len(emotions[EMOTION].moutharray) == 4:
    if (GPIO.input(HALL_EFFECT_PIN) == GPIO.HIGH and hall_effect_en):
      do_mouth_update(True) #Mouth opens
    else:
      do_mouth_update(False)  #Mouth closes
      
  do_blink_update() #Run blink updater
  if update_ready: #If we have a new frame to display
    img = frames_to_img(current_eye_state, current_mouth_state) #Generate image from states
    if patriotism:
      draw_hu_flag(img)
    else:
      default_side_lights(img)
    matrix.SetImage(img) #Show em
    update_ready = False #Mark that we have finished with this update

def draw_spinner(image):
  canvas = image.get_canvas()
  draw = image.get_draw()
  i = 0
  arc_size = 24
  image_x = (FRAME_WIDTH - arc_size) // 2
  image_y = (FRAME_HEIGHT*2 - arc_size) // 2
  while i < 20:
    image.clear()

    draw.arc([(image_x,image_y),(image_x+arc_size,image_y+arc_size)], start=((i*30)%360), end=((90*(i+1))%360), fill=tuple(col), width=2)
    canvas.paste(canvas,(0,0))
    canvas.paste(ImageOps.mirror(canvas.crop((0,0,FRAME_WIDTH, FRAME_HEIGHT*2))),(FRAME_WIDTH,0))
    matrix.SetImage(canvas)
    i += 1
    time.sleep(0.05)

def moving_text(title, color, image):
  canvas = image.get_canvas()
  draw = image.get_draw()
  for i in range(FRAME_WIDTH*2):
    image.clear()
    image.static_text(title, 16, (2*(FRAME_WIDTH-i),(FRAME_HEIGHT*2 - 18) //2), color)
    matrix.SetImage(canvas)
    time.sleep(0.04)

def check_server(image, succ_col, fail_col):
  function = "Server"
  with open("db.txt") as fp:
    splited = fp.readline().split("\t")
    if int(splited[3]) > 0:
      function += " : ON"
      moving_text(function, succ_col, image)
    else:
      function += " : OFF"
      moving_text(function, fail_col, image)

def check_hall_effect(image, succ_col, fail_col):
  function = "Mouth-sync"
  if GPIO.input(HALL_EFFECT_PIN) == GPIO.LOW:
    function += " : ON"
    moving_text(function, succ_col, image)
  else:
    function += " : OFF"
    moving_text(function, fail_col, image)

def Show_IP(image):
  first_half = "0.0."
  second_half = "0.0"
  try:
    splitted = IP.split(".")
    first_half = ".".join(splitted[0:2])
    second_half = ".".join(splitted[2:])
  except:
    pass

  image.static_text(first_half,position=(4,(FRAME_HEIGHT*2-18)//2))
  image.static_text(second_half,position=(FRAME_WIDTH+4,(FRAME_HEIGHT*2-18)//2))
  matrix.SetImage(image.get_canvas())

def face_load():
  eye_array = frame_to_rows(emotions[EMOTION].eyearray[0])
  mouth_array = frame_to_rows(emotions[EMOTION].moutharray[0])
  img = array_to_img(eye_array+mouth_array,col)
  return img
    
def bar_loading(image):
  temp_img = Canvas(FRAME_WIDTH, FRAME_HEIGHT*2,FONTFACE)
  canvas = image.get_canvas()
  for i in range(FRAME_WIDTH//2):
    temp_img.get_draw().rectangle([(i*2, 0),(i*2+1,32)], fill=tuple(col))
    canvas.paste(temp_img.get_canvas(),(0,0,FRAME_WIDTH,FRAME_HEIGHT*2))
    canvas.paste(ImageOps.mirror(temp_img.get_canvas()),(FRAME_WIDTH,0,FRAME_WIDTH*2,FRAME_HEIGHT*2))
    matrix.SetImage(canvas)
    time.sleep(abs(0.25-(i/100)))

  time.sleep(0.5)

  face_img = face_load()
  for i in range(FRAME_WIDTH//2):
    temp_img.get_draw().rectangle([(0, 0),(i*2+1,32)], fill=(0,0,0))
    canvas.paste(temp_img.get_canvas(),(0,0))
    canvas.paste(ImageOps.mirror(temp_img.get_canvas()),(FRAME_WIDTH,0))
    
    canvas.paste(face_img.crop((0,0,2*i,32)),(0,0))
    canvas.paste(ImageOps.mirror(face_img.crop((0,0,2*i,32))),((FRAME_WIDTH-i)*2,0))

    matrix.SetImage(canvas)
    time.sleep(0.05)

def Boot():
  #vars
  image = Canvas(FRAME_WIDTH*2,FRAME_HEIGHT*2, FONTFACE)
  #Colors for functionalities
  succ_col = (82, 185, 99)
  fail_col = (206, 41, 57)

  #EnginEar booting up
  lightning = Image.open("EnginEar_Logo.png").resize((20,28))
  image.static_text(text="EnginEar\nbooting up", size=12, position=(4,2))
  image.get_canvas().paste(lightning, ((FRAME_WIDTH*2 + 20) // 2, (FRAME_HEIGHT*2 - 28) // 2))
  matrix.SetImage(image.get_canvas())
  time.sleep(5)

  #Server status
  draw_spinner(image)
  check_server(image, succ_col, fail_col)
  
  #Motuh-sync status
  draw_spinner(image)
  check_hall_effect(image, succ_col, fail_col)
  image.clear()

  Show_IP(image)
  time.sleep(5)

  #Face load
  bar_loading(image)
  image.clear()
  matrix.SetImage(face_load())


if __name__ == "__main__":
  init()
  Boot()
  while True:
    loop()
  clear_up()
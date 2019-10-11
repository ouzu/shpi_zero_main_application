#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pi3d
import sys,os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import requests

import config
import core.graphics as graphics
import core.peripherals as peripherals
import core.mqttclient as mqttclient
import json

text = pi3d.PointText(graphics.pointFont, graphics.CAMERA, max_chars=35, point_size=128) 
text2 = pi3d.PointText(graphics.pointFontbig, graphics.CAMERA, max_chars=35, point_size=256)  #also big font possible, higher resolution


# look for graphics in core/graphics.py  0xE00F -> light,   0xE001 -> circle

httpbutton = pi3d.TextBlock(0, 0, 0.1, 0.0, 1, text_format= chr(0xE00F),size=0.99, spacing="C", space=0.6, colour=(1, 1, 1, 1))
circle = pi3d.TextBlock(-5, 15, 0.1, 0.0, 1, text_format= chr(0xE001),size=0.99, spacing="C", space=0.6, colour=(1, 1, 1, 1))

text.add_text_block(httpbutton)
text2.add_text_block(circle)
httpbutton.status = 'unknown'  # on init status is unknown


def inloop(textchange = False,activity = False, offset = 0):
      
  if textchange:
    text.regen()
    text2.regen()       
  
  if httpbutton.status == 'unknown':
    get_button_status()
  if httpbutton.status == 'error':
    httpbutton.colouring.set_colour([0,0,1]) 
  if peripherals.touch_pressed:
    peripherals.touch_pressed = False     
  
  if peripherals.clicked(httpbutton.x,httpbutton.y):
    url = 'http://10.0.1.172:8123/api/services/light/toggle'
    headers = {
      'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI4MGQ0NjA4YjlkMWY0MTkwOGIwNGUxMDZiMzY4MmQxMiIsImlhdCI6MTU3MDgxNzYxNiwiZXhwIjoxODg2MTc3NjE2fQ.rWoJeWwFkQgX726L_-wIYMt3bXXnay8HPMH1UTJec28',
      'content-type': 'application/json',
    }
    requests.post(url, headers=headers, data='{"entity_id": "light.wohnzimmer"}')
  return activity,offset


def get_button_status():
  pass

















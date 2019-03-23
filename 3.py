# -*- coding:utf-8 -*-
import pymouse,pykeyboard,os,sys
import time
from pymouse import *
from pykeyboard import PyKeyboard
import configparser

m = PyMouse() 
k = PyKeyboard()

def getIePos():
    

# time.sleep(2)
# print(m.position())

m.move(814,998) 
k.type_string('abcdefg') 
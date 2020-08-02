

from kivy import require
require('1.0.1')


from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.clock import Clock  
from kivy.graphics import Color, Ellipse, Triangle, Rectangle, Line
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.app import App
from kivy.lang import Builder

from random import random,choice
from math import sin,cos,sqrt,atan

import os
import psutil


def unsignedDist(a,b):
	return sqrt( ((a[0]-b[0])*(a[0]-b[0])) + ((a[1]-b[1])*(a[1]-b[1])) )

def keepVelocity(velocity,speed):
	sum  = unsignedDist(velocity,(0,0))
	if(sum==0):
		return
	velocity[0]/=sum 
	velocity[1]/=sum 
	velocity[0]*=speed 
	velocity[1]*=speed 

	return velocity


def funcSep(instance,value):
	global sepForce
	sepForce = value
	
def funcCohe(instance,value):
	global coheForce
	coheForce = value

def funcAllign(instance,value):
	global allignForce
	allignForce = value


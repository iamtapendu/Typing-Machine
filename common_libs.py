# All important libraries
import os
import re
import time
import json
import random

import matplotlib
import pygame
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as bck
matplotlib.use('TkAgg')
import scipy.stats as st
import statistics as stat
from PIL import Image,ImageTk

# constants using as color
BG_CLR = '#f8f8f8'
FG_CLR = '#222'
ACT_CLR = '#0b73b8'
HIGHLIGHT_CLR = '#FF4733'

# Various Paths
AUDIO_PATH = os.path.abspath('data/audio')+'/'
DB_PATH = os.path.abspath('data/db')+'/'
STORY_PATH = os.path.abspath('data/story')+'/'
PROFILE_PATH = os.path.abspath('data/profile.info')

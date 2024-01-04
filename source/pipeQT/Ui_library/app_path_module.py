'''
import python library
'''
import os
import io
import re
import sys
import math
import time
import glob
import json
import urllib
import socket
import pprint
import string
import signal
import platform
import threading
import traceback
import subprocess
import configparser
from pathlib import Path
from importlib import reload
# from signal import SIGKILL

'''
import third party modules
'''
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules').replace('\\', '/'))
import yaml
from source.py import platforms

'''
import pyside
'''
if platforms.is_windows():
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'modules','pyside2','window').replace('\\', '/'))

elif platforms.is_linux():
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'modules','pyside2','linux').replace('\\', '/'))

else:
    pass

try:
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtCore import Qt

except Exception:
    print(traceback.format_exc())

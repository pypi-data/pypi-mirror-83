#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fil3s.v1.classes.config import *

# invalid os.
def __invalid_os__(os):
	raise OSError(f"Unsupported operating system [{os}].")
	#

# check memory only path.
def __check_memory_only__(os):
	if path == False: 
		raise ValueError("This object is only used in the local memory and is not supposed to be saved or loaded.")
	#
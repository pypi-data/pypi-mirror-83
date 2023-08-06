#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fil3s.v1.classes.config import *

# invalid os.
def __invalid_os__(os):
	raise OSError(f"Unsupported operating system [{os}].")
	#

# check memory only path.
def __check_memory_only__(path):
	if path == False: 
		raise ValueError("This object is only used in the local memory and is not supposed to be saved or loaded.")
	#

# the generate object.
class Generate(object):
	def __init__(self):
		a=1
	def pincode(self, characters=6, charset=string.digits):
		return ''.join(random.choice(charset) for x in range(characters))
		#
	def shell_string(self, characters=6, numerical_characters=False, special_characters=False):
		charset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
		for x in ast.literal_eval(str(charset)): charset.append(x.upper())
		if numerical_characters:
			for x in [
				'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
			]: charset.append(x)
		if special_characters:
			for x in [
				'-', '+', '_'
			]: charset.append(x)
		return ''.join(random.choice(charset) for x in range(characters))
		#

# default initialized classes.
generate = Generate()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, pathlib

# settings.
def __get_source_path__(package_name, index=1):
	executive_dir = str(pathlib.Path(__file__).absolute()).replace(os.path.basename(pathlib.Path(__file__)), '').replace("//","/")
	if executive_dir[len(executive_dir)-1] == "/": executive_dir = executive_dir[:-1]
	source, c = "/", 1
	for id in executive_dir.split("/"):
		if id == package_name:
			if c == index:
				source += id+"/"
				break
			else: 
				source += id+"/"
				c += 1
		else: source += id+"/"
	base = source[:-1].split("/")
	base = source.replace(f'/{base[len(base)-1]}/', '/')
	return source, base

	#
SOURCE_NAME = "encrypti0n"
VERSION = "v1"
index = 1
if '--developer' in sys.argv: index = 2
SOURCE_PATH, BASE = __get_source_path__(SOURCE_NAME, index=index)
sys.path.insert(1, BASE)

# imports.
from encrypti0n.v1.classes.config import *
from encrypti0n.v1.classes import utils
from encrypti0n.v1.classes.encryption import Encryption,EncryptedDictionary


# the cli object class.
class CLI(object):
	def __init__(self, alias=None):
		
		# variables.
		self.modes={
			"--generate-keys":"Generate a key pair.",
			"--encrypt /path/to/file":"Encrypt the provided file path.",
			"--decrypt /path/to/file":"Decrypt the provided file path.",
			"-h / --help":"Show the documentation.",
		},
		self.options={
			"-k / --key /path/to/directory/":"Specify the path to the keys directory.",
			"-p / --passphrase 'Passphrase123!'":"Specify the key passphrase.",
		}
		self.alias = ALIAS
		self.documentation = self.__create_docs__()

		#
	def start(self):
		
		# help.
		if self.__argument_present__('-h') or self.__argument_present__('--help'):
			print(self.documentation)

		# encrypt.
		elif self.__argument_present__('--encrypt'):
			file = self.__get_argument__('--encrypt')
			key, passphrase = self.get_key_passphrase()
			_encryption_ = Encryption(key=key, passphrase=passphrase)
			_encryption_.load_keys()
			_encryption_.encrypt_file(file)

		# decrypt.
		elif self.__argument_present__('--decrypt'):
			file = self.__get_argument__('--decrypt')
			key, passphrase = self.get_key_passphrase()
			_encryption_ = Encryption(key=key, passphrase=passphrase)
			_encryption_.load_keys()
			_encryption_.decrypt_file(file)

		# generate-keys.
		elif self.__argument_present__('--generate-keys'):
			file = self.__get_argument__('--generate-keys')
			key, passphrase = self.get_key_passphrase()
			_encryption_ = Encryption(key=key, passphrase=passphrase)
			_encryption_.generate_keys()

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	def get_key_passphrase(self):
		key = self.__get_argument__('-k', required=False)
		if key == None:
			key = self.__get_argument__('--key', required=True)
		passphrase = self.__get_argument__('-p', required=False)
		if passphrase == None:
			passphrase = self.__get_argument__('--passphrase', required=True)
		return key, passphrase
	# system functions.
	def __create_docs__(self):
		m = str(json.dumps(self.modes, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		#o = str(json.dumps(self.options, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		o = str(json.dumps(self.options, indent=4)).replace('{\n','').replace('}\n','').replace('    "','    ').replace('": "',' : ').replace('",\n','\n').replace('"\n','\n')[:-2]
		c = "\nAuthor: Daan van den Bergh \nCopyright: © Daan van den Bergh 2020. All rights reserved."
		doc = "Usage: "+self.alias+" <mode> <options> \nModes:\n"+m
		if o != "": doc += "\nOptions:\n"+o
		doc += c
		return doc
	def __argument_present__(self, argument):
		if argument in sys.argv: return True
		else: return False
	def __get_argument__(self, argument, required=True, index=1, empty=None):

		# check presence.
		if argument not in sys.argv:
			if required:
				raise ValueError(f"Define parameter [{argument}].")
			else: return empty

		# retrieve.
		y = 0
		for x in sys.argv:
			try:
				if x == argument: return sys.argv[y+index]
			except IndexError:
				if required:
					raise ValueError(f"Define parameter [{argument}].")
				else: return empty
			y += 1

		# should not happen.
		return empty
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()

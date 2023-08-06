#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, requests, ast, json, pathlib, glob, platform

# fyunctions.
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "osx"
	elif os in ["linux"]: return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")

# source.
ALIAS = "encrypti0n"
SOURCE_NAME = "encrypti0n"
VERSION = "v1"
SOURCE_PATH = str(str(pathlib.Path(__file__).absolute()).replace(os.path.basename(pathlib.Path(__file__)), '').split('/'+SOURCE_NAME+"/")[0]+"/"+SOURCE_NAME+"/").replace("//","/")

# universal variables.
OS = __get_operating_system__()

# file settings.
ADMINISTRATOR = "administrator"
OWNER = os.environ.get("USER")
GROUP = "root"
if OS in ["osx"]: GROUP = "wheel"
SUDO = True
ADMIN_PERMISSION = 700
READ_PERMISSION = 750
WRITE_PERMISSION = 770

# functions.
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()
def __check_alias__():
	alias = SOURCE_NAME.lower()
	path = f"/usr/local/bin/{alias}"
	if not os.path.exists(path):
		file = f"""package={SOURCE_PATH}/{VERSION}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
		os.system(f"sudo touch {path}")
		os.system(f"sudo chmod 755 {path}")
		if OS in ["osx"]:
			os.system(f"sudo chown {os.environ.get('USER')}:wheel {path}")
		elif OS in ["linux"]:
			os.system(f"sudo chown {os.environ.get('USER')}:root {path}")
		__save_file__(f"{path}", file)
		os.system(f"sudo chmod 755 {path}")
		if '--silent' not in sys.argv:
			print(f'Successfully created alias: {alias}.')
			print(f"Check out the docs for more info $: {alias} -h")

# checks.
__check_alias__()
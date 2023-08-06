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
			else: c += 1
		else: source += id+"/"
	base = source[:-1].split("/")
	base = source.replace(f'/{base[len(base)-1]}/', '/')
	return source, base
SOURCE_NAME = "encrypti0n"
VERSION = "v1"
SOURCE_PATH, BASE = __get_source_path__(SOURCE_NAME)

# imports.
from encrypti0n.v1.classes.config import *
from encrypti0n.v1.classes import utils
from encrypti0n.v1.classes.encryption import Encryption

# functions.
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
		utils.__save_file__(f"{path}", file)
		os.system(f"sudo chmod 755 {path}")
		if not self.__argument_present__('--silent'):
			print(f'Successfully created alias: {alias}.')
			print(f"Check out the docs for more info $: {alias} -h")

# checks.
__check_alias__()
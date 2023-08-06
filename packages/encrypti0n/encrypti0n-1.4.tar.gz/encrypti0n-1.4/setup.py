# source: https://python-packaging.readthedocs.io/en/latest/minimal.html
import os, sys, pathlib, json
from setuptools import setup, find_packages

# utils.
def __get_argument__(argument, required=True, index=1, empty=None):

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
def __load_json__(path):
	data = None
	with open(path, "r") as json_file:
		data = json.load(json_file)
	return data
def __save_json__(path, data):
	with open(path, "w") as json_file:
		json.dump(data, json_file, indent=4, ensure_ascii=False)
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
	return source

# settings.
package = "encrypti0n"
source = __get_source_path__(package, index=1)
config = __load_json__(f'{source}/config.json')
setup(
	name=package,
	version=config["version"],
	description=config["description"],
	url=f'http://github.com/vandenberghinc/{package}',
	author=config["author"],
	author_email=config["email"],
	license='MIT',
	packages=find_packages(include=[package]),
	zip_safe=True)
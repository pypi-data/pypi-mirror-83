#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from encrypti0n.v1.classes.config import *
from encrypti0n.v1.classes import utils

# new imports.
import zlib, base64, binascii, glob, shutil, multiprocessing
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# the encryption class.
class Encryption(object):
	def __init__(self, 
		key=None,
		passphrase=None,
	):
		self.key = key
		self.passphrase = passphrase
		self.public_key = None
		self.private_key = None
	# key management.
	def generate_keys(self):

		# default response.
		response = utils.__default_response__()

		# checks.
		if os.path.exists(self.key): 
			response["error"] = f"Key [{self.key}] already exists."
			return response
			
		# generate.
		key_pair = RSA.generate(4096, e=65537)
		public_key = key_pair.publickey()
		public_key_pem = public_key.exportKey()
		private_key_pem = None
		if self.passphrase == None: 
			private_key_pem = key_pair.exportKey()
		else:  
			private_key_pem = key_pair.exportKey(passphrase=self.passphrase)

		# save.
		os.mkdir(self.key)
		utils.__save_file__(self.key+"/private_key.pem", private_key_pem.decode())
		utils.__save_file__(self.key+"/public_key.pem", public_key_pem.decode())
		utils.__set_file_path_permission__(self.key, permission=700)
		
		# response.
		response["success"] = True
		response["message"] = "Successfully generated a key pair."
		return response

		#
	def load_keys(self):

		# load keys.
		response = utils.__default_response__()
		self.public_key = utils.__load_file__(self.key+"/public_key.pem")
		self.private_key = utils.__load_file__(self.key+"/private_key.pem")

		# initialize keys.
		if self.passphrase == None:
			self.public_key = RSA.importKey(self.public_key)
			self.private_key = RSA.importKey(self.private_key)
		else:
			self.public_key = RSA.importKey(self.public_key, passphrase=self.passphrase)
			self.private_key = RSA.importKey(self.private_key, passphrase=self.passphrase)
		
		# response.
		response["success"] = True
		response["message"] = "Successfully loaded the key pair."
		return response
	# encrypting.
	def encrypt_file(self, path):
		response = utils.__default_response__()
		file = utils.__load_bytes__(path)
		encrypted = self.__encrypt_blob__(file, self.public_key)
		utils.__save_bytes__(path, encrypted)
		response["success"] = True
		response["message"] = f"Successfully encrypted file [{path}]."
		return response
	def encrypt_string(self, string):
		response = utils.__default_response__()
		encrypted = self.__encrypt_blob__(string, self.public_key)
		response["success"] = True
		response["message"] = f"Successfully encrypted file [{path}]."
		response["encrypted"] = encrypted.decode()
		return response
	# decrypting.
	def decrypt_file(self, path):
		response = utils.__default_response__()
		file = utils.__load_bytes__(path)
		decrypted = self.__decrypt_blob__(file.encode(), self.private_key)
		utils.__save_bytes__(path, decrypted)
		response["success"] = True
		response["message"] = f"Successfully decrypted file [{path}]."
		return response
	def decrypt_string(self, string):
		response = utils.__default_response__()
		if isinstance(string,str): string = string.encode()
		decrypted = self.__decrypt_blob__(string, self.private_key)
		response["success"] = True
		response["message"] = f"Successfully encrypted file [{path}]."
		response["decrypted"] = decrypted.decode()
		return response
	# system functions.
	def __encrypt_blob__(self, blob, public_key, silent=False):
		#Import the Public Key and use for encryption using PKCS1_OAEP
		rsa_key = public_key
		rsa_key = PKCS1_OAEP.new(rsa_key)

		#compress the data first
		try: 
			blob = zlib.compress(blob.encode())
		except: 
			blob = zlib.compress(blob)
		
		#In determining the chunk size, determine the private key length used in bytes
		#and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
		#in chunks
		chunk_size = 470
		offset = 0
		end_loop = False
		encrypted = bytearray()
		max_offset, progress = len(blob), 0
		if silent == False: print(f'Encrypting {max_offset} bytes.')
		while not end_loop:
			#The chunk
			chunk = blob[offset:offset + chunk_size]

			#If the data chunk is less then the chunk size, then we need to add
			#padding with " ". This indicates the we reached the end of the file
			#so we end loop here
			if len(chunk) % chunk_size != 0:
				end_loop = True
				#chunk += b" " * (chunk_size - len(chunk))
				chunk += bytes(chunk_size - len(chunk))
			#Append the encrypted chunk to the overall encrypted file
			encrypted += rsa_key.encrypt(chunk)

			#Increase the offset by chunk size
			offset += chunk_size
			l_progress = round((offset/max_offset)*100,2)
			if l_progress != progress:
				progress = l_progress
				if silent == False: print('Progress: '+str(progress), end='\r')

		#Base 64 encode the encrypted file
		return base64.b64encode(encrypted)
	def __decrypt_blob__(self, encrypted_blob, private_key, silent=False):

		#Import the Private Key and use for decryption using PKCS1_OAEP
		rsakey = private_key
		rsakey = PKCS1_OAEP.new(rsakey)

		#Base 64 decode the data
		encrypted_blob = base64.b64decode(encrypted_blob)

		#In determining the chunk size, determine the private key length used in bytes.
		#The data will be in decrypted in chunks
		chunk_size = 512
		offset = 0
		decrypted = bytearray()
		max_offset = len(encrypted_blob)
		progress = 0
		if silent == False: print(f'Decrypting {max_offset} bytes.')
		#keep loop going as long as we have chunks to decrypt
		while offset < len(encrypted_blob):
			#The chunk
			chunk = encrypted_blob[offset: offset + chunk_size]

			#Append the decrypted chunk to the overall decrypted file
			decrypted += rsakey.decrypt(chunk)

			#Increase the offset by chunk size
			offset += chunk_size
			l_progress = round((offset/max_offset)*100,2)
			if l_progress != progress:
				progress = l_progress
				if silent == False: print('Progress: '+str(progress), end='\r')

		#return the decompressed decrypted data
		return zlib.decompress(decrypted)


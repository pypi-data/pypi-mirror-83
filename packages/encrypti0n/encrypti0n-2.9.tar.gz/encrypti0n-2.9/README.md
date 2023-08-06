# Encrypti0n
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: osx & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>


## Installation:

	pip3 install encrypti0n

## CLI:
	Usage: encryption <mode> <options> 
	Modes:
		--generate-keys : Generate a key pair.
	    --encrypt /path/to/file : Encrypt the provided file path.
	    --decrypt /path/to/file : Decrypt the provided file path.
	    --create-alias : Create an alias.
	    -h / --help : Show the documentation.
	Options:
	    -k / --key /path/to/directory/ : Specify the path to the keys directory.
	    -p / --passphrase 'Passphrase123!Passphrase123!' : Specify the keys passphrase.
	Author: Daan van den Bergh 
	Copyright: © Daan van den Bergh 2020. All rights reserved.

## Python Examples.
Import the encryption package.
```python
# import the encryption object.
from encrypti0n.v1 import Encryption
```

Initialize the encryption class (Leave the passphrase None if you require no passphrase).
```python
# initialize the encryption class.
encryption = Encryption(
	key='mykey/',
	passphrase='MyPassphrase123!')
```

Generating the keys.
```python
# generate the key pair.
response = encryption.generate_keys()
```

Load the generated keys before encrypting / decrypting.
```python
# load the key pair.
response = encryption.load_keys()
```

Encrypting items.
```python
# encrypting a string.
response = encryption.encrypt_string('Hello World!')

# encrypting a file.
response = encryption.encrypt_file('file.txt')

# encrypting a directory (creates a zip).
response = encryption.encrypt_directory('directory/')
```

Decrypting items.
```python
# decrypting a string.
response = encryption.decrypt_string('Hello World!')

# decrypting a file.
response = encryption.decrypt_file('file.txt')

# decrypting a directory (from the encrypted zip).
response = encryption.decrypt_directory('directory/')
```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}
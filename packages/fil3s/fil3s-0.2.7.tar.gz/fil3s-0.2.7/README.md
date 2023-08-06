# Fil3s
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install fil3s

## The Directory class.
The Files.Directory() class. 
<br>Check the source code for more options & classes.
```python

# import the package.
import os
from fil3s import Files, Formats

# initialize a directory.
directory = Files.Directory(path='directory/')

# check the directory.
directory.check(
	owner=os.eniron.get('USER'),
	group=None,
	permission=755,
	sudo=True,
	recursive=False,
	silent=False,
	hierarchy={
		"subdir/":{
			"path":"subdir/",
			"directory":True,
			"owner":os.eniron.get('USER'),
			"group":None,
			"permission":755,
			"sudo":True,
		},
	})

```

## The Dictionary class.
The Files.Dictionary() class. 
<br>Check the source code for more options & classes.
```python

# import the package.
from fil3s import Files, Formats

# initialize a dictionary.
settings = Files.Dictionary(
	path='settings.json',
	load=True,
	default={
		"Hello":'World!',
	})

# the dict is already loaded by the load=True parameter.
settings.load()

# the loaded dict.
print(settings.dictionary)

# saving.
settings.dictionary = {
	"Hello":"World!"
}
settings.save()
settings.save({
	"Hello":"World!"
})

# check dict keys.
settings.check(
	save=True,
	default_dictionary={
		"Hello":'World!',
		"Hi":'World!',
	})

# divide the dictionary into a list of dicts.
list = setting.divide(into=2)

```

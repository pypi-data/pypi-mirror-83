# Fil3s
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: osx & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

# Installation
	pip3 install fil3s

# Files:

## The Directory object class.
The Files.Directory() object class. 
<br>Check the source code for more functions & options.
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
# directory.file_path = <Formats.FilePath>
# directory.file_path.path

# content.
paths = directory.paths(
	recursive=False,
	banned=[],# use full file paths.
)

# check contains.
bool = directory.contains("subdir", "/", recursive=False)

# returnable functions.
path = directory.join("subdir", "/")
path = directory.join("subdir/settings", type="json")
path = directory.oldest_path()
path = directory.random_path(characters=10, type="/")
path = directory.generate_path(characters=10, type="/")
path = directory.structured_join("subdir", type="/", structure="alphabetical")

```

## The Dictionary object class.
The Files.Dictionary() object class. 
<br>Check the source code for more functions & options.
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
# settings.file_path = <Formats.FilePath>
# settings.file_path.path

# the dict is already loaded by the load=True parameter.
settings.load()

# saving.
settings.save({"Hello":"World!"})

# or.
settings.dictionary = {"Hello":"World!"}
settings.save()

# check dictionary.
settings.check(
	save=True,
	default={
		"Hello":'World!',
		"Hi":'World!',
	})

# divide the dictionary into a list of dicts.
list = setting.divide(into=2)

```

# Formats:

## The FilePath object class.
The Formats.FilePath() object class. 
Most Files.* classes contain a FilePath object.
<br>Check the source code for more functions & options.
```python

# import the package.
from fil3s import Files, Formats

# initialize a dictionary.
file_path = Formats.FilePath(path='directory/', check_existance=False)
path = file_path.path

# returnable functions.
name = file_path.name()
extension = file_path.extension()
base = file_path.base(back=1)
size = file_path.size(mode="auto", options=["auto", "bytes", "kb", "mb", "gb", "tb"], type=str)
bool = file_path.exists()
bool = file_path.mount()
bool = file_path.directory()

# executable functions.
file_path.delete(forced=False, sudo=False, silent=False)
file_path.move(path="new-directory/", sudo=False, silent=False)
file_path.copy(path="new-directory/", sudo=False, silent=False)
file_path.open(sudo=False)

# file permissions.
permission = file_path.permission.get()
file_path.permission.set(permission=755, sudo=False, recursive=False, silent=False)
file_path.permission.check(permission=permission, sudo=False, recursive=False, silent=False)

# file ownership.
owner, group = file_path.ownership.get()
file_path.ownership.set(owner=owner, group=group, sudo=False, recursive=False, silent=False)
file_path.ownership.check(owner=owner, group=group, sudo=False, recursive=False, silent=False)

```
## The Date object class.
The Formats.Date() object class. 
<br>Check the source code for more functions & options.
```python

# import the package.
from fil3s import Files, Formats

# initialize a dictionary.
date_object = Formats.Date()

# variables.
date_object.seconds
date_object.minute
date_object.hour
date_object.day
date_object.day_name
date_object.week
date_object.month
date_object.month_name
date_object.year
date_object.date
date_object.timestamp
date_object.shell_timestamp
date_object.seconds_timestamp
date_object.shell_seconds_timestamp
date_object.time

# functions.
stamp = increase(self, date_object.timestamp, weeks=0, days=1, hours=0, seconds=0, format="%d-%m-%y %H:%M")
stamp = decrease(self, date_object.timestamp, weeks=0, days=1, hours=0, seconds=0, format="%d-%m-%y %H:%M")
comparison = compare(self, stamp, date_object.timestamp, format="%d-%m-%y %H:%M")
stamp = convert(self, date_object.timestamp, input="%d-%m-%y %H:%M", output="%Y%m%d")
seconds = to_seconds(self, date_object.timestamp, format="%d-%m-%y %H:%M")
stamp = from_seconds(self, seconds, format="%d-%m-%y %H:%M")

```

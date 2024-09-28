# meshbbs

This is a BBS project to run on a meshtastic node. The project was forked from https://github.com/TheCommsChannel/TC2-BBS-mesh and has been heavily modified.

It uses python poetry to manage the project.

This project is VERY VERY early, so be nice and patient. The code isn't amazing, the model to get and send message was designed to be easy for anyone to write plugins, not to be "correct". You'll understand when you look at the code :)

## Getting started

Make sure you have poetry installed
https://python-poetry.org/

You will need to copy the file `examples/example_config.ini` to config.ini. You should be able to figure this file out if you look in it.

You should be able to run `poetry install` to install all the things, then run `poetry run meshbbs` and the BBS will start to run.

You may want to change your long name to "hello to start BBS" or something similar.

## License

GNU General Public License v3.0

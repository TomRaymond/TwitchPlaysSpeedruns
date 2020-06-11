# TwitchPlaysSpeedruns

Built with python 3.8.2

Additional Package Setup:<br />
pip install pypiwin32<br />
python pywin32_postinstall.py -install<br />
pip install pyyaml<br />
pip install twitch-python<br />
pip install autopy

Required Libs:<br />
win32api & win32con from pypiwin32 + extensions (post_install). Required to send keyboard inputs via windows<br />
yaml from pyyaml. Required to load yaml config files<br />
twitch from twitch-python. User for connection and chatbot interface<br />
autopy is an advanced input library for keyboard inputs<br />

Additional Setup:<br />
You must add "{Your python install directory}\Lib\site-packages\win32" to your systems PYTHONPATH<br />

Notes:<br />
The pywin32_postinstall script may need to be run as admin<br />
The required library 'win32api' is not part of the PythonPath by default<br />
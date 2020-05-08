# TwitchPlaysSpeedruns

Built with python 2.7.14

Additional Package Setup:<br />
pip install pypiwin32<br />
python pywin32_postinstall -install<br />
pip install pyyaml<br />

Required Libs:<br />
win32api & win32con from pypiwin32 + extensions (post_install)<br />
yaml from pyyaml<br />

Additional Setup:<br />
You must add "{Your python install directory}\Lib\site-packages\win32" to your systems PYTHONPATH<br />

Notes:<br />
The pywin32_postinstall script may need to be run as admin<br />
The required library 'win32api' is not part of the PythonPath by default<br />
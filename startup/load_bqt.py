import sys
import os
import inspect

file_name = inspect.getsourcefile(lambda:0)
root_path = os.path.abspath(os.path.join(os.path.dirname(file_name), os.pardir))
site_packages = os.path.join(root_path, "env", "Lib", "site-packages")

# if you do not want to install bqt to the site-packages, the root needs to be on sys.path
# sys.path.append(root_path)
sys.path.append(site_packages)

import bqt


def register():
    bqt.register()


def unregister():
    bqt.unregister()

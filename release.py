#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
import plistlib

VERSION = "0.1.3"
OUTFILE = "adsabs.alfredworkflow"

# Remove the previous build
if os.path.exists(OUTFILE):
    os.remove(OUTFILE)

# Load the plist
with open("info.plist", "rb") as f:
    plist = plistlib.load(f)

# Remove Alfred 3 incompatible arguments
objects = plist.get("objects", [])
for obj in objects:
    if "config" not in obj:
        continue
    config = obj["config"]
    config.pop("argumenttreatemptyqueryasnil", None)
    config.pop("concurrently", None)
    obj["config"] = config

    if "version" in obj and obj.get("version") > 1:
        obj["version"] = obj["version"] - 1

# Clear variables
plist["variables"]["ADS_PYTHON"] = "python"
plist["variables"]["ADS_DEV_KEY"] = ""

# Update the version number
plist["version"] = VERSION

# Create the zip file
with zipfile.ZipFile(OUTFILE, "w") as zf:

    # Save the plist
    print("writing info.plist")
    zf.writestr("info.plist", plistlib.dumps(plist))

    # Copy the other files
    for fn in os.listdir("."):
        if fn in ["info.plist", "__pycache__", "build", "release.py", OUTFILE]:
            continue
        if fn.startswith("."):
            continue
        if fn.endswith(".pyc"):
            continue
        print("writing {0}".format(fn))
        zf.write(fn)

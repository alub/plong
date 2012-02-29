#!/bin/sh

cd `dirname $0`

if [ -x "/Applications/blender.app/Contents/MacOS/blender" ]; then
	COMMAND="/Applications/blender.app/Contents/MacOS/blender"
else
	COMMAND="blender"
fi

exec $COMMAND --background --python tests/all.py

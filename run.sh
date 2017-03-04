#!/bin/sh
# Getting the path this way allows this script to be run correctly from arbitrary location
MY_PATH="`dirname \"$0\"`"              # relative
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"  # absolutized and normalized
if [ -z "$MY_PATH" ] ; then
  # error; for some reason, the path is not accessible
  # to the script (e.g. permissions re-evaled after suid)
  exit 1  # fail
fi
echo "$MY_PATH"
docker-compose -f $MY_PATH/docker-compose.yml run ip-trigger python ip-trigger.py
#!/bin/sh

source ~/path/to/jobnumber.txt # created by runroo.py
ssh yourID@location.com "bash ~/directory/at/location/created/by/copy_phone_directory/${JOBNUMBER}/"

#!/bin/sh
source ./phoneBook/jobnumber.txt

scp -r /path/to/directory/with/runroo you@destination:/path/to/destination/directory/phoneBook${JOBNUMBER}/

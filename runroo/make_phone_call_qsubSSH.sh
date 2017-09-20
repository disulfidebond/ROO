#!/bin/sh

source ~/path/on/origin/phoneBook/jobnumber.txt
ssh you@destination "bash /work/path/on/destination/to/directory/phoneBook${JOBNUMBER}/phoneCall.txt"

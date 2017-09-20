#!/bin/bash

source ~/path/on/origin/jobnumber.txt

scp you@destination:/path/to/destination/directory/phoneBook${JOBNUMBER}/qsubJobRemote.ROOT.${JOBNUMBER}.log ~/path/on/origin/phoneBook/qsubJobRemote.ROOT.${JOBNUMBER}.log

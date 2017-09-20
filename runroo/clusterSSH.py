#!/usr/bin/python
import time
import os.path
import subprocess
import sys
import hashlib

# synopsis of phoneBook:
# phoneHome -> created dynamically, contains return call info
# jobData -> created dynamically, contains remote task info
# jobNumber -> created dynamically, contains remote task number assigned by local
# jobtask -> created statically, contains $PATH and other remote task info
# phonecall -> created statically, *called* dynamically, contains actual remote task command

# others:
# LL{hash:fastaname}
# phoneCallBackSetup -> phoneBook
# copyPhoneDirectory -> sends phoneBook to remote
# makePhoneCall -> executes remote:.../phoneBook/longDistanceCall
# longDistanceCall -> executes phonebook/phonecall.txt on specified remote node
# phonecall.txt -> executes remote task
# phoneHome -> when task is done, attempts to copy back, if fails, waits for retrieval-->identified by hash


l = []
with open('fastaList2_3.txt') as f:
	for i in f:
		i = i.rstrip('\n\r')
		l.append(i)
keyDict = dict()
n=61
node=16
nodeNM = '0'
def clusterSSH(rList, n_ct, node, nodeNM):

	n = c_ct
	for itm in rList:
        kString = hashlib.md5(itm).hexdigest()
        keyDict[kString] = itm
		j = open('/home/adminuser/Documents/fire4Run/phoneBook/jobdata.txt', 'w')
		itm = "export \"QUERYFILE="+itm+"\""
		j.write(itm)
		j.close()
        print('created jobData file')
		time.sleep(7) # guarantees there is no overlap on remote when files are wiped

		jn = open('/home/adminuser/Documents/fire4Run/phoneBook/jobnumber.txt', 'w')
		jn_itm = "export JOBNUMBER="+str(n)
		jn.write(jn_itm)
		jn.close()
        print('created jobNumber')
        time.sleep(5)

		jc = open('/home/adminuser/Documents/fire4Run/phoneBook/longDistanceCall.txt', 'w')
        # nodeName = nodeNM + str(node)
        nodeName = str(node)
        jc_itm = '#!/bin/sh\nsource ~/bazanBLAST/phoneBook4Task/phoneBook' + str(n) + '/jobnumber.txt\nsed -i \"1i\export JOBNUMBER=$JOBNUMBER\" ~/bazanBLAST/phoneBook4Task/phoneBook${JOBNUMBER}/phonecall.txt\nssh jcaskey@delta-c' + nodeName + ' \"bash ~/bazanBLAST/phoneBook4Task/phoneBook${JOBNUMBER}/phonecall.txt\"'
        jc.write(jc_itm)
        jc.close()
        print('created phoneCall file')
        time.sleep(5)

		kFile = '/home/adminuser/Documents/fire4Run/phoneBook/' + 'hashIDString' + '.txt'
        k = open(kFile, 'a')
        kFileWrite = kString + '\n' + itm
        k.write(kFileWrite)
        k.close()
        print('created hash string file')
        time.sleep(4)
		if subprocess.check_call(['bash', 'phoneCallBackSetup.sh']):
			print("Error with Bash setup, please check phoneCallBackSetup.sh before proceeding")
			sys.exit()
        print('ran phoneCallBackSetup')
        time.sleep(10)

		if subprocess.check_call(['bash', 'copy_phone_Directory.sh']):
			print("Error copying data for remote command, please check copy_phone_Directory.sh before proceeding")
			sys.exit()
        print('ran copyPhoneDirectorySetup')
        time.sleep(15)
		fname="/home/adminuser/Documents/fireAndRun/returnphonecall"+str(n)+".txt"
        jobsub = subprocess.Popen(['bash', 'make_phone_call.sh'])
        if jobsub:
        	print('made phone call, pausing before next loop')
        	time.sleep(25)
        elif jobsub < 0:
			print("Error communicating with remote host for command execution")
        	print('Or error with job submission')
			s = "Job Number " + str(n)
			print(s)
			sys.exit()
        else:
        	print('unspecified error or waiting')
#	while True:
#		if os.path.isfile(fname):
#			break
#		else:
#			time.sleep(60)
#			print("Still Waiting")
		print("Continuing with next string")
        time.sleep(1)
		n+=1
        # if not n % 6:
        #    node+=1
        #    if node > 9:
        #        nodeNM = ''

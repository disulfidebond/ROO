#!/usr/bin/python
import time
import os.path
import subprocess
import sys
import hashlib


# notes:
# KEY difference: with sshCluster, phonecall file is already created and modified
# with qsub, phoneCall is created dynamically and creates qsub pbs file

# rList == list of files to process on cluster with qsub
# list is blindly passed to qsub and run using executable
# required arguments are: allocationName, walltime, queue
# admins frown on tying up resources, so this model is a 'fire and flee' approach
# The job is checked remotely, and when completed, a separate script retrieves the resources.

# setup qsub file
# run make_phone_call_qsubSSH.sh -> creates a qsub submission script, then runs job submission and saves jobID in jobLogfile

	def qsubSSH(rList, n_ct, allocationName, wallTime, queueName):
	# wallTime MUST be formatted as
	# HH:MM:SS

	# n_ct == starting integer

	n = n_ct
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
		jn_itm = "export JOBNUMBER="+str(n)+'\n'
		jn_export = "export PBSVAR="+str(n)
		jn.write(jn_itm)
		jn.write(jn_export)
		jn.close()
        print('created jobNumber')
        time.sleep(5)

		jc = open('/home/adminuser/Documents/fire4Run/phoneBook/phoneCall.txt', 'w')
		qsubLine1 = '#!/bin/sh\n\n\n\n'
		qsubLine2 = 'PBSFILE="pbs_script_batch_${PBSVAR}.script"\n'
		qsubLine3 = 'PBSDIR=$(pwd)' # will run in current directory
		qsubLine4 = 'export BLASTFILE='+str(itm) # IMPORTANT: the file MUST be copied to the pwd
		qsubList = [
			'echo \'#!/bin/sh\' >> ${PBSDIR}/${PBSFILE}',
			'echo \'#PBS -l nodes=1:ppn=4\' >> ${PBSDIR}/${PBSFILE}',
			'echo \'#PBS -l walltime=' + str(wallTime) + '\' >> ${PBSDIR}/${PBSFILE}',
			'echo "#PBS -N jcaskeyJobBLAST_${PBSVAR}" >> ${PBSDIR}/${PBSFILE}',
			'echo "#PBS -o ${PBSVAR}.BLASToutput.txt" >> ${PBSDIR}/${PBSFILE}',
			'echo "#PBS -e errlog.${PBSVAR}.err" >> ${PBSDIR}/${PBSFILE}',
			'echo \'#PBS -q ' + str(queueName) + '\' >> ${PBSDIR}/${PBSFILE}',
			'echo \'#PBS -A ' + str(allocationName) + '\' >> ${PBSDIR}/${PBSFILE}',
			'echo \'#PBS -m e\' >> ${PBSDIR}/${PBSFILE}',
			'echo \'#PBS -m jcaskey@lsu.edu\' >> ${PBSDIR}/${PBSFILE}\n\n\n',
			'echo module load blast/2.2.28/INTEL-14.0.2',
			'BLASTFILE=${BLASTFILE}',
			'echo "/usr/local/packages/blast/2.2.28/INTEL-14.0.2/bin/blastn -query ${PBSDIR}/${BLASTFILE} -num_threads 4 -db ${PBSDIR}/Rattus -task blastn -word_size 7 -reward 1 -penalty -2 -gapextend 2 -gapopen 5 -evalue 0.01 -outfmt 7 -max_target_seqs 2" >> ${PBSDIR}/${PBSFILE}\n\n',
			'qsub ${PBSFILE} 1> /work/jcaskey/qsubJobRemote.ROOT.${JOBNUMBER}.log'
		]

		for string_itm in qsubList:
			jc.write(string_itm)
			jc.write('\n')
		jc.close()

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

		jobsub = subprocess.Popen(['bash', 'make_phone_call.sh'])
		if jobsub:
			print('made phone call, pausing before next loop')
			time.sleep(25)
			if subprocess.check_call(['bash', 'copy_phone_Directory.sh']):
				print("Error retrieving job number, check cluster")
				time.sleep(2)

		elif jobsub < 0:
			print("Error communicating with remote host for command execution")
			print('Or error with job submission')
			s = "Job Number " + str(n)
			print(s)
			sys.exit()
		else:
			print('unspecified error or waiting')

		print("Continuing with next string")
        time.sleep(1)
		n+=1

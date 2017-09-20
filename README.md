# ROO
Remote Organizational and Operational task manager

### Introduction
ROO is tool similar to [swarm](https://hpc.nih.gov/apps/swarm.html) that enables jobs to be submitted across multiple nodes, clusters, and servers.  Please note that it is very much a work in progress, and is undergoing active development, but at this point it is designed to be a high level tool that sends out and tracks tasks from a central origin server.  Said tasks can be set up to be parallel or serial tasks, depending on the need and design.

### Terminology

The host that submits the jobs is referred to as the **origin**.  All nodes or computers that receive and process jobs, *or* that relay job to a computing node, are referred to as **destinations**.

The process of sending a job to a destination node, cluster, or computer is called a **phone call** in the code, likewise, copying back data from a destination is a **return phone call**.

If a job is sent to a single node or server, that is the **single-node-SSH** command.

If a job is sent to a HPC cluster *not* using LSF or qsub, that is the **clusterSSH** command

If a job is sent to a HPC cluster that uses LSF, that is the **clusterLSF** command.

If a job is sent to a HPC cluster that uses qsub, that is the **qsubSSH** command.

### Usage
*as of current build 1*

Note: The home directory for the origin server must be manually modified; a setup script is in development for the next version.

Setup: modify the PATH for the origin server as necessary.  It is *highly* recommended that a subdirectory inside of ~/Documents/ is created for this use, and the directory is added to the python path.

Use: invoke with *python roo.py -a OPTION1 -f FILE1 -i FILE2*

Where:
OPTION1 is one of: 

check (checks a job that is running), start (starts a new job), restart (restarts a new job), stop (stops a job that is running)

FILE1 is a command file that follows this [format](https://github.com/disulfidebond/ROO/blob/master/commandFileTemplate.txt).

FILE2 is an input file to run the command entered, if it is required.


### Example

python roo.py -a start -f [exampleCommandFile.txt](https://github.com/disulfidebond/ROO/blob/master/commandFileTemplateExample.txt) -i fastaFile.fasta


### Setup and Detailed Explanation

The following files must be modified prior to use for all jobs:

[job_task.txt](https://github.com/disulfidebond/ROO/blob/master/job_task.txt)
[copy_phone_directory.sh](https://github.com/disulfidebond/ROO/blob/master/copy_phone_directory.sh)

The following files must be modified depending on the type of job:

qsubSSH:

[getjobNumber_qsubSSH.sh](https://github.com/disulfidebond/ROO/blob/master/getjobnumber_qsubSSH.sh)
[make_phone_call_qsubSSH](https://github.com/disulfidebond/ROO/blob/master/make_phone_call_qsubSSH.sh) 

clusterSSH:

[phonecall.txt](https://github.com/disulfidebond/ROO/blob/master/phone_call.txt)
[make_phone_call_clusterSSH.sh](https://github.com/disulfidebond/ROO/blob/master/make_phone_call_clusterSSH.sh)

###### When a job is started using clusterSSH:
    
    1) jobdata is sourced to add any necessary variables to the environment
    2) The job number is created from a number provided in 'n_ct', and incremented for each subsequent task in the input file
    3) The file 'longdistancecall' is created, which is the file that will start the analysis inside the cluster, and modifies the 'phonecall' file to have the appropriate variables.
    4) next, a text file is created with a hash string and the job number to uniquely identify the job
    5) copy_phone_directory copies the above contents to the destination that was specified
    6) make_phone_call does the following:
       a) make_phone_call uses SSH to launch the longdistancecall file on the destination
       b) longdistancecall has an SSH command to start the phonecall command, usually on a specified worker node
       c) phonecall runs the specified commands, 
       d) phonecall either stops and waits, or reads the file returnphonecall for the origin SSH information and uses scp to copy the results back to the origin

###### When a job is started using qsubSSH:

     1) jobdata is sourced to add any necessary variables to the environment
     2) The job number is created from a number provided in 'n_ct', and incremented for each subsequent task in the input file
     3) The file phonecall is created (NOTE this is different than clusterSSH).  The phonecall file will create a pbs file at the destination with all of the required values to submit the job to qsub
     4) next, a text file is created with a hash string and the job number to uniquely identify the job
     5) copy_phone_directory copies the above contents to the destination that was specified
     6) make_phone_call does the following:
       a) make_phone_call uses SSH to launch phonecall on the destination
       b) phonecall creates the pbs file, submits the job, and collects the job number in a log file
       c) getjobNumber_qsubSSH retrieves the job number from the destination so the job can be checked later
       d) when the job is completed, it is retrieved

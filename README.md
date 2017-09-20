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


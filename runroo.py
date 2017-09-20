#!/usr/bin/python

import argparse
import sys
from runroo import clusterSSH
from runroo import qsubSSH


def formatCommandClusterSSH(c_dict, l):
    if 'n_ct' in c_dict:
        t = c_dict['n_ct']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline, command \'n_ct\' not found')
        sys.exit()
    if 'node' in c_dict:
        t = c_dict['node']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline , command \'node\' not found')
    if 'nodeNM' in c_dict:
        t = c_dict['nodeNM']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline , command \'nodeNM\' not found')
    return l

def formatCommandQsubSSH(c_dict, l):
    if 'n_ct' in c_dict:
        t = c_dict['n_ct']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline, command \'n_ct\' not found')
        sys.exit()
    if 'allocationName' in c_dict:
        t = c_dict['allocationName']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline , command \'allocationName\' not found')
    if 'wallTime' in c_dict:
        t = c_dict['wallTime']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline , command \'wallTime\' not found')
    if 'queueName' in c_dict:
        t = c_dict['queueName']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline , command \'queueName\' not found')
    return l

def formatCommandSingleNodeSSH(c_dict, l):
    if 'n_ct' in c_dict:
        t = c_dict['n_ct']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline, command \'n_ct\' not found')
        sys.exit()
    return l

def formatCommandClusterLSF(c_dict, l):
    if 'n_ct' in c_dict:
        t = c_dict['n_ct']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline, command \'n_ct\' not found')
        sys.exit()
    if 'queueName' in c_dict:
        t = c_dict['queueName']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline, command \'queueName\' not found')
        sys.exit()
    if 'jobName' in c_dict:
        t = c_dict['jobName']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline, command \'jobName\' not found')
        sys.exit()
    if 'projectName' in c_dict:
        t = c_dict['projectName']
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline, command \'projectName\' not found')
        sys.exit()
    if 'wallTime' in c_dict:
        t = c_dict['wallTime'] # format wallTime for LSF as NN not NN:NN:NN
        l.append(t)
    else:
        print('Error, please check the formatting in the Commandline, command \'wallTime\' not found')
        sys.exit()
    return l



def parseSimpleCommandList(s_list):
    listlen = len(s_list)
    ct = 0
    commandsList = []
    while ct < listlen:
        s_list_row = s_list[ct]
        if s_list_row[0] == '#':
            continue
        else:
            commandsList.append(s_list_row)
        ct += 1


def parseComplexCommandList(c_list):
    listlen = len(c_list)
    ct = 0
    commandsList = []
    while ct < listlen:
        c_list_row = c_list[ct]
        c_list_row_items = c_list_row.split(',')
        if len(c_list_row_items) == 1:
            commandsList.append(c_list_row_items)
        else:
            c_list_row_dict = dict()



def inputStartCommandFile(f):
    l = []
    with open(f, 'r') as cF:
        for i in cF:
            i = i.rstrip('\r\n')
            l.append(i)
    return l

def formatDescription():
    print('Options for the command file:')
    print('1) No command file: create a text document with the folowing\n###\nNONE ')
    print('2) Typical commandFile:\n\n###\ninputFile=\n')
    print('3) ###\ncommandFormat= # can be one of: \'clusterSSH, qsubSSH, clusterLSF, single-node-SSH\'\n')
    print('### \n# clusterSSH:')
    print('node=,n_ct=,nodeNM=\'\'')
    print('### \n# qsubSSH:')
    print('n_ct=,allocationName=,wallTime=,queueName=)
    print('###\n clusterLSF:')
    print('n_ct=,queueName=,jobName=,projectName=,wallTime=)
    print('###\n single-node-SSH:')
    print('n_ct=)

def parseStartCommandFile(l):
    lRange = len(l)
    l_1 = l[1]
    parsedCommandList = []
    l1_split = l_1.split('=')
    try:
        tmpVal = l1_split[1]
    except IndexError:
        if l1_split[0] == 'NONE':
            return (0, [])
        else:
            print('Error, check formatting in commandsFile')
            for i in l:
                print(i)
            sys.exit()
    cvalue = ""
    cvalue_list = []
    cvalue_returnList = []
    rowCt = 0
    for i in xrange(0, lRange):
        iRow = l[i]
        if iRow[0] == '#':
            continue
        else: # 'clusterSSH, qsubSSH, clusterLSF, single-node-SSH'
            if rowCt == 0:
                iRow_split = iRow.split('=')
                if iRow_split[1] == 'clusterSSH':
                    cvalue = iRow_split[1]
                elif iRow_split[1] == 'qsubSSH':
                    cvalue = iRow_split[1]
                elif iRow_split[1] == 'clusterLSF':
                    cvalue = iRow_split[1]
                elif iRow_split[1] == 'single-node-SSH':
                    cvalue = iRow_split[1]
                else:
                    print('Error, please check command line of commands File')
                    sys.exit()
                rowCt += 2
            elif rowCt == 2:
                cvalue_tmp = dict()
                iRow_split = iRow_split(',')
                cvalue_list.append(cvalue)
                for v in iRow_split:
                    v_tmp = v.split('=')
                    cvalue_tmp[v_tmp[0]] = v_tmp[1]
                if cvalue == 'clusterSSH': # n_ct, node, nodeNM
                    cvalue_returnList = formatCommandClusterSSH(cvalue_tmp, cvalue_list)
                elif cvalue == 'qsubSSH': # n_ct, allocationName, wallTime, queueName
                    cvalue_returnList = formatCommandQsubSSH(cvalue_tmp, cvalue_list)
                elif cvalue == 'clusterLSF': # n_ct, queueName, jobName, projectName, wallTime
                    cvalue_returnList = formatCommandClusterLSF(cvalue_tmp, cvalue_list)
                elif cvalue == 'single-node-SSH': # n_ct
                    cvalue_returnList = formatCommandSingleNodeSSH(cvalue_tmp, cvalue_list)
                else:
                    print('Error, action command in command file not recognized.')
                    sys.exit()
                rowCt += 2
            else:
                continue
    return (1, cvalue_returnList)





def main():
    parser = argparse.ArgumentParser(description='Remote Organizational and Operational Tool: Root')
    parser.add_argument('-a', '--action', choices=['check', 'start', 'stop', 'restart'], help='check monitors a run in progress, start begins a new run, stop halts a run, restart restarts a previously stopped run')
    parser.add_argument('-i', '--inputFile', help='input file, its use is dependent on the action.  Ignored for \'check\' and \'stop\' actions.')
    parser.add_argument('-f', '--commandfile', help='file with formatted commands for the desired action.  Note that this is REQUIRED, even if commandline arguments will be provided.')
    parser.add_argument('-c', '--commandline', help='commandline arguments added directly to the program, not recommended.')
    parser.add_argument('-s', '--show', help='show format description for command file')
    args = parser.parse_args()

    if args.show:
        formatDescription()
        sys.exit()

    if args.action == 'check':
        # code stub, implementation incomplete
        print(args.action)
        sys.exit()
        if not args.commandfile:
            print('No command file found, hope you know what you\'re doing!  Attempting to monitor run with the provided parameters')
        else:
            print('Checking command file before proceeding.')
            cFile = inputStartCommandFile(args.commandfile)
            checkRes = parseStartCommandFile(cFile)
            if checkRes == 1:
                #
            else:
                # proceed with no commandsFile
    elif args.action == 'stop':
        # code stub, implementation incomplete
        print(args.action)
        sys.exit()
        if not args.commandfile:
            print('No command file found, hope you know what you\'re doing!  Attempting to halt run with the provided parameters')
        else:
            print('Checking command file before proceeding.')
            cFile = inputStartCommandFile(args.commandfile)
            checkRes = parseStartCommandFile(cFile)
            if checkRes[0] == 1:
                #
            else:
                # proceed with no commandsFile
    elif args.action == 'restart':
        # code stub, implementation incomplete
        print(args.action)
        sys.exit()
        if not args.commandFile:
            print('No command file has been found, and a command file is required for the restart action.  If you are ABSOLUTELY sure that you do not want to use a command file, create a text file with ####\nNONE as the command file.')
            sys.exit()
        else:
            print('Using command file ')
            print(args.commandFile)
            cFile = inputStartCommandFile(args.commandfile)
            checkRes = parseStartCommandFile(cFile)
            if not args.inputFile:
                print('No input file found, please check settings.')
                sys.exit()
            else:
                print('Using input file ')
                print(args.inputFile)
        if checkRes[0] == 1:
            #
        elif args.commandline:
            #
        else:
            print('Sorry, the command file was not read, and commands were not readable via commandline.  Please chack the formatting and retry.\n\nNote that a command file will always be checked first, and to force commandline use you must add the line\n\n ###\nNONE \n\n to a command file')
            sys.exit()
    elif args.action == 'start':
        if not args.commandFile:
            print('No command file has been found, and a command file is required for the start action.  If you are ABSOLUTELY sure that you do not want to use a command file, create a text file with ####\nNONE as the command file.')
            sys.exit()
        else:
            print('Using command file ')
            print(args.commandFile)
            print('for start action')
            cFile = inputStartCommandFile(args.commandfile)
            checkRes = parseStartCommandFile(cFile)
            if not args.inputFile:
                print('No input file found, please check settings.')
                sys.exit()
            else:
                print('Using input file ')
                print(args.inputFile)
                print('for start action')
        if checkRes[0] == 1:
            args4Commands = checkRes[0]
            if args4Commands[0] == 'clusterSSH':
                clusterSSH(args.inputFile, args4Commands[1], args4Commands[2],args4Commands[3])
            elif args4Commands[0] == 'qsubSSH':
                qsubSSH(args.inputFile, args4Commands[1], args4Commands[2], args4Commands[3], args4Commands[4])
            elif args4Commands[0] == 'clusterLSF':
                print('Not implemented yet')
                sys.exit()
                clusterLSF(args.inputFile, args4Commands[1], args4Commands[2], args4Commands[3], args4Commands[4], args4Commands[5])
            elif args4Commands[0] == 'single-node-SSH':
                print('Not implemented yet')
                sys.exit()
                singleNodeSSH(args.inputFile, args4Commands[1])
        elif args.commandline:
            # parse arguments, determine action type, and start action
        else:
            print('Sorry, the command file was not read, and commands were not readable via commandline.  Please chack the formatting and retry.\n\nNote that a command file will always be checked first, and to force commandline use you must add the line\n\n ###\nNONE \n\n to a command file')
            sys.exit()
    else:
        print('error, unrecognized input!')
        sys.exit()

if __name__ == "__main__":
    main()

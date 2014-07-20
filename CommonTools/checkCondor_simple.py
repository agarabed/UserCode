#!/usr/bin/python

import os
import re
import sys
import fileinput
import getopt

count = 0

import subprocess

if len(sys.argv)>1: verbose = bool(int(sys.argv[1]))
else: verbose = bool(0)

if len(sys.argv)>2: name = sys.argv[2]
else: name = 'agarabed'

def printCluster(c, prevClust):
    print "cluster ", prevClust, " : ", c['J']," jobs; ",c['C'], " completed, ",c['I'], " idle, ",c['R'], " running, ",c['H'], " held, ",c['S'], " suspended"

def zeroCount(c):
    c['J'] = 0
    c['C'] = 0
    c['R'] = 0
    c['I'] = 0
    c['R'] = 0
    c['H'] = 0
    c['S'] = 0

p = subprocess.Popen(['condor_q', name], stdout=subprocess.PIPE)
result = p.communicate()[0]

prevClust = -1
statusCount = {'J': 0, 'C': 0, 'R': 0, 'I': 0, 'H': 0, 'S': 0}
for line in result.splitlines():
    if line.find(name)>0:
	cluster = line.split('.')[0]
	status = line.split()[5]
	#print cluster, status, statusCount[status]
	if (cluster!=prevClust):
	   if (prevClust!=-1):
	       if verbose: printCluster(statusCount, prevClust) 
	       zeroCount(statusCount)
	   prevClust=cluster
	statusCount['J']+=1
	statusCount[status]+=1
	

printCluster(statusCount, prevClust)
print result.splitlines()[len(result.splitlines())-1]

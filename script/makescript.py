#!/usr/bin/python3

import codemapping
import datetime
import printutil
import os

LIBDIR = os.getcwd() + '/lib_script/'
LIBPREFILES = ['lib_xml.inc', 'lib_encode.inc', 'lib_preprocess.inc']
LIBPOSTFILE = ['lib_postprocess.inc']

def readLibScript(fileList):
	fullString = ''
	for libFile in fileList:
		with open(LIBDIR + libFile, 'r') as f:
			data = ''.join([line for line in f.readlines() if line[0] != '#'])
			fullString += data

	return fullString

def mergeScript(document, code, getPwd):
	try:
		dt = datetime.datetime.now()
		libPre = readLibScript(LIBPREFILES)
		libPost = readLibScript(LIBPOSTFILE)
		scriptFileName = "{}/{}_{}.sh".format(getPwd, document['assetSubType'][0], dt.strftime("%Y%m%d%H%M%S"))
		with open(scriptFileName, 'w') as newFile:
			newFile.write('#!/bin/sh\n')
			newFile.write(libPre)
			newFile.write(libPost)

	except Exception as err:
		printutil.printUsage(err)

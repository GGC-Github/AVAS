#!/usr/bin/python3

import codemapping
import datetime
import printutil
import os

LIBDIR = os.path.join(os.getcwd(), 'lib_script')
SCRIPTDIR = os.path.join(os.getcwd(), 'code_script')
LIBPREFILES = ['lib_xml.inc', 'lib_encode.inc', 'lib_preprocess.inc']
LIBPOSTFILE = ['lib_postprocess.inc']

def readScript(baseFileList, baseDir, codeMap = None):
	fullString = ''
	for baseFile in baseFileList:
		if codeMap is None:
			fullFilePath = os.path.join(baseDir, baseFile)
		else:
			fullFilePath = os.path.join(baseDir, codeMap[baseFile])
		with open(fullFilePath, 'r') as f:
			data = ''.join([line for line in f.readlines() if line[0] != '#'])
			fullString += data

	return fullString

def mergeScript(document, code, getPwd):
	dt = datetime.datetime.now()
	assetType = document['assetType'][0]
	assetSubType = document['assetSubType'][0].lower()
	CODEDIR = os.path.join(SCRIPTDIR, assetType, assetSubType)
	codeMap = getattr(codemapping, assetSubType + 'CodeMap')

	libPre = readScript(LIBPREFILES, LIBDIR)
	libPost = readScript(LIBPOSTFILE, LIBDIR)
	codeScript = readScript(code, CODEDIR, codeMap)
	scriptFileName = "{}/{}_{}.sh".format(getPwd, document['assetSubType'][0], dt.strftime("%Y%m%d%H%M%S"))
	with open(scriptFileName, 'w') as newFile:
		newFile.write('#!/bin/sh\n')
		newFile.write(libPre)
		newFile.write(codeScript)
		newFile.write(libPost)

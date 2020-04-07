#!/usr/bin/env python3
import os
import datetime
import base64
import yaml
import xml.etree.ElementTree as useXmlParser 
import codemapping
import re
import operator

LIBDIR = os.path.join(os.getcwd(), 'lib_script')
SCRIPTDIR = os.path.join(os.getcwd(), 'code_script')
LIBPREFILES = ['lib_preprocess.inc', 'lib_xml.inc', 'lib_encode.inc']
LIBAUTOFILES = ['lib_autostruct.inc']
LIBPOSTFILE = ['lib_postprocess.inc']
OPS = {
	'<': operator.lt,
	'<=': operator.le,
	'==': operator.eq,
	'!=': operator.ne,
	'>=': operator.ge,
	'>': operator.gt
}

def base64Decode(setString):
	return str(base64.b64decode(setString), encoding='utf-8')

def xmlResultFileParser(resultFile):
	print(resultFile)
	doc = useXmlParser.parse(resultFile)
	root = doc.getroot()
	sysInfo = { info.tag:base64Decode(info.text) if info.tag in\
				['processInfo' ,'portInfo' ,'systemctlInfo'] else info.text\
				for info in root.find("sysInfo").getchildren() }
	infoCollectList = {}
	fileCollectList = {}

	infoElementList = root.findall("infoElement")
	for infoElement in infoElementList:
		infoCollectList.update( { infoElement.attrib['code'] :\
								{ data.attrib['name'] : base64Decode(data.text)\
								for data in infoElement if data.tag in 'command' } } )

	fileList = root.findall("fileList/fileInfo")
	for fileElement in fileList:
		fileCollectList.update( {fileElement.find('filePath').text :\
								{ data.tag:base64Decode(data.text) \
								if data.tag == 'fileData' else data.text\
								for data in fileElement.getchildren()\
								if data.tag != 'filePath'}})

	return fileCollectList, infoCollectList, sysInfo

def codeParser(codeList):
	totalList = []
	for code in codeList:
		reg = re.findall(r'(\w+)-(\w+)', code)
		if len(reg) == 0 or (len(reg) == 1 and '~' in code):
			return None

		if len(reg) == 2:
			listTmp = ["{}-{:02}".format(reg[0][0], x) for x in range(int(reg[0][1]),\
						int(reg[1][1]) + 1)]
			totalList.extend(listTmp)
		elif len(reg) == 1 and reg[0][1].lower() == 'all':
			totalList = ["{}-{:02}".format(reg[0][0], x) for x in range(1, 73 + 1)]
			break
		else:
			if isinstance(code, list):
				totalList.extend(code)
			else:
				totalList.append(code)
	totalList = list(set(totalList))
	totalList.sort()
	return totalList

def readScript(baseFileList, baseDir, codeMap = None):
	fullString = ''
	for baseFile in baseFileList:
		if codeMap is None:
			fullFilePath = os.path.join(baseDir, baseFile)
		else:
			fullFilePath = os.path.join(baseDir, codeMap[baseFile][0])
		with open(fullFilePath, 'r', encoding='UTF-8') as f:
			data = ''.join([line for line in f.readlines() if line[0] != '#'])
			fullString += data

	return fullString

def mergeScript(document, code, getPwd):
	dt = datetime.datetime.now()
	assetType = document['assetType'][0]
	assetSubType = document['assetSubType'][0].lower()
	CODEDIR = os.path.join(SCRIPTDIR, assetType, assetSubType)
	codeMap = getattr(codemapping, assetSubType + code[0][0] + 'codeMap')

	libPre = readScript(LIBPREFILES, LIBDIR)
	libPost = readScript(LIBPOSTFILE, LIBDIR)
	libAutoStruct = readScript(LIBAUTOFILES, LIBDIR)
	codeScript = readScript(code, CODEDIR, codeMap)
	scriptFileName = "{}/{}_{}.sh".format(getPwd, document['assetSubType'][0],\
					dt.strftime("%Y%m%d%H%M%S"))
	with open(scriptFileName, 'w', encoding='UTF-8') as newFile:
		newFile.write('#!/bin/sh\n')
		newFile.write(libPre)
		newFile.write(codeScript)
		newFile.write(libAutoStruct)
		for codekey in code:
			newFile.write(codeMap[codekey][1] + '\n')
		newFile.write(libPost)
	
	os.chmod(scriptFileName, 0o755)

def printUsage(strVal):
	print("""
{}
[Usage]
====================
assetInfo:
    assetType:
        - OS
    assetSubType:
        - LINUX
    assetCode:
        - U-01 ~ U-10
        - U-11 ~ U-20
        - U-21 ~ U-30
	""".format(strVal))

def readConfig(name):
	document = yaml.load(open("AVAS.yaml", 'r', encoding='UTF-8'), Loader=yaml.SafeLoader)
	doc = document['assetInfo']
	print("""
***** Current Configration File Settings *****

TYPE : {}
SUBTYPE : {}
CODE : {}

**********************************************
	""".format(doc['assetType'], doc['assetSubType'], doc['assetCode']))
	return doc

def fileStatSetup(setString):	
	data = "[ 권한 = {}({}), 소유자 = {}({}), 소유그룹 = {}({}) ]".format(\
			setString[0], setString[1], setString[5], setString[6],\
			setString[7], setString[8])
	return data

import yaml
import datetime
import os
import stat
import re
from plugins import PluginCollection


def readConfig(confPath):
	document = yaml.load(open(confPath, 'r', encoding='UTF-8'), Loader=yaml.SafeLoader)
	doc = document['assetInfo']
	print(f"""
... Current Configuration File Settings
TYPE : {doc['assetType']}, SUBTYPE : {doc['assetSubType']}, CODE : {doc['assetCode']}
	""")
	return doc


def codeParser(assetType, assetSubType, codeList):
	totalList = []
	for code in codeList:
		reg = re.findall(r'(\w+)-(\w+)', code)

		if reg[0][1].lower() == 'all':
			pluginModules = PluginCollection(assetType, assetSubType, reg[0][0]).plugins
			totalList += pluginModules
		elif len(reg) == 2:
			lenNum = len(reg[0][1])
			tmpList = [f'{reg[0][0]}-{x:{lenNum}}' for x in range(int(reg[0][1]), int(reg[1][1]) + 1)]
			totalList += tmpList
		else:
			totalList.append(code)

	totalList = list(set(totalList))
	totalList.sort()
	return totalList


def readScript(baseFileList, baseDir):
	fullString = ''
	for baseFile in baseFileList:
		fullFilePath = os.path.join(baseDir, baseFile)
		with open(fullFilePath, 'r', encoding='UTF-8') as f:
			data = ''.join([line for line in f.readlines() if line[0] != '#' if not line.startswith('::')])
			fullString += data + '\n'

	return fullString


def mergeScript(document, plugins, getPwd):
	dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

	assetType = document['assetType'][0]
	assetSubType = document['assetSubType'][0]

	libList = {
		'batch': ['@echo off\n', 'bat', f'set ASSETTYPE={assetType}', f'set ASSETSUBTYPE={assetSubType}'],
		'shell': ['#!/bin/sh\n', 'sh', f'ASSETTYPE="{assetType}"', f'ASSETSUBTYPE="{assetSubType}"']
	}
	libName = 'batch' if assetType.lower() == 'windows' else 'shell'
	FILEHEADER = libList[libName][0]
	FILEEXT = libList[libName][1]

	LIBDIR = os.path.join(getPwd, 'LibScript', libName)

	LIBPRE = readScript([f'lib_{libName}_preprocess.inc'], LIBDIR)
	ASSETINFO = f'{libList[libName][2]}\n{libList[libName][3]}\n'
	LIBAUTO = readScript([f'lib_{libName}_autostruct.inc'], LIBDIR)

	code_script = [data.getScript() for data in plugins]
	code_funcList = [data.getScriptExcute() for data in plugins]
	if libName == 'batch':
		SCRIPTMID = LIBAUTO + '\n'.join(code_funcList) + '\n'.join(code_script)
	else:
		LIBXML = readScript(['lib_shell_xml.inc', 'lib_shell_encode.inc'], LIBDIR)
		SCRIPTMID = LIBXML + '\n'.join(code_script) + LIBAUTO + '\n'.join(code_funcList)

	LIBPOST = readScript([f'lib_{libName}_postprocess.inc'], LIBDIR)

	NEWSCRIPTFILE = os.path.join(getPwd, f'{assetType.lower()}_{assetSubType.lower()}_{dt}.{FILEEXT}')
	with open(NEWSCRIPTFILE, 'w', encoding='UTF-8', newline='\n') as newFile:
		newFile.write(FILEHEADER)
		newFile.write(LIBPRE)
		newFile.write(ASSETINFO)
		newFile.write(SCRIPTMID)
		newFile.write(LIBPOST)
	os.chmod(NEWSCRIPTFILE, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

	return NEWSCRIPTFILE

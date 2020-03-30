#!/usr/bin/env python3
import os
import traceback
import xml.etree.ElementTree as ET 
import base64

fileCollectList = {}
sysInfo = {}

def base64Decode(setString):
	return str(base64.b64decode(setString), encoding='utf-8')

def xmlResultFileParser(resultFile):
	global fileCollectList
	global sysInfo
	print(resultFile)
	doc = ET.parse(resultFile)
	root = doc.getroot()
	sysInfo = { info.tag:info.text if info.tag != 'processInfo' and info.tag != 'portInfo' else base64Decode(info.text) for info in root.find("sysInfo").getchildren() }
	infoElementList = root.find("infoElementList").getchildren()
	commandList = root.find("dataElementList/commandList").getchildren()

	fileList = root.findall("dataElementList/fileList/fileInfo")
	for fileElement in fileList:
		fileCollectList.update( {fileElement.find('filePath').text : { data.tag:base64Decode(data.text) if data.tag == 'fileData' else data.text for data in fileElement.getchildren() if data.tag != 'filePath'}})
	
	return None

def main():
	global fileCollectList
	global sysInfo
	print('[ Start Analysis Module ]\n')
	dirName = 'inputResult'
	getPwd = os.getcwd()
	fullPath = os.path.join(getPwd, dirName)
	try:
		print('Input Result Collection XML File Directory : ' + fullPath + '\n')
		fullFileList = os.listdir(fullPath)
		print('[ Result File List ]\n')
		for resultFile in fullFileList:
			code = xmlResultFileParser(os.path.join(fullPath, resultFile))
			print(code)
			fileCollectList.clear()
			sysInfo.clear()
			
	except Exception:
		print(traceback.format_exc())

if __name__ == '__main__':
	main()


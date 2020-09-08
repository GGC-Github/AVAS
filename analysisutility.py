import xml.etree.ElementTree as useXmlParser
import base64
from plugins import PluginCollection


def assetDistribution(assetInfo, sysInfo, infoDict, fileDict):
	assetType = assetInfo['assetType']
	assetSubType = assetInfo['assetSubType']
	pluginModules = PluginCollection(assetType, assetSubType, infoDict.keys()).plugins
	analysisRes = []
	for plugin in pluginModules:
		codeChk = plugin.getCode()
		analysisRes.append(plugin.analysisFunc(sysInfo, infoDict[codeChk], fileDict))

	return analysisRes


def base64Decode(setString):
	getString = base64.b64decode(setString)
	try:
		reString = getString.decode("UTF-8")
	except UnicodeDecodeError:
		reString = getString.decode("ANSI")

	return reString.replace('\r', '')


def xmlResultFileParser(resultFile):
	doc = useXmlParser.parse(resultFile)
	root = doc.getroot()
	decodelist = ['ipList', 'processInfo', 'portInfo', 'serviceInfo']

	assetInfo = {data.tag: data.text for data in root.find("assetInfo")}
	sysInfo = {info.tag: base64Decode(info.text) if info.tag in decodelist else info.text for info in
	           root.find("sysInfo")}

	infoCollectDict = {}
	fileCollectDict = {}

	infoElementList = root.findall("infoElement")
	for infoElement in infoElementList:
		tmpList = []
		for data in infoElement:
			if data.tag in 'command':
				tmpList.append({data.attrib['name']: base64Decode(data.text)})
			else:
				tmpList.append(data.text)

		infoCollectDict.update({infoElement.attrib['code']: tmpList})

	fileList = root.findall("fileList/fileInfo")
	for fileElement in fileList:
		fileKey = fileElement.find('filePath').text
		fileCollectDict.update({fileKey: {data.tag: base64Decode(data.text) if data.tag == 'fileData' else data.text for
		                                  data in fileElement if data.tag != 'filePath'}})

	return assetInfo, sysInfo, infoCollectDict, fileCollectDict


def mergeExeclData(setString):
	fullString = ''
	data = ''
	for key, value in setString.items():
		if '_PS' in key:
			data = f'[ {key.split("_")[0]} 프로세스 상태 ]\n'
		elif '_PORT' in key:
			data = f'[ {key.split("_")[0]} 포트 상태 ]\n'
		elif '_SYS' in key:
			data = f'[ {key.split("_")[0]} 서비스 데몬 상태 ]\n'
		elif 'FILEPERM:' in key:
			data = f'파일명 : {key.split("FILEPERM:")[1]}\n'
		elif 'FILEDATA:' in key:
			data = f'파일명 : {key.split("FILEDATA:")[1]}\n'
		elif 'CMD:' in key:
			data = f'[ {key.split("CMD:")[1]} ]\n\n'
		data += f'{value}\n'
		fullString += data
	return fullString

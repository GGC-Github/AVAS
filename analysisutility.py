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
	sysInfo = {info.tag: base64Decode(info.text) if info.tag in decodelist else info.text for info in root.find("sysInfo")}

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

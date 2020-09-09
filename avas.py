import os
import glob
import argparse
import collectutility
import analysisutility
import excelutility
from plugins import PluginCollection


def collectMain():
	fullPath = os.path.join(os.getcwd(), 'AVAS.yaml')
	print(f'Configuration File Path : {fullPath}')
	doc = collectutility.readConfig(fullPath)
	fullCode = collectutility.codeParser(doc['assetType'], doc['assetSubType'], doc['assetCode'])
	pluginModules = PluginCollection(doc['assetType'], doc['assetSubType'], fullCode).plugins
	fileName = collectutility.mergeScript(doc, pluginModules, os.getcwd())
	print(f'Merge Script Finished! {fileName}\n')


def analysisMain():
	fullPath = os.path.join(os.getcwd(), 'InputResult')
	print(f'Input Result Collection XML File Directory : {fullPath}\n')
	resultFileList = glob.glob(f'{fullPath}/*.xml')
	for resultFile in resultFileList:
		filePath = os.path.join(fullPath, resultFile)
		print(f'Collect File : {filePath}')
		assetInfo, sysInfo, infoDict, fileDict = analysisutility.xmlResultFileParser(filePath)
		print('##### Result xml File Parsing Success! #####')
		analysisRes = analysisutility.assetDistribution(assetInfo, sysInfo, infoDict, fileDict)
		excelutility.makeExcelReport(analysisRes, sysInfo)
		print('##### Final Result Report Successfully Created! #####')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog='avas', usage='%(prog)s [ AVAS MOD ] [options]',
		description='Automated Vulnerability Analysis System',
	)
	parser.add_argument('avas_mod', metavar='AVAS MOD', help='collect [ ... ] or analysis [ ... ]')

	args = parser.parse_args()

	print(f'[ Start {args.avas_mod} Module ]\n')
	if args.avas_mod == 'collect':
		collectMain()
	elif args.avas_mod == 'analysis':
		analysisMain()
	else:
		parser.print_help()
	print(f'[ End {args.avas_mod} Module ]')

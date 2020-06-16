#!/usr/bin/env python3
from abc import *
import re
import utility


class analysisBase(metaclass=ABCMeta):
	def __init__(self, code, fileList, infoList, sysList, codeMap):
		self.code = code
		self.fileList = fileList
		self.infoList = infoList
		self.sysList = sysList
		self.stat = {}
		self.fullString = [self.code, '양호', {}, codeMap[self.code][1]]

	@abstractmethod
	def analysisFunc(self):
		pass

	def processCheck(self, getValue):
		keyValue = f'{getValue}_PS'
		self.stat.update({keyValue: f'- Not found {getValue} Process\n'})
		flag = 0
		if 'processInfo' in self.sysList.keys():
			valueStr = ''.join(f'{line}\n' for line in self.sysList['processInfo'].split('\n') if getValue in line)
			if valueStr != '':
				self.stat.update({keyValue: valueStr})
				flag = 1

		return flag

	def portCheck(self, getValue, srvName):
		keyValue = f'{srvName}_PORT'
		self.stat.update({keyValue: f'- Not found {srvName} Port\n'})
		flag = 0
		if 'portInfo' in self.sysList.keys():
			valueStr = ''.join(f'{line}\n' for line in self.sysList['portInfo'].split('\n') if getValue in line)
			if valueStr != '':
				self.stat.update({keyValue: valueStr})
				flag = 1

		return flag

	def serviceCheck(self, getValue, srvName, compValue = None):
		keyValue = f'{srvName}_SYS'
		self.stat.update({keyValue: f'- Not found {srvName} Service\n'})
		flag = 0
		if compValue is None:
			compValue = srvName
		if 'serviceInfo' in self.sysList.keys():
			valueStr = ''.join(f'{line}\n' for line in self.sysList['serviceInfo'].split('\n') for value in getValue if value in line)
			if valueStr != '':
				self.stat.update({keyValue: valueStr})
				if compValue in self.stat[keyValue]:
					flag = 1

		return flag
	
	def fileDataCheck(self, fileName, defaultCnt, parseKey, pattern, confAttr):
		result = defaultCnt
		fileContent = self.fileList[fileName]
		fileKey = f'FILEDATA:{fileName}'
		self.stat.update({fileKey: f'- Not Found {confAttr} Configuration(!)\n'})
		if fileContent is not None:
			com = re.compile(pattern, re.MULTILINE)
			reg = re.findall(com, fileContent['fileData'])
			if reg:
				self.stat.update({fileKey: ''.join(f'{line}\n' for line in reg)})
				if parseKey == 'exist':
					result = 0
				elif parseKey == '!exist':
					self.stat.update({fileKey: self.stat[fileKey].replace('\n', '(!)\n')})
					result = 1

		return result	

	def dataNumGetValue(self, name, pattern, compValue, compType):
		fileKey = f'FILEDATA:{name}'
		result = 0

		com = re.compile(pattern, re.MULTILINE)
		reg = re.findall(com, self.stat[fileKey])
		if reg:
			cmpOper = utility.OPS[compType]
			if not cmpOper(compValue, reg[0]):
				self.stat.update({fileKey: self.stat[fileKey].replace('\n', '(!)\n')})
				result = 1

		return result

	def dataStrGetValue(self, name, pattern, compValue, compType):
		result = 0
		fileKey = f'FILEDATA:{name}'
		com = re.compile(pattern, re.MULTILINE)
		reg = re.findall(com, self.stat[fileKey])
		if reg:
			if compType == '#':
				if compValue in reg[0]:
					result = 1
			elif compType == 'not in':
				if compValue not in reg[0]:
					self.stat.update({fileKey: self.stat[fileKey].replace('\n', '(!)\n')})
					result = 1
			else:
				cmpOper = utility.OPS[compType]
				if cmpOper(compValue, reg[0]):
					self.stat.update({fileKey: self.stat[fileKey].replace('\n', '(!)\n')})
					result = 1

		return result

	def cmdStrGetValue(self, keyName, pattern, infoKey, compType, compValue = None):
		result = 0
		reString = ''
		dataValue = self.infoList[infoKey]
		if dataValue is not None:
			for data in dataValue.splitlines():
				com = re.compile(pattern, re.MULTILINE)
				reg = re.findall(com, data)
				if reg:
					if compType == '#':
						result = 1
					elif compType == 'not in':
						if compValue not in reg[0]:
							result = 1
					elif compType == "|":
						for comp in compValue.split('|'):
							if comp in reg[0]:
								data += '(!)'
								result = 1
					else:
						cmpOper = utility.OPS[compType]
						if cmpOper(compValue, reg[0]):
							data += '(!)'
							result = 1
				reString += f'{data}\n'

		self.stat.update({keyName: reString})

		return result

	def fileStatCheck(self, fileName, compPerm, compOwner, compType):
		cmpOper = utility.OPS[compType]
		fileKey = f'FILEPERM:{fileName}'
		if 'fileRealStat' in self.fileList[fileName].keys():
			fileStat = self.fileList[fileName]['fileRealStat'].split('|')
			self.stat.update({fileKey: utility.fileStatSetup(fileStat)})
			self.stat.update({fileKey: utility.fileStatSetup(self.fileList[fileName]['fileStat'].split('|'))})
		else:
			fileStat = self.fileList[fileName]['fileStat'].split('|')
			self.stat.update({fileKey: utility.fileStatSetup(fileStat)})

		# 파일 또는 디렉터리에 권한이 없을 시에 0으로 들어오는 값 수정
		filePerm = fileStat[1] if fileStat[1] != '0' else '0' * len(compPerm)
		fileOwner = fileStat[5]
		permBool = True
		ownerBool = True
		resultBool = False

		if compPerm is not None:
			for i in range(0, len(filePerm)):
				if not cmpOper(filePerm[i], compPerm[i]):
					permBool = False
					break

		if compOwner is not None:
			if fileOwner != compOwner:
				ownerBool = False

		if permBool and ownerBool:
			resultBool = True

		return resultBool
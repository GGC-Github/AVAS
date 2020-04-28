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
		self.fullString = [self.code, 'O', {}, codeMap[self.code][1]]


	@abstractmethod
	def analysisFunc(self):
		pass

	def processCheck(self, getValue):
		keyValue = "{}{}".format(getValue, '_PS')
		self.stat.update( { keyValue : ''.join("- {} Not found Process\n".format(getValue)) })
		flag = 0
		if 'processInfo' in self.sysList.keys():
			valueStr = ''.join("{}\n".format(line)
						for line in self.sysList['processInfo'].split('\n')
						if getValue in line)

			if valueStr != '':
				self.stat.update( { keyValue : valueStr } )
				flag = 1

		return flag

	def portCheck(self, getValue, srvName):
		keyValue = "{}{}".format(srvName, '_PORT')
		self.stat.update( { keyValue : ''.join("- {} Not found Port\n".format(srvName)) })
		flag = 0
		if 'portInfo' in self.sysList.keys():
			valueStr = ''.join("{}\n".format(line)
						for line in self.sysList['portInfo'].split('\n')
						if getValue in line)
			if valueStr != '':
				self.stat.update( { keyValue : valueStr } )
				flag = 1

		return flag

	def systemctlCheck(self, getValue, srvName):
		keyValue = "{}{}".format(srvName, '_SYS')
		self.stat.update( { keyValue : ''.join("- {} Not found Service\n".format(srvName)) })
		flag = 0
		if 'systemctlInfo' in self.sysList.keys():
			valueStr = ''.join("{}\n".format(line)
						for line in self.sysList['systemctlInfo'].split('\n')
						for value in getValue
						if value in line)
			if valueStr != '':
				self.stat.update( { keyValue : valueStr } )
				if 'loaded active' in self.stat[keyValue]:
					flag = 1
		return flag
	
	def fileDataCheck(self, fileName, defaultCnt, parseKey, pattern, confAttr):
		result = defaultCnt
		fileContent = self.fileList[fileName]
		fileKey = "{}{}".format('FILEDATA:', fileName)
		self.stat.update( { fileKey : ''.join("- {} Not Found Configuration(!)\n".format(confAttr))} )
		if fileContent is not None:
			com = re.compile(pattern, re.MULTILINE)
			reg = re.findall(com, fileContent['fileData'])
			if reg:
				self.stat.update( { fileKey : ''.join("{}\n".format(line) for line in reg) } )
				if parseKey == 'exist':
					result = 0
				elif parseKey == '!exist':
					self.stat.update( { fileKey : self.stat[fileKey].replace('\n', '(!)\n') } )
					result = 1

		return result	

	def dataNumGetValue(self, name, pattern, compValue, compType):
		fileKey = "{}{}".format('FILEDATA:', name)
		result = 0
		com = re.compile(pattern, re.MULTILINE)
		reg = re.findall(com, self.stat[fileKey])

		if compType == '<':
			if reg and int(reg[0]) < compValue:
				self.stat.update( { fileKey : self.stat[fileKey].replace('\n', '(!)\n') } )
				result = 1
		elif compType == '>':
			if reg and int(reg[0]) > compValue:
				self.stat.update( { fileKey : self.stat[fileKey].replace('\n', '(!)\n') } )
				result = 1
		elif compType == '=':
			if reg and int(reg[0]) == compValue:
				self.stat.update( { fileKey : self.stat[fileKey].replace('\n', '(!)\n') } )
				result = 1

		return result

	def dataStrGetValue(self, name, pattern, compValue, compType):
		result = 0
		fileKey = "{}{}".format('FILEDATA:', name)
		com = re.compile(pattern, re.MULTILINE)
		reg = re.findall(com, self.stat[fileKey])
		if reg:
			if compType == '!':
				if  compValue not in reg[0]:
					self.stat.update( { fileKey : self.stat[fileKey].replace('\n', '(!)\n') } )
					result = 1
			elif compType == '=':
				if compValue in reg[0]:
					self.stat.update( { fileKey : self.stat[fileKey].replace('\n', '(!)\n') } )
					result = 1

		return result

	def fileStatCheck(self, fileName, compPerm, compOwner, compType):
		cmpOper = utility.OPS[compType]
		fileKey = "{}{}".format('FILEPERM:', fileName)
		if 'fileRealStat' in self.fileList[fileName].keys():
			fileStat = self.fileList[fileName]['fileRealStat'].split('|')
			self.stat.update( { fileKey : utility.fileStatSetup(fileStat) } )
			self.stat.update( { fileKey : utility.fileStatSetup(
											self.fileList[fileName]['fileStat']
											.split('|')) } )
		else:
			fileStat = self.fileList[fileName]['fileStat'].split('|')
			self.stat.update( { fileKey : utility.fileStatSetup(fileStat) } )

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
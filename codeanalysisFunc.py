#!/usr/bin/env python3
from abc import *

class analysisBase(metaclass=ABCMeta):
	def __init__(self, code, fileList, infoList, sysList):
		self.code = code
		self.fileList = fileList
		self.infoList = infoList
		self.sysList = sysList

	@abstractmethod
	def analysisFunc(self):
		pass

class analysislinux001(analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '양호']
		stat = {}
		stat.update( { 'process' : ''.join("{}\n".format(line) \
						for line in self.sysList['processInfo'].split('\n') \
						if 'sshd' in line) } )
		stat.update( { 'port' : ''.join("{}\n".format(line) \
						for line in self.sysList['portInfo'].split('\n') \
						if ':22' in line) } )
		stat.update( { 'systemctl' : ''.join("{}\n".format(line) \
						for line in self.sysList['systemctlInfo'].split('\n') \
						if 'ssh.service' in line or 'sshd.service' in line) } )

		if stat['process'] != '' or stat['port'] != '' or ( stat['systemctl'] != '' and 'loaded active' in stat['systemctl']):
			fileContent = self.fileList['/etc/ssh/sshd_config']
			if fileContent is not None:
				if 'PermitRootLogin' in fileContent['fileData']:
					stat.update( { '/etc/ssh/sshd_config' : ''.join("{}\n".format(line) \
								for line in fileContent['fileData'].split('\n') \
								if 'PermitRootLogin' in line) } )
					if not 'no' in stat['/etc/ssh/sshd_config'].lstrip('PermitRootLogin').lower():
						fullString[1] = '취약'
				else:
					stat.update( { '/etc/ssh/sshd_config' : 'Not Found PermitRootLogin' } )
			else:
				stat.update( { '/etc/ssh/sshd_config' : 'Not Found ConfigurationFile' } )
		
		fullString.append(stat)
		return fullString
			
class analysislinux003(analysisBase):
	def analysisFunc(self):
		return None

class analysislinux007(analysisBase):
	def analysisFunc(self):
		return None

class analysislinux008(analysisBase):
	def analysisFunc(self):
		return None

class analysislinux031(analysisBase):
	def analysisFunc(self):
		return None

class analysislinux032(analysisBase):
	def analysisFunc(self):
		return None

class analysislinux042(analysisBase):
	def analysisFunc(self):
		return None

class analysislinux043(analysisBase):
	def analysisFunc(self):
		return None


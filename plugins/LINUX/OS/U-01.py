from plugins import Plugin


class linuxosu01(Plugin):
	def __init__(self):
		super().__init__()
		self.code = "U-01"
		self.codeScript = """
linux001() {
	code=$1
	xml_infoElement_tag_start "$code"

	xml_fileInfo_write "/etc/ssh/sshd_config"
	xml_fileInfo_write "/etc/pam.d/remote"
	xml_fileInfo_write "/etc/pam.d/login"
	xml_fileInfo_write "/etc/securetty"

	xml_infoElement_tag_end "$code"
}
		"""
		self.codeExcute = "linux001 U-01"
		self.description = {
			'Category': '계정 관리',
			'Name': 'root 계정 원격 접속 제한',
			'Important': '상',
			'ImportantScore': '3',
			'Criterion': '양호 : 원격 터미널 서비스를 사용하지 않거나, 사용 시 root 직접 접속을 차단한 경우\n'
			'취약 : 원격 터미널 서비스 사용 시 root 직접 접속을 허용한 경우',
			'ActionPlan': '원격 접속 시 root 계정으로 바로 접속 할 수 없도록 설정파일 수정'
		}
		self.fullString = [self.code, '양호', self.stat, self.description]

	def analysisFunc(self, sysInfo, infoDict, fileDict):
		chkServiceDict = {
			'ssh': [':22', ['ssh.service, sshd.service'], 'sshd_config'],
			'telnet': [':23', ['telnet.service', 'telnetd.service'], ['/etc/pam.d/remote', '/etc/pam.d/login'], '/etc/securetty']
		}
		vulCnt = 0
		for service in chkServiceDict.keys():
			chkNum = 0
			chkNum += self.processCheck(sysInfo, service)
			chkNum += self.portCheck(sysInfo, chkServiceDict[service][0], service)
			chkNum += self.serviceCheck(sysInfo, chkServiceDict[service][1], service, 'loaded active')
			if chkNum > 0:
				if 'ssh' == service:
					chkFlag, dictKey = self.getFileName(infoDict, fileDict, chkServiceDict[service][2])
					if chkFlag:
						if self.getConfig(dictKey, '^[\t ]*PermitRootLogin\\s\\S+$', 'PermitRootLogin', 'exist'):
							vulCnt += self.compStrValue(dictKey, '^[\t ]*PermitRootLogin\\s(\\S+)$', 'no', '==')
						else:
							self.stat.update({dictKey: self.stat[dictKey].replace('(!)\n', '\n')})
							vulCnt += 1
				else:
					for file in chkServiceDict[service][2]:
						chkFlag, dictKey = self.getFileName(infoDict, fileDict, file)
						if chkFlag:
							if self.getConfig(dictKey, '^[\t ]*auth\\s.*pam_securetty\\.so', 'pam_securetty.so', 'exist'):
								chkFlag, fileKey = self.getFileName(infoDict, fileDict, chkServiceDict[service][3])
								if chkFlag:
									if self.getConfig(fileKey, '^[\t ]*pts\\s+', 'pts', '!exist'):
										vulCnt += 1
										break
			else:
				vulCnt += 1

		if vulCnt < 2:
			self.fullString[1] = '취약'
		return self.fullString

from plugins import Plugin


class linuxosu31(Plugin):
	def __init__(self):
		super().__init__()
		self.code = "U-31"
		self.codeScript = """
linux031() {
	code=$1
	xml_infoElement_tag_start "$code"

	xml_fileInfo_write "/etc/sendmail.cf"
	xml_fileInfo_write "/etc/mail/sendmail.cf"

	xml_infoElement_tag_end "$code"
}
		"""
		self.codeExcute = "linux031 U-31"
		self.description = {
			'Category': '서비스 관리',
			'Name': '스팸 메일 릴레이 제한',
			'Important': '상',
			'ImportantScore': '3',
			'Criterion': '양호 : SMTP 서비스를 사용하지 않거나 릴레이 제한이 설정되어 있는 경우\n'
			'취약 : SMTP 서비스를 사용하며 릴레이 제한이 설정되어 있지 않은 경우',
			'ActionPlan': 'Sendmail 서비스를 사용하지 않을 경우 서비스 중지, 사용할 경우 릴레이 방지 설정 또는, 릴레이 대상 접근 제어'
		}
		self.fullString = [self.code, '양호', self.stat, self.description]

	def analysisFunc(self, sysInfo, infoDict, fileDict):
		vulCnt = 0
		chkNum = 0
		chkNum += self.processCheck(sysInfo, 'sendmail')
		chkNum += self.serviceCheck(sysInfo, ['sendmail.service'], 'sendmail', 'loaded active')

		if chkNum > 0:
			chkFlag, dictKey = self.getFileName(infoDict, fileDict, 'sendmail.cf')
			if chkFlag:
				if self.getConfig(dictKey, '^R.*550 Relaying denied.*$', 'Relaying denied', 'exist'):
					vulCnt += 1
		else:
			vulCnt += 1

		if vulCnt == 0:
			self.fullString[1] = '취약'

		return self.fullString

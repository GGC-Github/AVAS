from plugins import Plugin


class linuxosu07(Plugin):
	def __init__(self):
		super().__init__()
		self.code = "U-07"
		self.codeScript = """
linux007() {
	code=$1
	xml_infoElement_tag_start "$code"

	xml_fileInfo_write "/etc/passwd"

	xml_infoElement_tag_end "$code"
}
		"""
		self.codeExecute = "linux007 U-07"
		self.description = {
			'Category': '파일 및 디렉터리 관리',
			'Name': '/etc/passwd 파일 소유자 및 권한 설정',
			'Important': '상',
			'ImportantScore': '3',
			'Criterion': '양호 : /etc/passwd 파일 소유자가 root이고, 권한이 644 이하인 경우\n'
			'취약 : /etc/passwd 파일 소유자가 root가 아니거나, 권한이 644 이하가 아닌 경우',
			'ActionPlan': '/etc/passwd 파일 소유자 및 권한 변경 (소유자 root, 권한 644)'
		}
		self.fullString = [self.code, '양호', self.stat, self.description]

	def analysisFunc(self, sysInfo, infoDict, fileDict):
		reBool = True
		if '/etc/passwd' in fileDict.keys():
			reBool = self.filePermCheck(fileDict, '/etc/passwd', '644', 'root', '<=')
		else:
			self.stat.update({'FILEPERM:/etc/passwd': '- Not Found /etc/passwd File\n'})

		if not reBool:
			self.fullString[1] = '취약'
		return self.fullString

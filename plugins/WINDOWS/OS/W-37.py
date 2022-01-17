from plugins import Plugin


class windowsosw37(Plugin):
	def __init__(self):
		super().__init__()
		self.code = "W-37"
		self.codeScript = """
echo     ^<infoElement code="%CODE037%"^> >> %RESULT_COLLECT_FILE%

cacls %systemroot%\system32\config\SAM  > samperm_tmp.txt
if "%ERRORLEVEL%" == "0" (
    call :base64encode samperm_tmp.txt
    echo         ^<command name="SAM_FILE_PERM"^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
    for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
    echo         ^]^]^>^</command^> >> %RESULT_COLLECT_FILE%
)
if exist samperm_tmp.txt del /q samperm_tmp.txt

echo     ^</infoElement^> >> %RESULT_COLLECT_FILE%

echo %CODE037% Collect
		"""
		self.codeExecute = "set CODE037=W-37"
		self.description = {
			'Category': '보안 관리',
			'Name': 'SAM 파일 접근 통제 설정',
			'Important': '상',
			'ImportantScore': '3',
			'Criterion': '양호 : SAM 파일 접근권한에 Administrator, System 그룹만 모든 권한으로 설정되어 있는 경우\n'
			             '취약 : SAM 파일 접근권한에 Administrator, System 그룹 외 다른 그룹에 권한이 설정되어 있는 경우',
			'ActionPlan': 'SAM 파일 권한 확인 후 Administrator, System 그룹 외 다른 그룹에 설정된 권한 제거'
		}
		self.fullString = [self.code, '양호', self.stat, self.description]

	def analysisFunc(self, sysInfo, infoDict, fileDict):
		vulCnt = 0
		if infoDict:
			if 'SAM_FILE_PERM' in infoDict[0]:
				valueStr = infoDict[0]['SAM_FILE_PERM']
				if valueStr is not None:
					tmpStr = ''
					for data in valueStr.replace('\n\n', '\n').splitlines():
						if 'system:' in data.lower() or 'administrators:' in data.lower():
							tmpStr += data + '\n'
						else:
							tmpStr += data + '(!)\n'
							vulCnt += 1
					self.stat.update({'CMD:SAM 파일 접근 권한': tmpStr})
				else:
					self.stat.update({'CMD:SAM 파일 접근 권한': '- Not Found SAM file Permission Result\n'})
		else:
			self.stat.update({'CMD:SAM 파일 접근 권한': '- Not Found SAM file Permission Result\n'})

		if vulCnt > 0:
			self.fullString[1] = '취약'

		return self.fullString

from plugins import Plugin


class windowsosw40(Plugin):
    def __init__(self):
        super().__init__()
        self.code = "W-40"
        self.codeScript = """
call :xml_infoElement_tag_start %CODE040%

secedit /export /cfg secpolicy_tmp.txt > nul
type secpolicy_tmp.txt | more > secpolicy.txt
del /q secpolicy_tmp.txt

call :fileCheckSum secpolicy.txt, checksumvalue
if "%checksumvalue%" == "DUP" goto END040
call :xml_fileInfo_write secpolicy.txt, %checksumvalue%

:END040
if exist secpolicy.txt del /q secpolicy.txt

call :xml_infoElement_tag_end %CODE040%
"""
        self.codeExecute = "set CODE040=W-40"
        self.description = {
            'Category': '보안 관리',
            'Name': '원격 시스템에서 강제로 시스템 종료',
            'Important': '상',
            'ImportantScore': '3',
            'Criterion': '양호 : 원격 시스템에서 강제로 시스템 종료" 정책에 "Administrators"만 존재하는 경우\n'
                         '취약 : 원격 시스템에서 강제로 시스템 종료" 정책에 "Administrators" 외 다른 계정 및 그룹이 존재하는 경우',
            'ActionPlan': '원격 시스템에서 강제로 시스템 종료 -> Administrators'
        }
        self.fullString = [self.code, '양호', self.stat, self.description]

    def analysisFunc(self, sysInfo, infoDict, fileDict):
        vulCnt = 0
        fileKey = 'FILEDATA:Local Security Policy'

        if 'Local Security Policy' in fileDict.keys():
            self.stat.update({fileKey: fileDict['Local Security Policy']['fileData']})
            if self.getConfig(fileKey, '^SeRemoteShutdownPrivilege.*$', 'SeRemoteShutdownPrivilege', 'exist'):
                vulCnt += self.compStrValue(fileKey, '^SeRemoteShutdownPrivilege[ \t=]*(.*)$', '*S-1-5-32-544', '==')
                self.stat['CMD:SeRemoteShutdownPrivilege 설정 (Local Security Policy)'] = self.stat.pop(
                    'FILEDATA:Local Security Policy')

        if vulCnt == 0:
            self.fullString[1] = '취약'

        return self.fullString

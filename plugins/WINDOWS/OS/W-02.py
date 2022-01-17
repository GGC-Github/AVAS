from plugins import Plugin


class windowsosw02(Plugin):
    def __init__(self):
        super().__init__()
        self.code = "W-02"
        self.codeScript = """
call :xml_infoElement_tag_start %CODE002%

net user guest | findstr /bic:"Account active" > guest_tmp.txt
if "%ERRORLEVEL%" == "0" call :xml_command_write guest_tmp.txt, GUEST_ACCOUNT
if exist guest_tmp.txt del /q guest_tmp.txt

secedit /export /cfg secpolicy_tmp.txt > nul
type secpolicy_tmp.txt | more > secpolicy.txt
del /q secpolicy_tmp.txt

call :fileCheckSum secpolicy.txt, checksumvalue
if "%checksumvalue%" == "DUP" goto END002
call :xml_fileInfo_write secpolicy.txt, %checksumvalue%

:END002
if exist secpolicy.txt del /q secpolicy.txt

call :xml_infoElement_tag_end %CODE002%
"""
        self.codeExecute = "set CODE002=W-02"
        self.description = {
            'Category': '계정 관리',
            'Name': 'Guset 계정 비활성화',
            'Important': '상',
            'ImportantScore': '3',
            'Criterion': '양호 : Guest 계정이 비활성화 되어 있는 경우\n'
            '취약 : Guest 계정이 활성화 되어 있는 경우',
            'ActionPlan': 'Guest 계정 비활성화'
        }
        self.fullString = [self.code, '양호', self.stat, self.description]

    def analysisFunc(self, sysInfo, infoDict, fileDict):
        activeCnt = 0
        keyList = [
            'CMD:Guest 계정 활성화 여부(net user)',
            'CMD:Guest 계정 활성화 여부(Local Security Policy)',
        ]
        if infoDict:
            if 'GUEST_ACCOUNT' in infoDict[0]:
                activeCnt += self.cmdStrGetValue(keyList[0], infoDict[0], 'GUEST_ACCOUNT', '^Account active[ \t]*(\\S+)$', 'Yes', 'in')
        else:
            self.stat.update({keyList[0]: f'- Not Found "net user Guest" Result\n'})

        fileKey = 'FILEDATA:Local Security Policy'
        if 'Local Security Policy' in fileDict.keys():
            self.stat.update({fileKey: fileDict['Local Security Policy']['fileData']})
            if self.getConfig(fileKey, '^EnableGuestAccount.*$', 'EnableGuestAccount', 'exist'):
                activeCnt += self.compStrValue(fileKey, '^EnableGuestAccount[ \t=]*([0-9])$', '0', 'in')
            self.stat[keyList[1]] = self.stat.pop('FILEDATA:Local Security Policy')

        if activeCnt != 2:
            self.fullString[1] = '취약'
        return self.fullString

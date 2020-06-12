#!/usr/bin/env python3
import codeanalysisBase


class analysiswindows001(codeanalysisBase.analysisBase):
    def analysisFunc(self):
        resultCnt = 0
        activeCnt = 0
        keyList= [
            'CMD:Administrator 계정 활성화 여부(net user)',
            'CMD:Administrator 계정 활성화 여부(Local Security Policy)',
            'CMD:Administrator 계정명 변경 여부(Local Security Policy)'
        ]
        if 'ADMIN_ACCOUNT' in self.infoList.keys():
            activeCnt += self.cmdStrGetValue(keyList[0], '^Account active[ \t]*(.*)$', 'ADMIN_ACCOUNT', 'Yes', '#')
        else:
            self.stat.update({keyList[0]: 'Not Found "net user Administrator" Result'})

        if 'Local Security Policy' in self.fileList.keys():
            enableFlag = self.fileDataCheck(
                'Local Security Policy', 1, 'exist', '^EnableAdminAccount.*$', 'EnableAdminAccount')
            if enableFlag == 0:
                activeCnt += self.dataStrGetValue('Local Security Policy', '^EnableAdminAccount[ \t=]*([0-9])$', '1', '#')
                self.stat[keyList[1]] = self.stat.pop('FILEDATA:Local Security Policy')

        if activeCnt > 0:
            newnameFlag = self.fileDataCheck(
                'Local Security Policy', 1, 'exist', '^NewAdministratorName.*$', 'NewAdministratorName')
            if newnameFlag == 0:
                resultCnt = self.dataStrGetValue(
                    'Local Security Policy', '^NewAdministratorName[ \t=]*[\"]*([\\S]+[^\"])[\"]*$', 'Administrator', '=')
                import pdb; pdb.set_trace()
                self.stat[keyList[2]] = self.stat.pop('FILEDATA:Local Security Policy')

        if resultCnt > 0:
            self.fullString[1] = '취약'

        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows002(codeanalysisBase.analysisBase):
    def analysisFunc(self):
        activeCnt = 0
        keyList = [
            'CMD:Guest 계정 활성화 여부(net user)',
            'CMD:Guest 계정 활성화 여부(Local Security Policy)',
        ]
        if 'ADMIN_ACCOUNT' in self.infoList.keys():
            activeCnt += self.cmdStrGetValue(keyList[0], '^Account active[ \t]*(.*)$', 'GUEST_ACCOUNT', 'Yes', '#')
        else:
            self.stat.update({keyList[0]: 'Not Found "net user Guest" Result'})

        if 'Local Security Policy' in self.fileList.keys():
            enableFlag = self.fileDataCheck(
                'Local Security Policy', 1, 'exist', '^EnableGuestAccount.*$', 'EnableGuestAccount')
            if enableFlag == 0:
                activeCnt += self.dataStrGetValue('Local Security Policy', '^EnableGuestAccount[ \t=]*([0-9])$', '1',
                                                  '#')
                self.stat[keyList[1]] = self.stat.pop('FILEDATA:Local Security Policy')

        if activeCnt > 0:
            self.fullString[1] = '취약'
        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows008(codeanalysisBase.analysisBase):
    def analysisFunc(self):
        self.stat.update(
            {"{}{}".format('FILEDATA:', '/etc/ssh/sshd_config'): '- PermitRootLogin Not Found Configuration\n'})
        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows032(codeanalysisBase.analysisBase):
    def analysisFunc(self):
        self.stat.update(
            {"{}{}".format('FILEDATA:', '/etc/ssh/sshd_config'): '- PermitRootLogin Not Found Configuration\n'})
        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows035(codeanalysisBase.analysisBase):
    def analysisFunc(self):
        self.stat.update(
            {"{}{}".format('FILEDATA:', '/etc/ssh/sshd_config'): '- PermitRootLogin Not Found Configuration\n'})
        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows037(codeanalysisBase.analysisBase):
    def analysisFunc(self):
        self.stat.update(
            {"{}{}".format('FILEDATA:', '/etc/ssh/sshd_config'): '- PermitRootLogin Not Found Configuration\n'})
        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows040(codeanalysisBase.analysisBase):
    def analysisFunc(self):
        self.stat.update(
            {"{}{}".format('FILEDATA:', '/etc/ssh/sshd_config'): '- PermitRootLogin Not Found Configuration\n'})
        self.fullString[2] = self.stat
        return self.fullString

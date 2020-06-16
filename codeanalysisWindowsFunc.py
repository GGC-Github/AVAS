#!/usr/bin/env python3
import codeanalysisBase


class analysiswindows001(codeanalysisBase.analysisBase):
    # 2018 W-01 (상)
    # Administrator 계정 이름 바꾸기
    # 양호: Administrator Default 계정 이름을 변경한 경우
    # 취약: Administrator Default 계정 이름을 변경하지 않은 경우
    def analysisFunc(self):
        resultCnt = 0
        activeCnt = 0
        keyList= [
            'CMD:Administrator 계정 활성화 여부(net user)',
            'CMD:Administrator 계정 활성화 여부(Local Security Policy)',
            'CMD:Administrator 계정명 변경 여부(Local Security Policy)'
        ]
        if 'ADMIN_ACCOUNT' in self.infoList.keys():
            activeCnt += self.cmdStrGetValue(keyList[0], '^Account active[ \t]*(Yes)$', 'ADMIN_ACCOUNT', '#')
        else:
            self.stat.update({keyList[0]: f'- Not Found "net user Administrator" Result\n'})

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
                resultCnt = self.dataStrGetValue('Local Security Policy',
                                                 '^NewAdministratorName[ \t=]*[\"]*([\S]+[^\"])[\"]*[\S]$',
                                                 'Administrator', '==')
                self.stat[keyList[2]] = self.stat.pop('FILEDATA:Local Security Policy')

        if resultCnt > 0:
            self.fullString[1] = '취약'

        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows002(codeanalysisBase.analysisBase):
    # 2018 W-02 (상)
    # Guest 계정 상태
    # 양호: Guest 계정이 비활성화 되어 있는 경우
    # 취약: Guest 계정이 활성화 되어 있는 경우
    def analysisFunc(self):
        activeCnt = 0
        keyList = [
            'CMD:Guest 계정 활성화 여부(net user)',
            'CMD:Guest 계정 활성화 여부(Local Security Policy)',
        ]
        if 'GUEST_ACCOUNT' in self.infoList.keys():
            activeCnt += self.cmdStrGetValue(keyList[0], '^Account active[ \t]*(Yes)$', 'GUEST_ACCOUNT', '#')
        else:
            self.stat.update({keyList[0]: f'- Not Found "net user Guest" Result\n'})

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
    # 2018 W-08 (상)
    # 하드디스크 기본 공유 제거
    # 양호: 레지스트리의 AutoShareServer (WinNT: AutoShareWks)가 0이며 기본 공유가 존재하지 않는 경우
    # 취약: 레지스트리의 AutoShareServer (WinNT: AutoShareWks)가 1이거나 기본 공유가 존재하는 경우
    def analysisFunc(self):
        resultCnt = 0
        keyList = {
            'CMD:기본 공유 설정 여부(net share)':
                ['^[\S]+[ \t]+[\S]+[ \t]+(.*)', 'DEFAULT_SHARE', '|', '기본 공유|Default share', 'net share'],
            'CMD:AutoShareServer 레지스트리 설정':
                ['^[ \t]*AutoShareServer.*0x(.)$', 'AUTOSHARE_SERVER_REG', '==', '1', 'reg query AutoShareServer'],
            'CMD:AutoShareWks 레지스트리 설정':
                ['^[ \t]*AutoShareWks.*0x(.)$', 'AUTOSHARE_WKS_REG', '==', '1', 'reg query AutoShareWks']
        }

        for key in keyList.keys():
            if keyList[key][1] in self.infoList.keys():
                resultCnt += self.cmdStrGetValue(key, keyList[key][0], keyList[key][1], keyList[key][2], keyList[key][3])
            else:
                self.stat.update({key: f'- Not Found "{keyList[key][4]}" Result\n'})

        if resultCnt > 0:
            self.fullString[1] = '취약'

        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows032(codeanalysisBase.analysisBase):
    # 2018 W-32 (상)
    # 패치 관리 - 최신 HOT FIX 적용
    # 양호: 최신 Hotfix가 있는지 주기적으로 모니터링하고 반영하거나, PMS (Patch Management System) Agent가 설치되어 자동패치배포가 적용된 경우
    # 취약: 최신 Hotfix가 있는지 주기적으로 모니터 절차가 없거나, 최신 Hotfix를 반영하지 않은 경우, 또한 PMS(Patch Management System)
    #      Agent가 설치되어 있지 않거나, 설치되어 있으나 자동패치 배포가 적용되지 않은 경우
    def analysisFunc(self):
        self.fullString[1] = '리뷰'
        keyList = {
            'WINDOWS_HOTFIX': '현재 적용된 패치',
            'WINDOWS_UPDATE_REG': 'update 설정'
        }

        for key in keyList.keys():
            if key in self.infoList.keys():
                self.stat.update({f'CMD:{keyList[key]}': self.infoList[key]})

        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows035(codeanalysisBase.analysisBase):
    # 2018 W-35 (상)
    # 로그 관리 - 원격으로 액세스 할 수 있는 레지스트리 경로
    # 양호: Remote Registry Service가 중지되어 있는 경우
    # 취약: Remote Registry Service가 사용 중인 경우
    def analysisFunc(self):
        resultCnt = 0
        desStr = """
[참고]
서비스 시작유형(재부팅시 서비스 구동여부)
자동(재부팅시 시작됨)    - 2
수동(재부팅시 수동)      -  3
사용안함(재부팅시 중지됨) -  4
        """
        resultCnt += self.serviceCheck(['Remote Registry'], 'Remote Registry')
        if resultCnt > 0:
            valueStr = self.stat['Remote Registry_SYS'].replace('\n', '')
            self.stat.update({'Remote Registry_SYS': f'{valueStr} Service Running(!)\n'})
        if 'REMOTE_REGISTRY_REG' in self.infoList.keys():
            resultCnt += self.cmdStrGetValue('CMD:Remote Registry 서비스 시작 유형', '^[ \t]*Start.*0x(.)$',
                                             'REMOTE_REGISTRY_REG', '==', '2')
            valueStr = self.stat['CMD:Remote Registry 서비스 시작 유형']
            self.stat.update({'CMD:Remote Registry 서비스 시작 유형': f'{valueStr} {desStr}\n'})
        else:
            self.stat.update({'CMD:Remote Registry 서비스 시작 유형': '- Not Found Remote Registry Start Result\n'})

        if resultCnt > 0:
            self.fullString[1] = '취약'

        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows037(codeanalysisBase.analysisBase):
    # 2018 W-37 (상)
    # 보안 관리 - SAM 파일 접근 통제 설정
    # 양호: SAM 파일 접근권한에 Administrator, System 그룹만 모든 권한으로 설정되어 있는 경우
    # 취약: SAM 파일 접근권한에 Administrator, System 그룹 외 다른 그룹에 권한이 설정되어 있는 경우
    def analysisFunc(self):
        resultCnt = 0
        if 'SAM_FILE_PERM' in self.infoList.keys():
            valueStr = self.infoList['SAM_FILE_PERM']
            if valueStr is not None:
                resultList = ''.join(
                    [data + '\n' if 'system:' in data.lower() or 'administrators:' in data.lower() else data + '(!)\n'
                     for data in valueStr.replace('\n\n', '\n').splitlines()]
                )
                if '(!)' in resultList:
                    resultCnt += 1
                self.stat.update({'CMD:SAM 파일 접근 권한': resultList})
            else:
                self.stat.update({'CMD:SAM 파일 접근 권한': '- Not Found SAM file Permission Result\n'})
        else:
            self.stat.update({'CMD:SAM 파일 접근 권한': '- Not Found SAM file Permission Result\n'})

        if resultCnt > 0:
            self.fullString[1] = '취약'

        self.fullString[2] = self.stat
        return self.fullString


class analysiswindows040(codeanalysisBase.analysisBase):
    # 2018 W-40 (상)
    # 보안 관리 - 원격 시스템에서 강제로 시스템 종료
    # 양호: "원격 시스템에서 강제로 시스템 종료" 정책에 "Administrators"만 존재하는 경우
    # 취약: "원격 시스템에서 강제로 시스템 종료" 정책에 "Administrators"외 다른 계정 및 그룹이 존재하는 경우
    def analysisFunc(self):
        resultCnt = 0
        if 'Local Security Policy' in self.fileList.keys():
            enableFlag = self.fileDataCheck(
                'Local Security Policy', 1, 'exist', '^SeRemoteShutdownPrivilege.*$', 'SeRemoteShutdownPrivilege')
            if enableFlag == 0:
                resultCnt += self.dataStrGetValue('Local Security Policy', '^SeRemoteShutdownPrivilege[ \t=]*(.*)$',
                                                  '*S-1-5-32-544', '!=')
                self.stat['CMD:SeRemoteShutdownPrivilege 설정 (Local Security Policy)'] = \
                    self.stat.pop('FILEDATA:Local Security Policy')

        if resultCnt > 0:
            self.fullString[1] = '취약'

        self.fullString[2] = self.stat
        return self.fullString

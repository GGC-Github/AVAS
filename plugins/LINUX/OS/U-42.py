from plugins import Plugin


class linuxosu42(Plugin):
    def __init__(self):
        super().__init__()
        self.code = "U-42"
        self.codeScript = """
linux042() {
    code=$1
    xml_infoElement_tag_start $code
    
    if [ "$OS_VERSION" != "" ] && [ "$OS_KERNEL_VERSION" != "" ]; then
        xml_command_write "OS_VERSION" "$OS_NAME $OS_VERSION"
        xml_command_write "OS_KERNEL_VERSION" "$OS_KERNEL_VERSION"
    fi

    xml_infoElement_tag_end "$code"
}
        """
        self.codeExecute = "linux042 U-42"
        self.description = {
            'Category': '패치 관리',
            'Name': '최신 보안패치 및 벤더 권고사항 적용',
            'Important': '상',
            'ImportantScore': '3',
            'Criterion': '양호 : 패치 적용 정책을 수립하여 주기적으로 패치를 관리하고 있는 경우\n'
            '취약 : 패치 적용 정책을 수립하지 않고 주기적으로 패치관리를 하지 않는 경우',
            'ActionPlan': 'OS 관리자, 서비스 개발자가 패치 적용에 따른 서비스 영향 정도를 파악하여 OS 관리자 및 벤더에서 적용함'
        }
        self.fullString = [self.code, '양호', self.stat, self.description]

    def analysisFunc(self, sysInfo, infoDict, fileDict):
        self.fullString[1] = '리뷰'
        keyList = {
            'OS_VERSION': 'OS 버전',
            'OS_KERNEL_VERSION': 'OS 커널 버전'
        }

        for key in keyList.keys():
            if infoDict:
                for info in infoDict:
                    if key in info:
                        self.stat.update({f'CMD:{keyList[key]}': info[key]})

        return self.fullString

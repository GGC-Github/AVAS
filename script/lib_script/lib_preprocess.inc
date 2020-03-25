#############################################################################################
#
# @file lib_preprocess.inc
# 
# @brief 공통 선작업 유틸리티 파일
#
# @version 0.0.1
#
#############################################################################################

##### 스크립트 실행 시 언어 설정
lang_check=`locale -a 2>/dev/null | grep "en_US" | egrep -i "(utf8|utf-8)"`
if [ "$lang_check" = "" ]; then
	lang_check="C"
fi

LANG="$lang_check"
LC_ALL="$lang_check"
LANGUAGE="$lang_check"
export LANG
export LC_ALL
export LANGUAGE

##### 포트 명령어 설정
if [ "`command -v netstat 2>/dev/null`" != "" ] || [ "`which netstat 2>/dev/null`" != "" ]; then
	port_cmd="netstat"
else
	port_cmd="ss"
fi

if [ "`command -v systemctl 2>/dev/null`" != "" ] || [ "`which systemctl 2>/dev/null`" != "" ]; then
	systemctl_cmd="systemctl"
fi

##### 수집 파일 지정
date_tmp=`date +"%Y%m%d%H%M"`
RESULT_COLLECT_FILE="result_collect_$date_tmp.xml"
RESULT_CMD_DATA_FILE="result_command_data_$date_tmp.xml"
RESULT_FILE_DATA_FILE="result_file_data_$date_tmp.xml"

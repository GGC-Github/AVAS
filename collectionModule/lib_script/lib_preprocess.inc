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

##### 명령어 설정
if [ "`command -v netstat 2>/dev/null`" != "" ] || [ "`which netstat 2>/dev/null`" != "" ]; then
	port_cmd="netstat"
else
	port_cmd="ss"
fi

if [ "`command -v systemctl 2>/dev/null`" != "" ] || [ "`which systemctl 2>/dev/null`" != "" ]; then
	systemctl_cmd="systemctl"
fi

if [ "`command -v readlink 2>/dev/null`" != "" ] || [ "`which readlink 2>/dev/null`" != "" ]; then
	readlink_cmd="readlink"
fi

##### 수집 파일 지정
date_tmp=`date +"%Y%m%d%H%M"`
SCRIPT_EXECUTE_PATH=`pwd`
RESULT_COLLECT_FILE="$SCRIPT_EXECUTE_PATH/result_collect_$date_tmp.xml"
RESULT_CMD_DATA_FILE="$SCRIPT_EXECUTE_PATH/result_command_data_$date_tmp.xml"
RESULT_FILE_DATA_FILE="$SCRIPT_EXECUTE_PATH/result_file_data_$date_tmp.xml"

##### root 계정으로의 실행 여부 확인
if [ "`id | grep \"uid=0\"`" = "" ]; then
	echo ""; 
	echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=";
	echo "";
	echo "This script must be run as root.";
	echo "";
	echo "진단 스크립트는 root 권한으로 실행해야 합니다.";
	echo ""; 
	echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=";
	echo ""; 
	exit 1;
fi

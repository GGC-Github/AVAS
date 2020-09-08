#############################################################################################
#
# @file lib_shell_encode.inc
# 
# @brief 공통 인코딩 유틸리티 파일
#
# @version 0.0.1
#
#############################################################################################
data_cmd_encoding() {
	data="$1"
	if [ "`command -v base64 2>/dev/null`" != "" ] || [ "`which base64 2>/dev/null`" != "" ]; then
		echo "$data" | sed -e 's/^ *//g' -e 's/^	*//g' | base64 -w 76
	fi
}

data_file_encoding() {
	file_name=$1
	if [ "`command -v base64 2>/dev/null`" != "" ] || [ "`which base64 2>/dev/null`" != "" ]; then
		if [ "`echo $file_name | egrep 'issue\.net|motd'`"  != "" ]; then
			cat $file_name | sed -e 's/^ *//g' -e 's/^	*//g' | base64 -w 76
		else
			cat $file_name | sed -e 's/^ *//g' -e 's/^   *//g' | egrep -v '^$|^#' | base64 -w 76
		fi
	fi
}

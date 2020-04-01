#############################################################################################
#
# @file lib_autostruct.inc
# 
# @brief 공통 xml 파일 구조 시작 유틸리티 파일
#
# @version 0.0.1
#
#############################################################################################
xml_file_header_tag "$RESULT_COLLECT_FILE"

xml_tag_write "$RESULT_COLLECT_FILE" "<root>" "0"

xml_sysInfo_contents "$RESULT_COLLECT_FILE"

#xml_tag_write "$RESULT_COLLECT_FILE" "<infoElementList>" "1"

#xml_tag_write "$RESULT_CMD_DATA_FILE" "<commandList>" "2"

xml_tag_write "$RESULT_FILE_DATA_FILE" "<fileList>" "1"


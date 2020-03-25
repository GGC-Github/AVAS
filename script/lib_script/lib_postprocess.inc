#############################################################################################
#
# @file lib_postprocess.inc
# 
# @brief 공통 후작업 유틸리티 파일
#
# @version 0.0.1
#
#############################################################################################

xml_infoElementList_tag_end "$RESULT_COLLECT_FILE"
xml_dataElementList_tag_start "$RESULT_COLLECT_FILE"

xml_commandList_tag_end "$RESULT_CMD_DATA_FILE"
xml_fileList_tag_end "$RESULT_FILE_DATA_FILE"

## Merge Result Files
if [ -f "$RESULT_COLLECT_FILE" ]; then
	if [ -f "$RESULT_CMD_DATA_FILE" ]; then
		cat "$RESULT_CMD_DATA_FILE" >> $RESULT_COLLECT_FILE
		rm -f "$RESULT_CMD_DATA_FILE"
	fi
	if [ -f "$RESULT_FILE_DATA_FILE" ]; then
		cat "$RESULT_FILE_DATA_FILE" >> $RESULT_COLLECT_FILE
		rm -f "$RESULT_FILE_DATA_FILE"
	fi
	xml_dataElementList_tag_end "$RESULT_COLLECT_FILE"
	xml_root_tag_end "$RESULT_COLLECT_FILE"
else
	echo "[Error] Not Found Result Files"
fi

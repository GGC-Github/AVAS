:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: @file lib_batch_postprocess.inc
::
:: @brief 공통 후작업 유틸리티 파일
::
:: @version 0.0.1
::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

echo     ^</fileList^> >> %RESULT_FILE_DATA_FILE%
copy %RESULT_COLLECT_FILE% + %RESULT_FILE_DATA_FILE% %RESULT_COLLECT_FILE% /b
echo ^</root^> >> %RESULT_COLLECT_FILE%

del /q "systeminfo.txt"
del /q "base64.txt"
del /q "%RESULT_FILE_DATA_FILE%"

exit /b 0
:base64encode
	certutil -encode %~1 base64tmp.txt
	type base64tmp.txt | findstr /v CERTIFICATE > base64.txt
	del /q %~1
	del /q base64tmp.txt
exit /b

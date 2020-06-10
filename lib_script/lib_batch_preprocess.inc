@echo off
set local
chcp 437>nul
PUSHD %~DP0

set hh=%time:~0,2%
set hh1=%hh:~0,1%
set hh2=%hh:~1,1%
if "%hh1%" == " " set hh=0%hh2%
set DATETEXT=%hh%%time:~3,2%%time:~6,2%
for /f "tokens=*" %%a in ('hostname') do set HOSTNAME=%%a

set RESULT_COLLECT_FILE=result_collect_%HOSTNAME%_%DATETEXT%.xml
set RESULT_FILE_DATA_FILE=result_file_data_%HOSTNAME%_%DATETEXT%.xml

net session>nul 2>&1
if not "%ERRORLEVEL%" == "0" (
	echo.
	echo =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	echo.
	echo This script must be run as admin.
	echo.
	echo =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	echo.
	pause>nul
	exit
)

set checksumvalue=DUP

echo ^<?xml version="1.0" encoding="UTF-8"?^> > %RESULT_COLLECT_FILE%
echo ^<root^> >> %RESULT_COLLECT_FILE%
echo     ^<sysInfo^> >> %RESULT_COLLECT_FILE%

systeminfo > systeminfo.txt
for /f "tokens=1,2 delims=:" %%a in ('"findstr /bic:"OS Name" systeminfo.txt"') do set OSNAME=%%b
for /f "tokens=1,2 delims=:" %%a in ('"findstr /bic:"OS Version" systeminfo.txt"') do set OSVERSION=%%b
for /f "tokens=1,2 delims=:" %%a in ('"findstr /bic:"OS Host Name" systeminfo.txt"') do set HOSTNAME=%%b

set OSNAME=%OSNAME: =%
set OSVERSION=%OSVERSION: =%
set HOSTNAME=%HOSTNAME: =%

echo         ^<osType^>Windows^</osType^> >> %RESULT_COLLECT_FILE%
echo         ^<osName^>%OSNAME%^</osName^> >> %RESULT_COLLECT_FILE%
echo         ^<osVersion^>%OSVERSION%^</osVersion^> >> %RESULT_COLLECT_FILE%
echo         ^<hostname^>%HOSTNAME%^</hostname^> >> %RESULT_COLLECT_FILE%

certutil > nul
if "%ERRORLEVEL%" == "0" (set ENCTYPE=base64) else (set ENCTYPE=NULL)
echo         ^<encType^>%ENCTYPE%^</encType^> >> %RESULT_COLLECT_FILE%

ipconfig | more > iplist.txt
call :base64encode iplist.txt
echo         ^<ipList^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
echo         ^]^]^>^</ipList^> >> %RESULT_COLLECT_FILE%

tasklist | more > tasklist.txt
call :base64encode tasklist.txt
echo         ^<processInfo^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
echo         ^]^]^>^</processInfo^> >> %RESULT_COLLECT_FILE%

netstat -ano | more > portlist.txt
call :base64encode portlist.txt
echo         ^<portInfo^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
echo         ^]^]^>^</portInfo^> >> %RESULT_COLLECT_FILE%

net start | more > servicelist.txt
call :base64encode servicelist.txt
echo         ^<serviceInfo^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
echo         ^]^]^>^</serviceInfo^> >> %RESULT_COLLECT_FILE%

echo     ^</sysInfo^> >> %RESULT_COLLECT_FILE%

echo     ^<fileList^> > %RESULT_FILE_DATA_FILE%
@echo off
rem  
rem  Licensed Materials - Property of IBM and/or HCL
rem
rem  HCL OneDB Server
rem  (c) Copyright IBM Corporation 2011 All rights reserved.
rem  (c) Copyright HCL Technologies Ltd. 2017.  All Rights Reserved.
rem
rem  
rem
rem  Name        : cmalarmprogram.bat
rem  Created     : May 2011
rem  Description : Automates many IDS events using event alarms from the
rem               Connection Manager. To install this script, add the following
rem               line to the configuration file :
rem                  CMALARMPROGRAM    <INFORMIXDIR>/etc/alarmprogram.bat
rem               where <INFORMIXDIR> is replaced by the full value of $INFORMIXDIR
rem               This script sends email and pages the DBA when necessary.
rem
rem  /**************************************************************************/


rem ########################################
rem                                          
rem PUBLIC SECTION : CONFIGURATION VARIABLES 
rem                                          
rem ########################################

SET ALARMADMIN=0
SET ALARMPAGER=0
SET ADMINEMAIL=
SET PAGEREMAIL=

SET MAILUTILITY=%INFORMIXDIR%\bin\ntmail
SET POPSERVER=
SET SENDER=informix@.machine.com



rem #########################################
rem                                          
rem     PRIVATE SECTION : EVENT HANDLERS         
rem                                          
rem #########################################

set ALRM_NOTWORTHY=1
set ALRM_INFO=2
set ALRM_ATTENTION=3
set ALRM_EMERGENCY=4
set ALRM_FATAL=5

set EVENT_SEVERITY=%1
set EVENT_CLASS=%2
set EVENT_MSG=%~3
set EVENT_ADD_TEXT="%~4"
rem If this alarm is for a specific connection unit then the unit's name is
rem included in EVENT_ADD_TEXT.  It is also available via the 
rem INFORMIXCMCONUNITNAME environment variable.
set EVENT_FILE="%~5"
set EVENT_UNIQID=%6

set EXIT_STATUS=0
set RM=del
set MAILBODY=%TEMP%\B_%RANDOM%_%EVENT_CLASS%
set MAILHEAD=%TEMP%\H_%RANDOM%_%EVENT_CLASS%
set TMPFILE=%TEMP%\1_%RANDOM%_%EVENT_CLASS%
set TMPFILE2=%TEMP%\2_%RANDOM%_%EVENT_CLASS%
set TMPFILE3=%TEMP%\3_%RANDOM%_%EVENT_CLASS%
set ALARMTESTFILE=
SET DATE_INT=x
SET TIME_INT=y
SET COUNT=0

rem /* Keep track of the last 5 minutes of the alarm log */
SET LASTALARMFILE=%TEMP%\.%INFORMIXCMNAME%.lastcmalarm
SET CURRENT=%TEMP%\%INFORMIXCMNAME%.alarm.current

rem /* Get Format and delimiter information for data and time. */
for /F "tokens=3" %%a in ('reg query "HKCU\Control Panel\International" /v iDate') do set "DATE_FORMAT=%%a"
for /F "tokens=3" %%a in ('reg query "HKCU\Control Panel\International" /v sDate') do set "DATE_DELIM=%%a"
for /F "tokens=3" %%a in ('reg query "HKCU\Control Panel\International" /v sTime') do set "TIME_DELIM=%%a"
for /F "tokens=3" %%a in ('reg query "HKCU\Control Panel\International" /v sDecimal') do set "DECIMAL_DELIM=%%a"


rem /*Remove optional day in the beginning if it exists. */
for %%x in (%DATE%) do set TODAY_DATE=%%x

rem /*Make international date based on the format */
for /F "tokens=1-3 delims=%DATE_DELIM% " %%x in ("%TODAY_DATE%") do (
  if %DATE_FORMAT%==0 set DATE_INT=%%z-%%x-%%y
  if %DATE_FORMAT%==1 set DATE_INT=%%z-%%y-%%x
  if %DATE_FORMAT%==2 set DATE_INT=%%x-%%y-%%z
)

rem /*Use international time and decimal delimiters to set time information */
for /F "tokens=1,2,3 delims=%TIME_DELIM%%DECIMAL_DELIM%" %%x in ("%TIME%") do set TIMESTR=%%x%%y%%z & set TIME_INT=%%x:%%y:%%z & set M=%%y
for /F "tokens=1 delims=0" %%x in ("%M%") do set MIN=%%x

if %MIN% LSS 5 (set /A T5MINAGO=%TIMESTR% - 4500) else set /A T5MINAGO=%TIMESTR% - 500

if NOT EXIST %LASTALARMFILE% goto BYPASS
for /F "tokens=1,2,3,4* delims=:. " %%i in (%LASTALARMFILE%) do if %%i EQU %DATE_INT% if %%j%%k%%l GEQ %T5MINAGO% @echo %DATE_INT% %%j:%%k:%%l %%m>> %CURRENT%

if EXIST %CURRENT% move %CURRENT% %LASTALARMFILE%
:BYPASS

rem In order avoid sending incorrect mails ALARMADMIN and ALARMPAGER
rem must be correctly configured.  If they are out of range or unset 
rem they will be reset to 0 (deactivated).

if "x%ALARMADMIN%" == "x" echo ALARMADMIN is unset, setting it to 0. & set ALARMADMIN=0
if %ALARMADMIN% LSS 0  goto badadmin
if %ALARMADMIN% GTR 5  goto badadmin
  goto ebadadmin
:badadmin
  echo ALARMADMIN is out of range, reseting it to 0 from %ALARMADMIN%
  set ALARMADMIN=0
:ebadadmin

if x%ALARMPAGER% == x echo ALARMPAGER is unset, setting it to 0. & SET ALARMPAGER=0
if %ALARMPAGER% LSS 0 goto badpager
if %ALARMPAGER% GTR 5 goto badpager
  goto ebadpager
:badpager
  echo ALARMPAGER is out of range, reseting it to 0 from %ALARMPAGER% 
  set ALARMPAGER=0
:ebadpager

if %EVENT_SEVERITY% EQU 1 set EVENT_SEVERITY_NAME=trivia
if %EVENT_SEVERITY% EQU 2 set EVENT_SEVERITY_NAME=information
if %EVENT_SEVERITY% EQU 3 set EVENT_SEVERITY_NAME=Attention!
if %EVENT_SEVERITY% EQU 4 set EVENT_SEVERITY_NAME=EMERGENCY!!
if %EVENT_SEVERITY% EQU 5 set EVENT_SEVERITY_NAME=FATAL EVENT!!! 

rem Cleanup the mail header and the mail body file 
%RM% %MAILBODY% %MAILHEAD% %TMPFILE% 2>> nul

echo Subject: %INFORMIXCMNAME% : %EVENT_SEVERITY_NAME% : %EVENT_MSG% >> %MAILHEAD%
echo %EVENT_ADD_TEXT% >> %MAILBODY%

set NOSENDER=1
rem /* Send e-mail to who may be interested */

if %ALARMADMIN% EQU 0 goto eaadmin
if %EVENT_SEVERITY% LSS %ALARMADMIN% goto lssadmin
if "x%ADMINEMAIL%" == "x" goto :eadmin
  echo To: %ADMINEMAIL% >> %MAILHEAD%
  set MAILTO=%ADMINEMAIL%
  set NOSENDER=0
  goto eaadmin
:lssadmin
  echo Event Severity = %EVENT_SEVERITY% is lower than ALARMADMIN=%ALARMADMIN%
  echo No mail will be sent to ALARMEMAIL
:eaadmin

if %ALARMPAGER% EQU 0 goto eapager
if %EVENT_SEVERITY% LSS %ALARMPAGER% goto lsspager
if "x%PAGEREMAIL%" == "x" goto :eapager
  if %NOSENDER% EQU 0 echo cc: %PAGEREMAIL% >> %MAILHEAD% & set MAILTO=%MAILTO% %PAGEREMAIL% & goto eapager
    echo To: %PAGEREMAIL%  >> %MAILHEAD%
    set MAILTO=%PAGEREMAIL%
    goto :eapager
:lsspager
  echo Event Severity = $EVENT_SEVERITY is lower than ALARMPAGER=%ALARMPAGER%
  echo No mail will be sent to PAGEREMAIL
:eapager

if "x%MAILTO%" == "x" echo SENDER IS NULL NO MAIL WILL BE SENT. & goto endprog

rem /* send mail */ 
if "x%ALARMPROGRAMTEST%" == "x" goto tomail 
  type %MAILBODY% >> %ALARMTESTFILE%
goto endprog

:tomail
if "x%MAILUTILITY%" == "x" echo MAILUTILITY is not set, NO MAIL will be sent. & goto endprog 
  REM /* Do not send same alarm in less than 5 minute intervel. */
  if NOT EXIST %LASTALARMFILE% echo. > %LASTALARMFILE%
  TYPE %LASTALARMFILE% | FIND /C "%EVENT_MSG%" > %TMPFILE3% 
  for /f "tokens=1" %%x in ( %TMPFILE3% ) do set COUNT=%%x 
  if %COUNT% GEQ 1 goto endprog
   %MAILUTILITY% -h %POPSERVER% -f %SENDER% -s "%INFORMIXCMNAME% : %EVENT_SEVERITY_NAME% : %EVENT_MSG% " %MAILTO% < %MAILBODY%  >> NUL 2>&1
:endprog
echo %DATE_INT% %TIME_INT% %EVENT_MSG% >> %LASTALARMFILE%
%RM% %MAILHEAD% %MAILBODY% %TMPFILE% %TMPFILE2% %TMPFILE3% %SQLTMPFILE% 

SET ALARMADMIN=
SET ALARMPAGER=
SET ADMINEMAIL=
SET PAGEREMAIL=
SET MAILUTILITY=
SET POPSERVER=
SET SENDER=


set ALRM_NOTWORTHY=
set ALRM_INFO=
set ALRM_ATTENTION=
set ALRM_EMERGENCY=
set ALRM_FATAL=

rem /* input parameters */
set EVENT_SEVERITY=
set EVENT_CLASS=
set EVENT_MSG=
set EVENT_ADD_TEXT=
set EVENT_FILE=

set RM=
set MAILBODY=
set MAILHEAD=
set TMPFILE=
set TMPFILE2=
set TMPFILE3=
set EXIT_STATUS=


@echo off

set HADOOP_HOME=C:\hadoop

echo ========================================
echo Uploading Expense Data
echo ========================================

"%HADOOP_HOME%\bin\hadoop.cmd" fs -mkdir -p /expense

"%HADOOP_HOME%\bin\hadoop.cmd" fs -put -f "C:\Users\Dell\Desktop\expense\data\data.csv" /expense/

echo.
echo Checking uploaded file...

"%HADOOP_HOME%\bin\hadoop.cmd" fs -ls /expense

echo.
echo Upload completed.

pause
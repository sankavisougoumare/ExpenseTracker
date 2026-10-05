@echo off
title Expense Tracker - Hadoop Setup

echo ==========================================
echo   EXPENSE TRACKER - HADOOP SETUP
echo ==========================================
echo.

set HADOOP_HOME=C:\hadoop
set JAVA_HOME=C:\Progra~1\Java\jdk-25

echo [1/4] Checking Hadoop...
call "%HADOOP_HOME%\bin\hadoop.cmd" version

if errorlevel 1 (
    echo.
    echo ERROR: Hadoop could not be started.
    pause
    exit /b 1
)

echo.
echo [2/4] Checking Hadoop directories...

if not exist "%HADOOP_HOME%\data\namenode" (
    mkdir "%HADOOP_HOME%\data\namenode"
)

if not exist "%HADOOP_HOME%\data\datanode" (
    mkdir "%HADOOP_HOME%\data\datanode"
)

echo.
echo [3/4] Starting NameNode...

start "Hadoop NameNode" cmd /k "cd /d C:\hadoop\bin && hadoop.cmd namenode"

timeout /t 5 /nobreak >nul

echo.
echo [4/4] Starting DataNode...

start "Hadoop DataNode" cmd /k "cd /d C:\hadoop\bin && hadoop.cmd datanode"

echo.
echo ==========================================
echo Hadoop startup commands sent.
echo ==========================================
echo.
echo Wait 10 seconds and run:
echo.
echo     jps
echo.
pause
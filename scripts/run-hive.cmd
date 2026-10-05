@echo off

set HIVE_HOME=C:\hive

echo ========================================
echo Expense Tracker - Hive
echo ========================================

echo.
echo Creating database...

hive -f "C:\Users\Dell\Desktop\expense\hive\01_create_database.sql"

echo.
echo Creating table...

hive -f "C:\Users\Dell\Desktop\expense\hive\02_create_table.sql"

echo.
echo Loading data...

hive -f "C:\Users\Dell\Desktop\expense\hive\03_load_data.sql"

echo.
echo Running analysis...

hive -f "C:\Users\Dell\Desktop\expense\hive\04_analysis.sql"

echo.
echo ========================================
echo Expense Tracker Completed
echo ========================================

pause
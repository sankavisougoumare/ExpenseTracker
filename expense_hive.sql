CREATE DATABASE IF NOT EXISTS expense_tracker;

USE expense_tracker;

DROP TABLE IF EXISTS expenses;

CREATE EXTERNAL TABLE expenses (
    expense_date DATE,
    category STRING,
    amount DOUBLE,
    payment_method STRING,
    description STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/expense';
-- ==========================================
-- EXPENSE TRACKER SQL ANALYSIS
-- ==========================================

-- 1. View all expenses
SELECT *
FROM expenses;


-- 2. Calculate total expense
SELECT SUM(amount) AS total_expense
FROM expenses;


-- 3. Calculate average expense
SELECT AVG(amount) AS average_expense
FROM expenses;


-- 4. Find highest expense
SELECT *
FROM expenses
ORDER BY amount DESC
LIMIT 1;


-- 5. Find lowest expense
SELECT *
FROM expenses
ORDER BY amount ASC
LIMIT 1;


-- 6. Total expense by category
SELECT
    category,
    SUM(amount) AS total_expense
FROM expenses
GROUP BY category
ORDER BY total_expense DESC;


-- 7. Average expense by category
SELECT
    category,
    AVG(amount) AS average_expense
FROM expenses
GROUP BY category
ORDER BY average_expense DESC;


-- 8. Expense by payment method
SELECT
    payment_method,
    SUM(amount) AS total_expense
FROM expenses
GROUP BY payment_method
ORDER BY total_expense DESC;


-- 9. Number of transactions by category
SELECT
    category,
    COUNT(*) AS transaction_count
FROM expenses
GROUP BY category
ORDER BY transaction_count DESC;


-- 10. Daily expense
SELECT
    date,
    SUM(amount) AS daily_expense
FROM expenses
GROUP BY date
ORDER BY date;


-- 11. Monthly expense
SELECT
    year,
    month,
    SUM(amount) AS monthly_expense
FROM expenses
GROUP BY year, month
ORDER BY year, month;


-- 12. Highest spending category
SELECT
    category,
    SUM(amount) AS total_expense
FROM expenses
GROUP BY category
ORDER BY total_expense DESC
LIMIT 1;
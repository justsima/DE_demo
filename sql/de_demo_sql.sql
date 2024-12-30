-- ============================================
-- SECTION 1: DATABASE INITIALIZATION & USER SETUP
-- ============================================

-- Create Database
CREATE DATABASE de_demo;
drop database de_demo;
-- Create User with Password and Assign Roles
CREATE USER de_user WITH PASSWORD 'de_password';
GRANT ALL PRIVILEGES ON DATABASE de_demo TO de_user;
ALTER ROLE de_user CREATEDB;
GRANT CREATE ON SCHEMA public TO de_user;
GRANT USAGE ON SCHEMA public TO de_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO de_user;
ALTER USER de_user WITH SUPERUSER;

-- ============================================
-- SECTION 2: STAGING TABLE CREATION
-- ============================================

-- Create Transactions Staging Table
CREATE TABLE IF NOT EXISTS stg_transactions (
    TransactionID TEXT PRIMARY KEY,
    CustomerID TEXT,
    ProductID TEXT,
    Category TEXT,
    Quantity INTEGER,
    Price FLOAT,
    TransactionDate TIMESTAMP
);
select count(*) from stg_transactions;
-- Create Users Staging Table
CREATE TABLE IF NOT EXISTS stg_users (
    CustomerID TEXT PRIMARY KEY,
    Name TEXT,
    Email TEXT,
    Age INTEGER,
    Country TEXT,
    SignupDate TIMESTAMP
);
select count(*) from stg_users;
-- Create Products Staging Table
CREATE TABLE IF NOT EXISTS stg_products (
    ProductID TEXT PRIMARY KEY,
    ProductName TEXT,
    Category TEXT,
    Brand TEXT,
    Price FLOAT,
    StockQuantity INTEGER
);
select count(*) from stg_products;
-- ============================================
-- SECTION 3: DATA VALIDATION FOR STAGING TABLES
-- ============================================

-- Validate Foreign Key Relationships
SELECT DISTINCT "CustomerID"
FROM public.stg_transactions
WHERE "CustomerID" NOT IN (
    SELECT "CustomerID" FROM public.stg_users
);

SELECT DISTINCT "ProductID"
FROM public.stg_transactions
WHERE "ProductID" NOT IN (
    SELECT "ProductID" FROM public.stg_products
);

-- ============================================
-- SECTION 4: ANALYTICAL TABLE CREATION
-- ============================================

-- Create Dimension Tables
CREATE TABLE IF NOT EXISTS dim_users AS
SELECT DISTINCT
    "CustomerID",
    "Name",
    "Email",
    "Age",
    "Country",
    "SignupDate"
FROM public.stg_users;

CREATE TABLE IF NOT EXISTS dim_products AS
SELECT DISTINCT
    "ProductID",
    "ProductName",
    "Category",
    "Brand",
    "Price",
    "StockQuantity"
FROM public.stg_products;

-- Create Fact Transactions Table
CREATE TABLE IF NOT EXISTS fact_transactions AS
SELECT
    t."TransactionID",
    t."CustomerID",
    t."ProductID",
    t."Quantity",
    t."Price",
    t."TransactionDate",
    u."Age" AS CustomerAge,
    p."Category" AS ProductCategory,
    p."Brand" AS ProductBrand
FROM public.stg_transactions t
JOIN public.stg_users u ON t."CustomerID" = u."CustomerID"
JOIN public.stg_products p ON t."ProductID" = p."ProductID";

-- ============================================
-- SECTION 5: VALIDATION FOR ANALYTICAL TABLES
-- ============================================

-- Validate Data Integrity
SELECT COUNT(*) FROM dim_users;
SELECT COUNT(*) FROM dim_products;
SELECT COUNT(*) FROM fact_transactions;

-- Verify Data in Tables
SELECT * FROM dim_users LIMIT 5;
SELECT * FROM dim_products LIMIT 5;
SELECT * FROM fact_transactions LIMIT 5;

-- ============================================
-- SECTION 6: SQL ANALYSIS FOR BUSINESS INSIGHTS
-- ============================================

-- Find the top 5 customers based on total spending
SELECT u."CustomerID", u."Name", SUM(t."Quantity" * t."Price") AS TotalSpent
FROM fact_transactions t
JOIN dim_users u ON t."CustomerID" = u."CustomerID"
GROUP BY u."CustomerID", u."Name"
ORDER BY TotalSpent DESC
LIMIT 5;

-- Identify the best-selling product in each category
SELECT p."Category", p."ProductName", SUM(t."Quantity") AS TotalQuantity
FROM fact_transactions t
JOIN dim_products p ON t."ProductID" = p."ProductID"
GROUP BY p."Category", p."ProductName"
ORDER BY p."Category", TotalQuantity DESC;

-- Calculate the daily sales trend for the last 7 days
SELECT t."TransactionDate"::DATE AS SalesDate, SUM(t."Quantity" * t."Price") AS DailySales
FROM fact_transactions t
WHERE t."TransactionDate" >= NOW() - INTERVAL '7 days'
GROUP BY SalesDate
ORDER BY SalesDate;

-- Find the category with the highest sales in the last month
SELECT p."Category", SUM(t."Quantity" * t."Price") AS TotalSales
FROM fact_transactions t
JOIN dim_products p ON t."ProductID" = p."ProductID"
WHERE t."TransactionDate" >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY p."Category"
ORDER BY TotalSales DESC
LIMIT 1;
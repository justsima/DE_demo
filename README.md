# **Data Engineering Take-Home Assignment**
*🔗 For Short over view there is a 2-minute project walkthrough video, showcasing key steps and results. Check above in the folder.*

## **Navigation**

- **[1. Introduction](#1-introduction)**
- **[2. Project Setup](#2-project-setup)**
- **[3. Data Ingestion](#3-data-ingestion)**
- **[4. Database Design and Staging Tables](#4-database-design-and-staging-tables)**
- **[5. Data Loading to Staging Area](#5-data-loading-to-staging-area)**
- **[6. Dimension and Fact Tables](#6-dimension-and-fact-tables)**
- **[7. Data Analysis and Insights](#7-data-analysis-and-insights)**
- **[8. Final Validations and Integrity Checks](#8-final-validations-and-integrity-checks)**
- **[9. Conclusion](#9-conclusion)**
- **[10. Lessons Learned](#10-lessons-learned)**

---
## **1. Introduction**

### **Project Overview**

In this project, we developed a **robust data engineering pipeline** to process, transform, and analyze datasets. The focus was on designing a structured workflow to ingest raw data, validate it, transform it into a meaningful format, and derive key business insights.

### **Objective**

The main objectives of this project are:

- **Data Ingestion:** Import raw datasets from CSV files.
- **Database Design:** Design staging, dimension, and fact tables in PostgreSQL.
- **Data Loading:** Load and validate data across different layers of the database.
- **Data Analysis:** Extract meaningful insights through SQL queries and visualizations.
- **Data Validation:** Ensure referential integrity, schema correctness, and data consistency.

### **Tools and Technologies Used**

- **Programming Language:** Python
- **Libraries:** Pandas, SQLAlchemy, Matplotlib
- **Database:** PostgreSQL
- **Visualization:** Jupyter Notebook
- **IDE:** DataGrip for SQL queries
- **Version Control:** Git

### **Key Deliverables**

- A fully functional **data pipeline** to handle raw data ingestion, transformation, and analysis.
- A well-structured **PostgreSQL database schema** with staging, dimension, and fact tables.
- Analytical insights answering critical business questions.
- Clear and professional **documentation** showcasing the pipeline architecture and results.

---


# **3. Project Setup**

### **Objective**

This section outlines the **setup and configuration steps** required to prepare the environment for the project. It ensures all dependencies, tools, and configurations are in place to guarantee smooth execution.

---

## **3.1 Prerequisites**

Ensure the following tools and libraries are installed before proceeding:

- **Python (v3.9 or later)** – Data processing and analysis
- **PostgreSQL (v15 or later)** – Database management system
- **DataGrip** – SQL query editor and database management (optional)
- **Jupyter Notebook** – Interactive development environment for Python

```bash
Directory Strcutre
DE_demo/
│
├── data/
│   ├── transactions.csv
│   ├── users.csv
│   ├── products.csv          → Raw datasets (transactions.csv, users.csv, products.csv)
│
├── scripts/         → Python scripts for data ingestion and validation
│   ├── load_to_staging.py
│
├── notebooks/       → Jupyter notebooks for exploration and analysis
│   ├── Explore Dataset.ipynb
│
├── sql/            → SQL scripts for schema creation and data analysis
│   ├── de_demo_sql.sql
│
├── .env            → Environment variables for secure configuration
│
├── README.md       → Documentation file
│
└── requirements.txt → Python dependencies
```

# **4. Data Ingestion**

### **Objective**

In this step, we focus on **loading raw datasets** into Pandas DataFrames, performing **initial exploration (EDA)**, and applying **basic data cleaning and validation** to ensure consistency and integrity before moving data into the staging area in PostgreSQL.

---

## **4.1 Loading Raw Datasets**

### **Goal:**

Load raw datasets (`transactions.csv`, `users.csv`, `products.csv`) into Pandas DataFrames for initial inspection and analysis.

### **Process:**

- Use Pandas to read CSV files into DataFrames.
- Inspect column names, data types, and row counts.
- Identify any immediate issues (e.g., missing values, incorrect data types).

**Key Python Code:**

```python
import pandas as pd

# Load datasets into Pandas DataFrames
transactions_df = pd.read_csv('../data/transactions.csv')
users_df = pd.read_csv('../data/users.csv')
products_df = pd.read_csv('../data/products.csv')

# Display basic information about the datasets
print(transactions_df.info())
print(users_df.info())
print(products_df.info())
```

# **5. Database Design and Staging Tables**

### **Objective**

In this step, we design and create **staging tables** in PostgreSQL. These tables serve as temporary storage for raw but cleaned datasets before they are transformed into **dimension** and **fact tables** for analysis.

---

## **5.1 Staging Table Design**

### **Goal:**

Design staging tables to mirror the structure of the cleaned datasets from the previous step.

### **Staging Table Overview:**

1. **stg_transactions:** Stores transaction details, including `TransactionID`, `CustomerID`, `ProductID`, and `TransactionDate`.
2. **stg_users:** Stores user information, including `CustomerID`, `Name`, `Email`, and `SignupDate`.
3. **stg_products:** Stores product details, including `ProductID`, `ProductName`, `Category`, and `Price`.

---

### **5.2 Checking Staged Tables and validating schema**

The staging tables are created in PostgreSQL using SQL.
After that I did of validation the schema

**SQL Queries:**

```sql
-- Verify Schema for Transactions Table
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'stg_transactions';

-- Verify Schema for Users Table
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'stg_users';

-- Verify Schema for Products Table
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'stg_products';

```

# **6. Data Loading to Staging Area**

### **Objective**

In this step, we **load the cleaned datasets** from Pandas DataFrames into their respective **staging tables** in PostgreSQL. This step ensures that data is successfully transferred, validated, and ready for transformation into **dimension** and **fact tables**.

---

## **6.1 Loading Data into Staging Tables**

### **Goal:**

Insert cleaned data into PostgreSQL staging tables (`stg_transactions`, `stg_users`, `stg_products`) using SQLAlchemy.

### **Process:**

1. Use SQLAlchemy to establish a connection with PostgreSQL.
2. Load datasets into their respective staging tables.
3. Validate row counts after loading.

**Key Python Code:**

```python
from sqlalchemy import create_engine

# Establish a database connection
engine = create_engine('postgresql://de_user:de_password@localhost:5432/de_demo')

# Load DataFrames into staging tables
transactions_df.to_sql('stg_transactions', engine, if_exists='replace', index=False)
users_df.to_sql('stg_users', engine, if_exists='replace', index=False)
products_df.to_sql('stg_products', engine, if_exists='replace', index=False)

print("Data successfully loaded into staging tables.")
```

# **7. Dimension and Fact Tables**

### **Objective**

The purpose of this step is to **organize data into structured tables** optimized for analysis. By transitioning from staging tables to **dimension and fact tables**, we ensure that data is clean, logically structured, and ready for business intelligence and analytical queries.

In this step:

- Dimension tables (`dim_users`, `dim_products`) store descriptive attributes.
- A fact table (`fact_transactions`) captures measurable transactional data.
- Relationships between dimension and fact tables are validated for consistency.

---

## **7.1 Why Dimension and Fact Tables?**

### **Dimension Tables:**

- Contain **descriptive, categorical information** about entities such as users and products.
- Enable analysts to filter and group data efficiently.

**Examples:**

- `dim_users`: Stores user-specific details like Name, Email, Age, Country.
- `dim_products`: Stores product-specific details like Product Name, Category, Brand.

### **Fact Table:**

- Stores **transactional, numeric data** and links to dimension tables via foreign keys.
- Represents measurable business events.

**Example:**

- `fact_transactions`: Stores sales transactions with details like TransactionID, CustomerID, ProductID, Quantity, and Price.

By using **dimension and fact tables**, we improve:

- **Query Performance:** Faster response times for analytical queries.
- **Data Integrity:** Clear separation between descriptive and transactional data.
- **Scalability:** Easier to scale and add new metrics or dimensions.

---

## **7.2 Designing Dimension Tables**

### **Purpose:**

Dimension tables are derived from staging tables (`stg_users`, `stg_products`) and store **unique, descriptive data**.

### **What Happens Here:**

- Only unique and relevant data is extracted.
- Redundant or duplicate rows are removed.
- Attributes are cleaned and prepared for analytical queries.

**Key Dimension Tables:**

1. **dim_users:** Stores customer details.
2. **dim_products:** Stores product details.

### **Example Schema:**

- `dim_users`: CustomerID, Name, Email, Age, Country, SignupDate
- `dim_products`: ProductID, ProductName, Category, Brand, Price, StockQuantity

**Outcome:**

- Dimension tables act as lookup references for the fact table.
- Ensure accurate representation of descriptive attributes.

---

## **7.3 Designing the Fact Table**

### **Purpose:**

The fact table (`fact_transactions`) serves as the **central table** that links dimension tables through **foreign keys**.

### **What Happens Here:**

- Transactional data is aggregated and linked with descriptive attributes from dimension tables.
- Data is optimized for slicing, dicing, and analytical reporting.

**Example Schema:**

- `fact_transactions`: TransactionID, CustomerID, ProductID, Quantity, Price, TransactionDate, CustomerAge, ProductCategory, ProductBrand

### **How it’s Built:**

- Data from `stg_transactions` is joined with `dim_users` and `dim_products`.
- Relevant columns are selected, cleaned, and loaded into the fact table.

**Outcome:**

- The fact table becomes the **single source of truth for transactional insights**.
- Enables meaningful analysis and aggregation across dimensions.

---

## **7.4 Ensuring Referential Integrity**

### **Purpose:**

To ensure **data consistency** across dimension and fact tables.

### **What Happens Here:**

- Verify that every `CustomerID` in the fact table exists in `dim_users`.
- Verify that every `ProductID` in the fact table exists in `dim_products`.
- Ensure no orphaned records are present.

### **Outcome:**

- All relationships between tables are validated.
- No mismatched or incomplete records are carried forward.

---

## **7.5 Validating Row Counts and Schema**

### **Purpose:**

To ensure data was correctly transformed and loaded into dimension and fact tables.

### **What Happens Here:**

- Compare row counts between staging and dimension tables.
- Verify data types and schema in each table.
- Check for missing or null values in critical columns.

### **Outcome:**

- Data integrity across all tables is ensured.
- Schema aligns with expected structures.

---

## **7.6 Summary**

At the end of this step:

- ✅ Data from staging tables was transformed into **dimension tables (`dim_users`, `dim_products`)**.
- ✅ A **fact table (`fact_transactions`)** was created to store transactional data.
- ✅ Referential integrity between tables was validated.
- ✅ Row counts and schema structures were verified.

### **Why This Step Matters:**

The transition from staging tables to analytical tables represents the **core transformation phase** of the data pipeline. The organized structure enables efficient analytical queries and supports scalable business intelligence solutions.

---

# **8. Data Analysis and Insights**

### **Objective**

In this step, we **analyze the data** stored in the `dim_users`, `dim_products`, and `fact_transactions` tables to extract **meaningful business insights**. This phase focuses on answering key questions through **SQL queries** and **visualization techniques**.

---

## **8.1 Why Data Analysis Matters?**

Data analysis converts raw data into **actionable insights**. By leveraging **dimension and fact tables**, we can:

- Identify sales trends and customer behavior.
- Uncover key performance metrics.
- Support business decisions with data-driven evidence.

The analysis will cover both **SQL-based analytical queries** and **visualizations** generated from Jupyter Notebook.

---

## **8.2 Analytical Queries**

### **Purpose:**

To answer key business questions using **SQL queries** on dimension and fact tables.

### **Key Analytical Questions:**

1. **Top-Selling Products:** Which products generate the most sales revenue?
2. **High-Value Customers:** Who are the top customers contributing to sales?
3. **Sales Trends Over Time:** How have sales evolved monthly or yearly?
4. **Category Performance:** Which product categories perform best?

### **SQL Query Example:**

```sql
-- Top 5 Best-Selling Products
SELECT
    p.ProductName,
    SUM(t.Quantity * t.Price) AS TotalRevenue
FROM fact_transactions t
JOIN dim_products p ON t.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY TotalRevenue DESC
LIMIT 5;
```

# **9. Final Validations and Integrity Checks** (#8-final-validations-and-integrity-checks)

### **Objective**

In this step, we perform **final checks** to ensure the entire data pipeline—from ingestion to analysis—has been executed correctly. This includes validating **referential integrity**, **schema consistency**, and **data completeness** across all tables.

---

## **9.1 Why Final Validation Matters?**

Final validations ensure that:

- All data relationships are correctly maintained.
- Data integrity is preserved across staging, dimension, and fact tables.
- Schema definitions match the expected design.
- No inconsistencies are carried into downstream processes or reports.

---

## **9.2 Referential Integrity Validation**

### **Purpose:**

Ensure relationships between **dimension** and **fact tables** are consistent and free from orphaned records.

### **Validation Focus Areas:**

1. Every `CustomerID` in `fact_transactions` exists in `dim_users`.
2. Every `ProductID` in `fact_transactions` exists in `dim_products`.

### **SQL Validation Example:**

```sql
-- Check for Orphaned CustomerIDs
SELECT DISTINCT CustomerID
FROM fact_transactions
WHERE CustomerID NOT IN (SELECT CustomerID FROM dim_users);

-- Check for Orphaned ProductIDs
SELECT DISTINCT ProductID
FROM fact_transactions
WHERE ProductID NOT IN (SELECT ProductID FROM dim_products);
```

# **10. Conclusion**

### **Objective**

In this final step, we **summarize the outcomes** of the data engineering pipeline, highlight the **key achievements**, and provide **recommendations** for potential improvements or next steps.

---

## **10.1 Project Overview**

This project aimed to design and implement a **robust data engineering pipeline** for processing, validating, and analyzing datasets using **Python, PostgreSQL, and Jupyter Notebook**.

The primary objectives achieved include:

- ✅ **Data Ingestion:** Loaded raw datasets into Pandas DataFrames for initial exploration and cleaning.
- ✅ **Data Cleaning and Validation:** Addressed missing values, ensured schema consistency, and validated referential integrity.
- ✅ **Database Design:** Created **staging, dimension, and fact tables** following industry best practices.
- ✅ **Data Transformation:** Transformed raw data into meaningful dimensions and fact tables for analysis.
- ✅ **Data Analysis and Visualization:** Generated insights using SQL analytical queries and Python visualizations.
- ✅ **Validation and Integrity Checks:** Ensured data consistency across all stages of the pipeline.

---

## **10.2 Key Achievements**

1. **Reliable Data Pipeline:**

   - Successfully ingested, cleaned, and loaded datasets into PostgreSQL.
   - Ensured zero data loss or corruption during the process.

2. **Optimized Database Design:**

   - Designed efficient **staging, dimension, and fact tables** aligned with analytical best practices.
   - Ensured referential integrity and schema validation.

3. **Actionable Insights:**

   - Generated key business insights through analytical SQL queries and visualizations.
   - Highlighted trends, patterns, and opportunities for decision-making.

4. **End-to-End Validation:**
   - Performed multiple validation steps to ensure data integrity and correctness across every layer.

---

## **10.3 Challenges Encountered**

1. **Data Inconsistencies:**

   - Missing and invalid values required careful cleaning and validation.

2. **Referential Integrity Issues:**

   - Orphaned keys in `CustomerID` and `ProductID` required additional checks.

3. **Schema Adjustments:**
   - Schema mismatches between staging and analytical tables needed iterative corrections.

### **How These Challenges Were Overcome:**

- Applied consistent data validation steps during ingestion and transformation.
- Validated foreign key relationships through SQL queries.
- Performed schema checks across all stages.

---

## **10.6 Final Thoughts**

This project successfully delivered a **structured, validated, and insightful data engineering pipeline**. The combination of **Python for data processing**, **PostgreSQL for database management**, and **Jupyter Notebook for analysis and visualization** provided an effective framework for solving the given problem.

**Key Takeaways:**

- A well-designed pipeline ensures **data integrity and scalability**.
- Data validation is critical to building a **trustworthy analytical model**.
- Insights derived from structured data play a crucial role in **business decision-making**.

This project demonstrates **end-to-end data engineering expertise** and sets a foundation for future enhancements and scalability.

---

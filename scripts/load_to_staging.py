import pandas as pd
from sqlalchemy import create_engine, text

# Database credentials
DB_USER = 'de_user'
DB_PASSWORD = 'de_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'de_demo'

# Create database engine
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Load datasets
transactions = pd.read_csv('../data/transactions.csv')
users = pd.read_csv('../data/users.csv')
products = pd.read_csv('../data/products.csv')

# Ensure proper data types
transactions['TransactionDate'] = pd.to_datetime(transactions['TransactionDate'], errors='coerce')
users['SignupDate'] = pd.to_datetime(users['SignupDate'], errors='coerce')

# Create staging tables
CREATE_STAGING_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS staging_transactions (
    TransactionID TEXT,
    CustomerID TEXT,
    ProductID TEXT,
    Category TEXT,
    Quantity INTEGER,
    Price FLOAT,
    TransactionDate TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging_users (
    CustomerID TEXT,
    Name TEXT,
    Email TEXT,
    Age INTEGER,
    Country TEXT,
    SignupDate TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging_products (
    ProductID TEXT,
    ProductName TEXT,
    Category TEXT,
    Brand TEXT,
    Price FLOAT,
    StockQuantity INTEGER
);
"""

def create_staging_tables():
    with engine.connect() as connection:
        connection.execute(text(CREATE_STAGING_TABLES_SQL))
        print("✅ Staging tables created successfully!")

def load_to_staging():
    transactions.to_sql('staging_transactions', engine, if_exists='replace', index=False)
    users.to_sql('staging_users', engine, if_exists='replace', index=False)
    products.to_sql('staging_products', engine, if_exists='replace', index=False)
    print("✅ Data successfully loaded into staging tables!")

if __name__ == '__main__':
    create_staging_tables()
    load_to_staging()

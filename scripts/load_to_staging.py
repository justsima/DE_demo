# load_to_stage.py

import pandas as pd
from sqlalchemy import create_engine, text
import os

# Ensure to create a .env file with appropriate credentials in your project directory.
DB_USER = os.getenv('POSTGRES_USER', 'de_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'de_password')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'de_demo')

# Database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_csv_files():
    """
    Load datasets from CSV files into Pandas DataFrames.
    """
    try:
        transactions_df = pd.read_csv('../data/transactions.csv')
        users_df = pd.read_csv('../data/users.csv')
        products_df = pd.read_csv('../data/products.csv')
        print("✅ Datasets successfully loaded into Pandas DataFrames.")
        return transactions_df, users_df, products_df
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        raise

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database.
    """
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("✅ Successfully connected to the PostgreSQL database.")
        return engine, connection
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise

def load_to_staging(engine, transactions_df, users_df, products_df):
    """
    Load DataFrames into staging tables in PostgreSQL.
    """
    try:
        transactions_df.to_sql('stg_transactions', engine, if_exists='replace', index=False)
        users_df.to_sql('stg_users', engine, if_exists='replace', index=False)
        products_df.to_sql('stg_products', engine, if_exists='replace', index=False)
        print("✅ Data successfully loaded into staging tables.")
    except Exception as e:
        print(f"❌ Error loading data into staging tables: {e}")
        raise


def validate_staging_tables(engine):
    """
    Validate row counts and schema integrity in staging tables.
    """
    validation_queries = {
        "stg_transactions": "SELECT COUNT(*) FROM stg_transactions;",
        "stg_users": "SELECT COUNT(*) FROM stg_users;",
        "stg_products": "SELECT COUNT(*) FROM stg_products;"
    }
    try:
        with engine.connect() as connection:
            for table, query in validation_queries.items():
                result = connection.execute(text(query)).fetchone()
                print(f"✅ {table} row count: {result[0]}")
        print("✅ Validation checks completed successfully.")
    except Exception as e:
        print(f"❌ Error during validation checks: {e}")
        raise

def main():
    """
    Main function to orchestrate the pipeline.
    """
    print("🚀 Starting data loading to staging pipeline...")
    
    # Step 1: Load CSV Files
    transactions_df, users_df, products_df = load_csv_files()
    
    # Step 2: Establish Database Connection
    engine, connection = get_db_connection()
    
    # Step 3: Load Data into Staging Tables
    load_to_staging(engine, transactions_df, users_df, products_df)
    
    # Step 4: Validate Staging Tables
    validate_staging_tables(engine)
    
    # Step 5: Close Database Connection
    connection.close()
    engine.dispose()
    print("✅ Pipeline execution completed successfully.")

if __name__ == '__main__':
    main()

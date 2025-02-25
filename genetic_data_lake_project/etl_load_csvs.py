import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Text
import traceback

# Database connection parameters
DB_USER = "myuser"          # Replace with your PostgreSQL username
DB_PASSWORD = "mypassword"  # Replace with your PostgreSQL password
DB_NAME = "datalake"        # Your database name
DB_HOST = "localhost"       # Using localhost (Docker maps container port to host)
DB_PORT = "5432"

# Create the SQLAlchemy engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Mapping of CSV file names to table names
files_and_tables = {
    "individuals.csv": "individuals",
    "relationships.csv": "relationships",
    "marriages.csv": "marriages",
    "snp_definitions.csv": "snp_definitions",
    "snps.csv": "snps",
    "indel_definitions.csv": "indel_definitions",
    "indels.csv": "indels",
    "structural_variants.csv": "structural_variants",
    "health_phenotypes.csv": "health_phenotypes",
    "lifestyle.csv": "lifestyle"
}

data_lake_dir = "data_lake"

def load_csv_to_db(csv_file, table_name):
    file_path = os.path.join(data_lake_dir, csv_file)
    print(f"\nLoading {file_path} into table {table_name}...")
    
    # For relationships, force columns to be strings.
    if table_name == "relationships":
        reader = pd.read_csv(file_path, chunksize=100000, 
                             dtype={'individual_id': str, 'father_id': str, 'mother_id': str})
        # Specify SQL types for these columns.
        dtype = {"individual_id": Text(), "father_id": Text(), "mother_id": Text()}
    else:
        reader = pd.read_csv(file_path, chunksize=100000)
        dtype = None

    chunk_number = 0
    table_created = False  # For relationships, we want to replace the table on the first chunk.
    
    for chunk in reader:
        chunk_number += 1
        try:
            if table_name == "relationships":
                # Ensure the columns are strings and replace missing values with None
                for col in ["father_id", "mother_id"]:
                    if col in chunk.columns:
                        chunk[col] = chunk[col].where(chunk[col].notna(), None)
                # For the first chunk, replace the table; afterward, append
                if not table_created:
                    method = "replace"
                    table_created = True
                else:
                    method = "append"
            else:
                method = "append"
            chunk.to_sql(table_name, engine, if_exists=method, index=False, dtype=dtype)
            print(f"Chunk {chunk_number} loaded for {table_name}.")
        except Exception as e:
            print(f"Error loading chunk {chunk_number} for table {table_name}: {e}")
            traceback.print_exc()
            continue
    print(f"Finished loading {table_name}.")

if __name__ == "__main__":
    for csv_file, table_name in files_and_tables.items():
        try:
            # Catch empty file errors
            try:
                load_csv_to_db(csv_file, table_name)
            except pd.errors.EmptyDataError:
                print(f"Warning: {csv_file} is empty. Skipping.")
        except Exception as e:
            print(f"Critical error loading {csv_file} into {table_name}: {e}")
            traceback.print_exc()
            continue
    print("ETL complete!")

from app.Data.db import connect_database
import pandas as pd

def insert_dataset(dataset_id, name, num_rows, num_columns, uploaded_by, upload_date):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_id, name, num_rows, num_columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (dataset_id, name, num_rows, num_columns, uploaded_by, upload_date))

    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()

    return dataset_id

def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df


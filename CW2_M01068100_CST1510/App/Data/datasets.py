import pandas as pd
from CW2_M01068100_CST1510.app.Data.db import connect_database

def insert_dataset(dataset_name, file_name, records, description, owner):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, file_name, records, description, owner)
        VALUES (?, ?, ?, ?, ?)
    """, (dataset_name, file_name, records, description, owner))

    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()

    return dataset_id


def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df

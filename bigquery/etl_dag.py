from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import mysql.connector as mysql
from google.cloud import bigquery, storage
import pandas as pd
import io

def connect_bigquery():
    bigquery_connection = bigquery.Client("secret-compass-453715-h4")
    return bigquery_connection

def connect_storage():
    storage_client = storage.Client()
    return storage_client

def connect_mysql():
    mysql_connection = mysql.connect(
        host="mysql-cloud",
        port="3306",
        user="root",
        password="",
        database="ecommerce"
    )
    return mysql_connection

def read_query_from_mysql(mysql_connection, query_str):
    cursor = mysql_connection.cursor()
    cursor.execute(query_str)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    cursor.close()
    return df

def read_csv_from_gcs(cloud_storage, bucket_name, file_name):
    bucket = cloud_storage.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_string()
    df = pd.read_csv(io.StringIO(data.decode('utf-8')))
    return df

def write_csv_to_gcs(cloud_storage, bucket_name, file_name, df):
    csv_data = df.to_csv(index=False)
    bucket = cloud_storage.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_data, content_type='text/csv')

def calculate_customer_distribution(df_customers, df_cities):
    df_customer_distribution = df_customers.groupby(by="city").count()["customer_id"]
    df_merged = pd.merge(df_cities, df_customer_distribution, left_on="name", right_on="city", how="left")[["city_id", "customer_id"]].rename(columns={"customer_id": "population"})
    df_merged.fillna(0, inplace=True)
    df_merged["population"] = df_merged["population"].astype(int)
    return df_merged

def populate_cities_in_bigquery(bigquery_connection, df_cities):
    bigquery_connection.query("delete from ecommerce.cities where city_id >= 0").result()
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    table_id = "secret-compass-453715-h4.ecommerce.cities"
    job = bigquery_connection.load_table_from_dataframe(df_cities, table_id, job_config=job_config)
    job.result()

def populate_customer_distribution_in_bigquery(bigquery_connection, df_customer_distribution):
    bigquery_connection.query("delete from ecommerce.customer_distribution where city_id >= 0").result()
    df_customer_distribution["created_at"] = datetime.now()
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    table_id = "secret-compass-453715-h4.ecommerce.customer_distribution"
    job = bigquery_connection.load_table_from_dataframe(df_customer_distribution, table_id, job_config=job_config)
    job.result()

def read_query_from_bigquery(bigquery_connection, query_str):
    query = bigquery_connection.query(query_str)
    df = query.to_dataframe()
    return df

def etl_process():
    mysql_connection = connect_mysql()
    df_cities = read_query_from_mysql(mysql_connection, "SELECT * from cities")
    cloud_storage = connect_storage()
    df_customers = read_csv_from_gcs(cloud_storage, "ecommerce_files", "customers/customers.csv")
    df_customer_distribution = calculate_customer_distribution(df_customers, df_cities)
    bigquery_connection = connect_bigquery()
    populate_cities_in_bigquery(bigquery_connection, df_cities)
    populate_customer_distribution_in_bigquery(bigquery_connection, df_customer_distribution)
    df_distribution_in_cities = read_query_from_bigquery(bigquery_connection, "SELECT cities.name as city_name, customer_dist.population from `secret-compass-453715-h4.ecommerce.customer_distribution` as customer_dist left join `secret-compass-453715-h4.ecommerce.cities` as cities on customer_dist.city_id = cities.city_id order by population desc")
    write_csv_to_gcs(cloud_storage, "ecommerce_files", "customers/distributions_in_cities.csv", df_distribution_in_cities)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 17),
    'retries': 1
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL pipeline using Airflow',
    schedule_interval='@daily'
)

task_run_etl = PythonOperator(
    task_id='run_etl_process',
    python_callable=etl_process,
    dag=dag
)

task_run_etl

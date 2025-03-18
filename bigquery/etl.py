import mysql.connector as mysql
from google.cloud import bigquery, storage
import datetime
import pandas as pd
import io

def connect_bigquery():
    # connect to bigquery
    bigquert_connection = bigquery.Client("secret-compass-453715-h4")
    return bigquert_connection


def connect_storage():
    # connect to google cloud storage
    storage_client = storage.Client()
    return storage_client


def connect_mysql():
    # connect to mysql
    mysql_connection = mysql.connect(
        host="localhost",
        port = "3306",
        user = "root",
        password = "",
        database = "ecommerce"
    )
    return mysql_connection


def read_query_from_mysql(mysql_connection, query_str):
    # read cities from mysql database
    cursor = mysql_connection.cursor()
    cursor.execute(query_str)
    result = cursor.fetchall()

    # convert the result to a pandas dataframe
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

    cursor.close()
    return df


def read_csv_from_gcs(cloud_storage, bucket_name, file_name):
    # read a csv file from google cloud storage

    # get the bucket
    bucket = cloud_storage.bucket(bucket_name)

    # get the blob
    blob = bucket.blob(file_name)

    # download the blob as a string
    data = blob.download_as_string()

    # convert the string to a pandas dataframe
    df = pd.read_csv(io.StringIO(data.decode('utf-8')))

    return df

def write_csv_to_gcs(cloud_storage, bucket_name, file_name, df):
    # write a pandas dataframe to a csv file in google cloud storage

    # convert the dataframe to a csv string
    csv_data = df.to_csv(index=False)

    # get the bucket
    bucket = cloud_storage.bucket(bucket_name)

    # get the blob
    blob = bucket.blob(file_name)

    # upload the csv string to the blob
    blob.upload_from_string(csv_data, content_type='text/csv')


def calculate_customer_distribution(df_customers : pd.DataFrame, df_cities : pd.DataFrame):
    # calculate the distribution of each city based on the customers dataframe

    # group the customers by city and count the number of customers in each city
    df_customer_distribution = df_customers.groupby(by="city").count()["customer_id"]

    # merge the cities dataframe with the customer distribution dataframe
    df_merged = pd.merge(df_cities, df_customer_distribution, left_on="name", right_on="city", how="left")[["city_id","customer_id"]].rename(columns={"customer_id":"population"})

    # fill the cities without population with 0
    df_merged.fillna(0, inplace=True)

    # convert the population to integer
    df_merged["population"] = df_merged["population"].astype(int)

    return df_merged


def populate_cities_in_bigquery(bigquery_connection, df_cities : pd.DataFrame):
    # populate cities read from the mysql table in bigquery

    # delete all rows from the table
    bigquery_connection.query("delete from ecommerce.cities where city_id >= 0").result()

    # insert the cities from the dataframe
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    table_id = "secret-compass-453715-h4.ecommerce.cities"
    job = bigquery_connection.load_table_from_dataframe(df_cities, table_id, job_config=job_config)
    job.result()
    

def populate_customer_distribution_in_bigquery(bigquery_connection, df_customer_distribution : pd.DataFrame):
    # populate the customer population in bigquery

    # delete all rows from the table
    bigquery_connection.query("delete from ecommerce.customer_distribution where city_id >= 0").result()

    # add the created_at column
    df_customer_distribution["created_at"] = datetime.datetime.now()

    # insert the cities from the dataframe
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    table_id = "secret-compass-453715-h4.ecommerce.customer_distribution"
    job = bigquery_connection.load_table_from_dataframe(df_customer_distribution, table_id, job_config=job_config)
    job.result()
    

def read_query_from_bigquery(bigquery_connection, query_str):
    # read a query from bigquery
    query = bigquery_connection.query(query_str)

    # convert the result to a pandas dataframe
    df = query.to_dataframe()
    return df


def main():
    # =========================================================Extract data from mysql and google cloud storage
    # connect to mysql
    mysql_connection = connect_mysql()

    # read cities from mysql
    df_cities = read_query_from_mysql(mysql_connection, "SELECT * from cities")

    cloud_storage = connect_storage()

    # read customers from google cloud storage in the csv format
    df_customers = read_csv_from_gcs(cloud_storage,"ecommerce_files", "customers/customers.csv")

    # =========================================================Transform data
    # calculate the distribution of customers in each city
    df_customer_distribution = calculate_customer_distribution(df_customers, df_cities)

    # =========================================================Load data to bigquery
    # connect to bigquery
    bigquery_connection = connect_bigquery()    

    # populate cities in bigquery
    populate_cities_in_bigquery(bigquery_connection, df_cities)

    populate_customer_distribution_in_bigquery(bigquery_connection, df_customer_distribution)
    
    # show customers didtribution in cities
    df_distribution_in_cities = read_query_from_bigquery(bigquery_connection, "SELECT cities.name as city_name, customer_dist.population \
                                        from `secret-compass-453715-h4.ecommerce.customer_distribution` as customer_dist \
                                        left join `secret-compass-453715-h4.ecommerce.cities` as cities on customer_dist.city_id = cities.city_id \
                                        order by population desc")
    
    # write the distribution in cities to google cloud storage
    write_csv_to_gcs(cloud_storage,"ecommerce_files", "customers/distributions_in_cities.csv", df_distribution_in_cities)

if __name__ == "__main__":
    main()
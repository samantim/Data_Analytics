from google.cloud import bigquery
from faker import Faker
import datetime
import pandas as pd
import mysql.connector as mysql

def connect_bigquery():
    # connect to bigquery
    bigquert_connection = bigquery.Client("secret-compass-453715-h4")
    return bigquert_connection

def connect_mysql():
    # connect to mysql
    mysql_connection = mysql.connect(
        host="localhost",
        port = "3306",
        user = "root",
        password = "6902",
        database = "ecommerce"
    )
    return mysql_connection

def read_cities(mysql_connection):
    # read cities from mysql database - the first 20 cities
    cursor = mysql_connection.cursor()
    cursor.execute("SELECT * from cities order by name limit 20")
    result = cursor.fetchall()
    # convert the result to a pandas dataframe
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    cursor.close()
    return df


def populate_cities_from_mysql(bigquery_connection, df_cities : pd.DataFrame):
    # populate cities read from the mysql table in bigquery

    # delete all rows from the table
    query = bigquery_connection.query("delete from ecommerce.cities where city_id >= 0")

    # insert the cities from the dataframe
    for i in range(df_cities.shape[0]):
        query_string = f"INSERT INTO `secret-compass-453715-h4.ecommerce.cities` (city_id, name, created_at) VALUES ({i+1}, '{df_cities.loc[i,"name"]}', '{df_cities.loc[i,"created_at"]}')"
        query = bigquery_connection.query(query_string)   
    
    query.result()  # Wait for the query to finish

def populate_cities_fakegenerated(bigquery_connection):
    # populate cities with fake data in the case of generating new data
    fake = Faker(seed=0)

    # delete all rows from the table
    query = bigquery_connection.query("delete from ecommerce.cities where city_id >= 0")

    # insert the cities from the faker
    for i in range(10):
        city_name = fake.city()
        query_string = f"INSERT INTO `secret-compass-453715-h4.ecommerce.cities` (city_id, name, created_at) VALUES ({i+1}, '{city_name}', '{datetime.datetime.now()}')"
        query = bigquery_connection.query(query_string)   
    
    query.result()  # Wait for the query to finish


def show_cities(bigquery_connection):
    # show the cities in the bigquery table
    query = bigquery_connection.query("SELECT * from `secret-compass-453715-h4.ecommerce.cities` order by city_id")

    df = query.to_dataframe()
    print(df)

def main():
    # connect to mysql
    mysql_connection = connect_mysql()
    # read cities from mysql
    df_cities = read_cities(mysql_connection)
    # connect to bigquery
    bigquert_connection = connect_bigquery()    
    # populate cities in bigquery
    populate_cities_from_mysql(bigquert_connection, df_cities)
    # show the cities in bigquery
    show_cities(bigquert_connection)

if __name__ == "__main__":
    main()
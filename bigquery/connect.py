from google.cloud import bigquery
from faker import Faker
import datetime

def connect_bigquery():
    client = bigquery.Client("secret-compass-453715-h4")
    return client

def populate_cities(bigquert_connection):
    query = bigquert_connection.query("INSERT INTO `secret-compass-453715-h4.ecommerce.cities` (city_id, name, created_at) VALUES (1, 'Basel', '2023-10-01 12:00:00')")
    query = bigquert_connection.query("INSERT INTO `secret-compass-453715-h4.ecommerce.cities` (city_id, name, created_at) VALUES (2, 'Berlin', '2023-10-01 12:00:00')")
    query.result()  # Wait for the query to finish


def show_cities(bigquert_connection):
    query = bigquert_connection.query("SELECT * from `secret-compass-453715-h4.ecommerce.cities`")

    df = query.to_dataframe()
    print(df)

def main():
    client = connect_bigquery()
    populate_cities(client)
    show_cities(client)

if __name__ == "__main__":
    main()
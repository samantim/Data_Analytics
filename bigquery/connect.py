from google.cloud import bigquery

client = bigquery.Client()

result = client.query("SELECT * from `secret-compass-453715-h4.ecommerce.cities`")
print(result)
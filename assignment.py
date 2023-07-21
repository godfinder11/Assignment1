from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType
 # Kafka configuration
KAFKA_BROKER = 'your_kafka_broker'
KAFKA_TOPIC = 'x1'


# Elasticsearch configuration
ELASTICSEARCH_HOST = 'your_elasticsearch_host'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_INDEX = 'clickstream_data'


# Spark configuration
SPARK_MASTER = 'local[*]'
SPARK_APP_NAME = 'ClickstreamProcessor'

# Create a Kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BROKER)

# Create an Elasticsearch client
es = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}])



# Create a SparkSession
spark = SparkSession.builder.master(SPARK_MASTER).appName(SPARK_APP_NAME).getOrCreate()

# Define the schema for clickstream data
clickstream_schema = StructType([
    StructField("row_key", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("url", StringType(), True),
    StructField("country", StringType(), True),
    StructField("city", StringType(), True),
    StructField("browser", StringType(), True),
    StructField("os", StringType(), True),
    StructField("device", StringType(), True),
])

# Function to process and aggregate clickstream data
def process_clickstream_data(data):
    # Create a DataFrame from the JSON data
    df = spark.read.json(data, schema=clickstream_schema)
    
    # Perform the required aggregations (e.g., group by URL and country)
    aggregated_df = df.groupBy("url", "country").agg(
        {"user_id": "count", "timestamp": "avg"}  # Count of clicks and average time spent
    ).withColumnRenamed("count(user_id)", "click_count").withColumnRenamed("avg(timestamp)", "avg_time_spent")
    
    # Convert the aggregated DataFrame to an Elasticsearch-friendly format
    es_data = aggregated_df.toJSON().collect()
    
    # Index the processed data in Elasticsearch
    for record in es_data:
        es.index(index=ELASTICSEARCH_INDEX, body=record)

# Main data pipeline loop
for message in consumer:
    data = message.value.decode("utf-8")
    process_clickstream_data(data)


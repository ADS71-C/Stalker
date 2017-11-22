import os
import findspark

findspark.init('C:\spark-2.2.0-bin-hadoop2.7\spark-2.2.0-bin-hadoop2.7')
findspark.find()

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Proftaak") \
    .getOrCreate()

sc = spark.sparkContext
sc.addPyFile(r'C:\Users\mike_\Documents\School\Proftaak\soft-boiled.zip')
from src.algorithms import gmm

tweets_df = None
for filename in os.listdir('dataset'):
    print(filename)
    chunk = spark.read.json('dataset/' + filename)
    chunk = chunk.filter('geo is not null')
    chunk = chunk.filter('place is not null')
    chunk = chunk.select(['user', 'text', 'geo', 'place', 'entities.urls', 'extended_entities.media'])
    if tweets_df is not None:
        tweets_df = tweets_df.union(chunk)
    else:
        tweets_df = chunk

tweets_df.createOrReplaceTempView('my_tweets')
gmm_model = gmm.train_gmm(spark, 'my_tweets', ['user.location', 'text'], min_occurrences=5, max_num_components=12)


# Save model for future prediction use
gmm.save_model(gmm_model, 'model_file.csv')

import json
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegressionModel
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType

spark = SparkSession.builder.appName("mllib_cassandra_predict_app").getOrCreate()
spark.conf.set("spark.cassandra.connection.host", "localhost")

checkpoint_location = "ml_checkpoint"
keyspace = "streaming_1004"

data_path = "*.csv"
model_dir = "models"
model = LinearRegressionModel.load(model_dir + "/model")

schema = StructType.fromJson(json.loads('{"fields":[{"metadata":{},"name":"Date","nullable":true,"type":"timestamp"},{"metadata":{},"name":"Open","nullable":true,"type":"double"},{"metadata":{},"name":"High","nullable":true,"type":"double"},{"metadata":{},"name":"Low","nullable":true,"type":"double"},{"metadata":{},"name":"Close","nullable":true,"type":"double"},{"metadata":{},"name":"Adj Close","nullable":true,"type":"double"},{"metadata":{},"name":"Volume","nullable":true,"type":"integer"}],"type":"struct"}'))

features = ["Open,High,Low,Close,Adj Close"]

data = spark \
    .readStream \
    .format("csv") \
    .schema(schema) \
    .options(header=True, maxFilesPerTrigger=1) \
    .load(data_path)
    
    
def prepare_data(df, features):    
    f_columns = ",".join(features).split(",")
    all_columns = ",".join(features).split(",")
    all_columns = list(map(lambda c: F.col(c), all_columns))
    model_data = df.select(all_columns)
    assembler = VectorAssembler(inputCols=f_columns, outputCol='features')
    model_data = assembler.transform(model_data)
    model_data = model_data.select('features')
    return model_data

def process_batch(df, epoch):
    model_data = prepare_data(df, features)
    prediction = model.transform(model_data)
    prediction.write\
        .format("org.apache.spark.sql.cassandra") \
        .mode("append")\
        .options(keyspace=keyspace, table="student910_9_prediction") \
        .save()

def foreach_batch_output(df):
    from datetime import datetime as dt
    date = dt.now().strftime("%Y%m%d%H%M%S")
    return df\
        .writeStream \
        .trigger(processingTime='%s seconds' % 10) \
        .foreachBatch(process_batch) \
        .option("checkpointLocation", checkpoint_location + "/" + date)\
        .start()

stream = foreach_batch_output(data)
stream.awaitTermination()
spark.stop()
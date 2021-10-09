# Подготовка и обучение данных для модели линнейной регрессии

from pyspark.ml.evaluation import RegressionEvaluator, BinaryClassificationEvaluator
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("stud910_9_prepare_and_train_app").master("local[*]").getOrCreate()

data_path = "Amazon.csv"
model_dir = "models"

# read data from storage
data = spark\
    .read\
    .format("csv")\
    .options(inferSchema=True, header=True) \
    .load(data_path)
    
# target
target = ["Volume"]

# model evaluator. Используем модель линейной регрессии 
evaluator = RegressionEvaluator() \
        .setMetricName("rmse") \
        .setLabelCol("label") \
        .setPredictionCol("prediction")
        
# Подготовка и обучение данных

def prepare_data(data, features, target):
    # features
    f_columns = ",".join(features).split(",")
    # target
    f_target = ",".join(target).split(",")
    f_target = list(map(lambda c: F.col(c).alias("label"), f_target))
    # all columns
    all_columns = ",".join(features + target).split(",")
    all_columns = list(map(lambda c: F.col(c), all_columns))
    # model data set
    model_data = data.select(all_columns)
    # preparation
    assembler = VectorAssembler(inputCols=f_columns, outputCol='features')
    model_data = assembler.transform(model_data)
    model_data = model_data.select('features', f_target[0])
    return model_data

def prepare_and_train(data, features, target):
    model_data = prepare_data(data, features, target)
    # train, test
    train, test = model_data.randomSplit([0.8, 0.2], seed=12345)
    # model
    lr = LinearRegression(featuresCol='features', labelCol='label', maxIter=10, regParam=0.01)
    # train model
    model = lr.fit(train)
    # check the model on the test data
    prediction = model.transform(test)
    prediction.show(5)
    evaluation_result = evaluator.evaluate(prediction)
    print("Evaluation result: {}".format(evaluation_result))
    return model

features = ["Open,High,Low,Close,Adj Close"]

model = prepare_and_train(data, features, target)
model.write().overwrite().save(model_dir + "/model")
spark.stop()
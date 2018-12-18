#Set ENV
import os
os.environ["SPARK_HOME"] = "/opt/spark"
os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3.6"
os.environ["PYSPARK_DRIVER_PYTHON"] = "ipython3"
#%set_env SPARK_HOME=/opt/spark
#%set_env PYSPARK_PYTHON=/usr/bin/python3.6
#%set_env PYSPARK_DRIVER_PYTHON=ipython3

#Adding pyspark to sys.path at runtime
import findspark
findspark.init()
findspark.add_jars('/opt/spark/jars/elasticsearch-spark-20_2.11-5.3.0.jar')

#Spark Init
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

def create_spark_session(app_name='pySpark'):
    conf = (SparkConf()
            .setAppName(app_name)
            .setMaster('local[*]')
            .set('spark.driver.memory', '4G')
            )
    context = SparkContext(conf=conf)
    spark = SparkSession(context).builder.getOrCreate()
    return spark

#Usage
#spark = create_spark_session()
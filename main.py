# -*- coding: utf-8 -*-
"""
author SparkByExamples.com
"""

import pandas as pd    
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from etherscan import *

def show():
    data = [['Scott', 50], ['Jeff', 45], ['Thomas', 54],['Ann',34]] 

    # pandasDF = pd.DataFrame(data, columns = ['Name', 'Age']) 
    
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("SparkByExamples.com") \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("OFF")
    
    sparkDF=spark.createDataFrame(pandasDF)

    mySchema = StructType([ StructField("First Name", StringType(), True)\
                        ,StructField("Age", IntegerType(), True)])

    sparkDF2 = spark.createDataFrame(pandasDF,schema=mySchema)

    return sparkDF2.toPandas()

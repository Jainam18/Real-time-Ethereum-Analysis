import pandas as pd
from pyspark.sql import SparkSession
from scraper_updated import main
import time
from constants import *
import pyspark.sql.functions as F
# import matplotlib.pyplot as plt

spark = None
current_time = time.time()

def get_data():

    hashes_df = pd.read_csv("hashes.csv")['0']
    hashes_list = hashes_df.to_list()

    scraped_data = main()

    global spark
    spark = SparkSession.builder.appName(
        "pandas to spark").getOrCreate()

    df_spark = spark.createDataFrame(scraped_data)

    data_no_duplicates = df_spark.filter(
        ~df_spark['hash'].isin(hashes_list))

    new_hashes = data_no_duplicates.toPandas()['hash']
    aggregated_hashes = pd.concat([hashes_df, new_hashes])

    aggregated_hashes.to_csv('hashes.csv')

    return data_no_duplicates


def do_analysis(df_spark=None):
    
    # spark = SparkSession.builder.appName(
    #     "pandas to spark").getOrCreate()
    
    # df_spark = spark.read.option('header', 'true').csv("data/new_data.csv")
    
    columns_to_drop = ['id','type_2718','date','v','r','s','version']
    df = df_spark.drop(*columns_to_drop)

    # convert numeric columns to appropriate data types
    df = df.withColumn("block_id", df["block_id"].cast("integer"))
    df = df.withColumn("call_count", df["call_count"].cast("integer"))
    df = df.withColumn("value", df["value"].cast("float"))
    df = df.withColumn("value_usd", df["value_usd"].cast("float"))
    df = df.withColumn("internal_value", df["internal_value"].cast("float"))
    df = df.withColumn("internal_value_usd", df["internal_value_usd"].cast("float"))
    df = df.withColumn("gas_used", df["gas_used"].cast("integer"))
    df = df.withColumn("fee", df["fee"].cast("float"))
    df = df.withColumn("fee_usd", df["fee_usd"].cast("float"))
    df = df.withColumn("gas_limit", df["gas_limit"].cast("float"))
    df = df.withColumn("gas_price", df["gas_price"].cast("float"))
    df = df.withColumn("nonce", df["nonce"].cast("integer"))
    df = df.withColumn("effective_gas_price", df["effective_gas_price"].cast("float"))
    df = df.withColumn("max_fee_per_gas", df["max_fee_per_gas"].cast("float"))
    df = df.withColumn('max_priority_fee_per_gas', df['max_priority_fee_per_gas'].cast("integer"))
    df = df.withColumn("base_fee_per_gas", df["base_fee_per_gas"].cast("integer"))

    num_cols = []
    cat_cols = []

    for s in df.schema:
        data_type = str(s.dataType)
        if data_type == "StringType()":
            cat_cols.append(s.name)
        
        if data_type == "LongType()" or data_type == "DoubleType()" or data_type=='IntegerType()':
            num_cols.append(s.name)

    # for i in cat_cols:
    #     num_unique = df.select(approxCountDistinct(f"{i}")).collect()[0][0]
    #     print(f"{i} has {num_unique} unique values")

    df = df.fillna(0)
    # df.show()

    type_analysis = df.groupBy("type").agg(F.sum("gas_used").alias("total_gas_used"),F.sum("value_usd").alias("total_value_txn_usd"),F.sum("effective_gas_price").alias("total_effective_gas_price"),F.sum("fee_usd").alias("total_fee_usd"),F.sum("call_count").alias("total_call_count"))
    type_analysis_pd = type_analysis.toPandas()
    
    total_gas = df.select(F.sum("gas_used")).collect()[0][0]
    total_value_transferred = df.agg(F.sum("value_usd")).collect()[0][0]
    total_transactions = df.count()
    
    total_stats = pd.DataFrame({"total_gas":[total_gas], "total_value_transferred":[total_value_transferred], "total_transactions":[total_transactions]})
    print(total_stats, type_analysis_pd)
    
    
    output = [type_analysis_pd, total_stats]
    type_analysis_pd.to_csv("type_analysis.csv")
    total_stats.to_csv("total_stats.csv")
    return output


def add_to_db(analysis=None):
    print("---analysis---")
    
    if analysis:
        analysis_total = analysis[1]
        analysis_type = analysis[0]
    else:
        analysis_total = pd.read_csv("total_stats.csv", index_col=0)
        analysis_type = pd.read_csv("type_analysis.csv", index_col=0)
    
    analysis_type = analysis_type.set_index('type')
    type_df = pd.DataFrame()
    try:
        type_df = pd.read_csv("data/type_data.csv", index_col=0)
    except:
        print("---------------file not found, using cached data-------------------------")
    print("fetched typedf:")
    print(type_df)
    print("scraped typedf:")
    print(analysis_type)
    
    if not type_df.empty:
        type_df = pd.concat([analysis_type, type_df], axis=0)
    else:
        type_df = analysis_type

    print("typedf before agg:")
    print(type_df)
    type_df = type_df.groupby('type').agg('sum')
    
    print("new typedf:")
    print(type_df)
    
    type_df.to_csv("data/type_data.csv")
    
    #total table
    total_df = pd.DataFrame()
    try:
        total_df = pd.read_csv("data/total_data.csv", index_col=0)
    except:
        print("---------------file not found, using cached data-------------------------")
    print("fetched totaldf:")
    print(total_df)
    
    if not total_df.empty:
        # print("analysis_total, total_df")
        # print(analysis_total.head())
        total_df = pd.concat([analysis_total, total_df], axis=0)
        # print(total_df.head())
        
    else:
        total_df = analysis_total
        
    total_df = total_df.agg(['sum'])
    
    
    print("new totaldf:")
    print(total_df)
    
    total_df.to_csv("data/total_data.csv")


def analysis_iteration():
    data = get_data()
    analysis = do_analysis(data)
    add_to_db(analysis)
    # add_to_db()

    
def create_db():
    add_to_db()
    print("created db")
    
if __name__ == '__main__':
    while True:
        analysis_iteration()
        print("iteration complete. Waiting for 60 secs")
        time.sleep(60)
import asyncio
from websockets.server import serve
import pandas as pd
import sqlite3
import pickle
from constants import *


conn = sqlite3.connect('analysis.sqlite')
# sql_query = f'SELECT * FROM {tables[0]["table"]}'

async def echo(websocket):
    query = ""
    async for message in websocket:
        if message:
            print("query received: ", message)
            query = message
            break
        else:
            print("No query received")
            break
    
    pickled_df = None
    try:
        
        # parsed_query = pd.read_sql_query(query if query else sql_query, conn)
        # df = pd.DataFrame(parsed_query, columns=tables[0]["columns"])
        # print(df.shape)
        # print("query: ", query if query else sql_query)
        type_df = pd.read_csv("data/type_data.csv").iloc[:,1:]
        total_df = pd.read_csv("data/total_data.csv").iloc[:,1:]
        print(type_df, total_df)
        # df = pd.read_csv("output.csv") 
        pickled_df = pickle.dumps([type_df, total_df])
    except Exception as e:
        print("Exception", e)
    finally:
        await websocket.send(pickled_df)


async def main():
    async with serve(echo,'', socket_port):
        await asyncio.Future()

asyncio.run(main())

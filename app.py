import threading
import time
from flask import Flask, render_template, request
from turbo_flask import Turbo
from socket_client import get_socket_message
from colab import create_db, analysis_iteration
from constants import *
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)
turbo = Turbo(app)

# create_db()

f = open("hashes.csv", "w")
f.write(",0\n0,2")
f.close()

query = ""


@app.context_processor
def inject_load():
    # print("sending query:", query)
    data = get_socket_message(query=query)
    print(data)

    df = pd.DataFrame(data[0],
                        columns=data[0].columns)
    # Create Bar chart
    fig = px.bar(df, x=df.index, y='total_gas_used', color='total_gas_used', barmode='group')
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return {"type_data": data[0], "total_data": data[1], "graphJSON": graphJSON }


@app.route('/', methods=['GET', 'POST'])
def index():
    global query
    if request.method == 'POST':
        if request.form.get('Filter') == 'Filter':
            print("Filtering")
            query = ""
            # query = f"SELECT * FROM {table_name} WHERE TxnHash='0xd985d71e004f10e1034d5c152dea402496509d6f2b2643e215b7766676d5eee0'"
            
        elif request.form.get('Reset') == 'Reset':
            print("Resetting")
            query = ""
    # Students data available in a list of list
    students = [['Akash', 34, 'Sydney', 'Australia'],
                ['Rithika', 30, 'Coimbatore', 'India'],
                ['Priya', 31, 'Coimbatore', 'India'],
                ['Sandy', 32, 'Tokyo', 'Japan'],
                ['Praneeth', 16, 'New York', 'US'],
                ['Praveen', 17, 'Toronto', 'Canada']] 
    # Convert list to dataframe and assign column values
    
    return render_template('index.html')

# @app.route('/template')
# def dashboard():
#     return render_template('index.html')

# @app.route('/set-query')
# def set_query():
#     print("Updating query")
#     global query
#     query = f"SELECT * FROM {table_name} WHERE Age='12 secs ago'"
#     return ("nothing")


def update_load():
    with app.app_context():
        while True:
            time.sleep(60)
            turbo.push(turbo.replace(
                render_template('transactions.html'), 'load'))


th = threading.Thread(target=update_load)
th.daemon = True
th.start()


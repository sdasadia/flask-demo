
################## IMPORT REQUIRED PACKAGES ########################
from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from pandas import DataFrame,Series
import datetime as dt
import bokeh
from bokeh.plotting import figure
from bokeh.plotting import figure, show
from bokeh.models import HoverTool
from bokeh.charts import TimeSeries, output_file, show
from bokeh.embed import components

import datetime as dt

import quandl
quandl.ApiConfig.api_key = "ZL6bU8BmT8BXSAzGLUbQ"

######################## OBTAIN  / PLOT  DATA #############################

def make_plot(price_req, stock_symb):

    now = dt.datetime.now().date()
    then = now - dt.timedelta(days=30)
    then = "&start_date=" + then.strftime("%Y-%m-%d")
    now = "&end_date=" + now.strftime("%Y-%m-%d")

    symb = "WIKI/" + stock_symb

    mydata = quandl.get(symb, start_date=then, end_date=now)
    mydata = mydata[price_req]
    mydata.reset_index(inplace=True)

    TOOLS = [HoverTool()]
    p = TimeSeries(mydata, x='Date', ylabel='Stock Prices', plot_height=300,
                   tools = TOOLS)
    script, div = components(p)

    return script, div


####################################################################

app = Flask(__name__)

quandl.ApiConfig.api_key = "ZL6bU8BmT8BXSAzGLUbQ"

@app.route('/')
def main():
	return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/plotpage', methods=['POST'])
def plotpage():

    stock_symb = request.form['tickerText'].upper()
    reqList1 = request.form.getlist('priceCheck')
    reqList2 = request.form.getlist('priceCheck1')
    reqList3 = request.form.getlist('priceCheck2')
    reqList4 = request.form.getlist('priceCheck3')# checkboxes
    reqList = reqList1 + reqList2 + reqList3 + reqList4

    try:

        script, div = make_plot(reqList, stock_symb)
        return render_template('plot.html', ticker = stock_symb, script = script, div = div )

    except:

        return render_template('plot.html', error = " <h2>Error \n Most likely, the ticker "
                                                    "you entered was not found in the "
                                                    "dataset.</h2>", ticker = stock_symb )

if __name__ == '__main__':
	app.run(port=33507)


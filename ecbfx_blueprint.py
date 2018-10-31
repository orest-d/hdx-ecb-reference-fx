import logging
from flask import Flask, Response, Blueprint
import ecbfx

app = Blueprint('ecbfx', __name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    return """
<html>
    <head>
        <title>HDX ECB reference FX</title>
    </head>
    <body>
        <h1>HDX interface to <a href="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html">ECB reference FX rates</a></h1>
        Data source: %s
        
        <ul>
            <li><a href="api/original_data.zip">Original data (zip)</a></li>
            <li><a href="api/original_data.csv">Original data (csv)</a></li>
            <li><a href="api/data_with_hxl.csv">Data with HXL tags (csv)</a></li>
            <li><a href="api/fx/fx_rates_in_USD.csv">FX rates in USD (csv)</a></li>
        </ul>
    </body>    
</html>
"""%ecbfx.data_url()

@app.route('/api/original_data.zip')
def original_data_zip():
    return Response(ecbfx.raw_data(),mimetype="application/zip")

@app.route('/api/original_data.csv')
def original_data_csv():
    return Response(ecbfx.csv_content(), mimetype="text/csv")

@app.route('/api/data_with_hxl.csv')
def data_with_hxl_csv():
    df = ecbfx.add_hxl_tags(ecbfx.df_content())
    return Response(df.to_csv(index=False), mimetype="text/csv")

@app.route('/api/fx/fx_rates_in_<string:currency>.csv')
def rates_in_currency_csv(currency):
    df = ecbfx.df_content()
    df = ecbfx.add_base_currency(df)
    df = ecbfx.convert_currency(df,currency)
    df = ecbfx.add_hxl_tags(df)
    return Response(df.to_csv(index=False), mimetype="text/csv")

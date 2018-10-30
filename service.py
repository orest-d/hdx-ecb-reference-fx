import logging
from flask import Flask, Response
from urllib.request import urlopen
import zipfile
import os.path
import io
import pandas as pd

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

data_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"

def csv_content(url=None):
    "Fetch the raw csv data"
    url = data_url if url is None else url
    zipdata = urlopen(url).read()
    zf = zipfile.ZipFile(io.BytesIO(zipdata),"r")
    name = [n for n in zf.namelist() if os.path.splitext(n)[1].lower()==".csv"][0]
    return zf.read(name)

def df_content(url=None):
    "Fetch the data as a dataframe"
    return pd.read_csv(io.BytesIO(csv_content(url)))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    logger.info('Lambda function invoked index()')

    return """
<html>
    <head>
        <title>HDX ECB reference FX</title>
    </head>
    <body>
        <h1>HDX ECB reference FX</h1>
        <ul>
            <li><a href="/api/original_data.zip">Original data (zip)</a></li>
            <li><a href="/api/original_data.csv">Original data (csv)</a></li>
            <li><a href="/api/data_with_hxl.csv">Data with HXL tags (csv)</a></li>
        </ul>
    </body>    
</html>
"""

@app.route('/api/original_data.zip')
def original_data_zip():
    return Response(urlopen(data_url).read(),mimetype="application/zip")

@app.route('/api/original_data.csv')
def original_data_csv():
    return Response(csv_content(), mimetype="text/csv")

@app.route('/api/data_with_hxl.csv')
def data_with_hxl_csv():
    df = df_content()
    hxl = [("#date" if c.lower()=="date" else "#value +"+str(c))for c in df.columns]
    hxl_df = pd.DataFrame([hxl],columns=df.columns)
    df = hxl_df.append(df)
    return Response(df.to_csv(index=False), mimetype="text/csv")

if __name__ == '__main__':
    app.run(debug=True)

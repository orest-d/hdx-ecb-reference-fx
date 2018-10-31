import logging
from urllib.request import urlopen
import zipfile
import os.path
import io
import pandas as pd

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def data_url():
    return "file:///home/orest/PycharmProjects/hdx/hdx-ecb-reference-fx/eurofxref-hist.zip"
    return "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"

def raw_data(url=None):
    url = data_url() if url is None else url
    return urlopen(url).read()

def csv_content(url=None):
    "Fetch the raw csv data"
    zipdata = raw_data(url)
    zf = zipfile.ZipFile(io.BytesIO(zipdata),"r")
    name = [n for n in zf.namelist() if os.path.splitext(n)[1].lower()==".csv"][0]
    return zf.read(name)

def df_content(url=None,add_base_currency=False,base_currency="EUR"):
    "Fetch the data as a dataframe"
    return pd.read_csv(io.BytesIO(csv_content(url)))

def add_base_currency(df,base_currency="EUR"):
    df.loc[:,base_currency]=1.0
    return df

def convert_currency(df, to_currency="USD", base_currency="EUR"):
    currency_columns = [c for c in df.columns if c.lower()!="date"]
    scale = (df.loc[:,base_currency]/df.loc[:,to_currency]).values.copy()
    for c in currency_columns:
        df.loc[:,c]*=scale
    return df

def add_hxl_tags(df):
    hxl = [("#date" if c.lower()=="date" else "#value +"+str(c))for c in df.columns]
    hxl_df = pd.DataFrame([hxl],columns=df.columns)
    df = hxl_df.append(df)
    return df


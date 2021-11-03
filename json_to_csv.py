import os
import requests
from datetime import datetime
import hmac
import hashlib
import base64
import json
import time
import pandas as pd
import numpy as np

file_input = "2021-11-02 17_44_07 HK to US 100.00 RAW.txt"
file_output = "2021-11-02 17_44_07 HK to US 100.00 BODY.csv"
to_country_value = "US"
to_currency_value = "USD"

def json_to_csv_convert(file_input, file_output, to_country=None, to_currency=None):

    folder_name = "2021-11-02"
    file = open(".\output\%s\%s" % (folder_name, file_input), "r")
    data = file.read()

    start_loc = data.find("[")
    end_loc = data.find("]")

    # save body of data in string
    data = data[(start_loc):(end_loc + 1)]

    # converts body of data to list
    data_json = json.loads(data)

    # loading body of data as dataframe
    df = pd.DataFrame(data_json)

    # if using array inputs for multiple countries/currencies append these to
    # dataframe/CSV
    if to_currency and to_country is not None:
        # Adding 'to country & currency' to dataframe

        df.insert(len(df.columns) - 1, "to_country", to_country)
        df.insert(len(df.columns) - 1, "to_currency", to_currency)

    df.to_csv(".\output\%s\%s" % (folder_name, file_output))
    print('Saved body of data as: ' + file_output)
    return df

json_to_csv_convert(file_input, file_output, to_country_value, to_currency_value)


